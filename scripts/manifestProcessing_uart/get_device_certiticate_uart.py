"""
Device Certificate generation
"""
# (c) 2015-2021 Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.
#
# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
# PARTICULAR PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT,
# SPECIAL, PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE
# OF ANY KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF
# MICROCHIP HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE
# FORESEEABLE. TO THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL
# LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED
# THE AMOUNT OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR
# THIS SOFTWARE.

import argparse
import serial
import sys
import time
from hashlib import sha256
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
import ssl





parser = argparse.ArgumentParser(description='Fetch device certificate over UART for PIC32MZW1 Curiosity Board')
parser.add_argument('-c','--com', type=str, help='COM port to use')

args = parser.parse_args()

if not args.com:
    print("Please provide COM port to use")
    sys.exit(-4)


def getitem(cosnole, itemCommand, verificationCommand=None):
    try:
        ser.write(itemCommand)
        time.sleep(0.4)
        response=ser.readlines()
        response=[x.rstrip() for x in response]
        response=bytearray.fromhex(response[1].decode('utf-8'))
        h = sha256()
        h.update(response)
        dataHash = h.digest()

        if verificationCommand:
            ser.write(verificationCommand)
            time.sleep(.2)
            verResponse=ser.readlines()
            verResponse=[x.rstrip() for x in verResponse]
            responseHash=bytearray.fromhex(verResponse[1].decode('utf-8'))
            if dataHash==responseHash:
                return response
            else:
                print(dataHash)
                print(responseHash)
                return False  
        else:
            return response
    except Exception as e:
        print(f"\nCommand {itemCommand} \nVerification: {verificationCommand}")
        print(e)
        sys.exit(-5)

def process_devCert(creds):
        
    device_cert_der = creds["devCer"]
    cert_PEM = ssl.DER_cert_to_PEM_cert(device_cert_der)
    device_cert = x509.load_pem_x509_certificate(str.encode(cert_PEM), default_backend())
    fileName=creds["serial"]
    for attr in device_cert.subject:
        if attr.oid == x509.oid.NameOID.COMMON_NAME:
            fileName=attr.value
    
    print('Validate Device Key in certificate: ', end='')
    #See if the device key in the device and the one in the certificate matches
    device_public_key_raw = bytearray(64)
    device_public_key_raw = creds["devPub"]

    device_public_key = ec.EllipticCurvePublicNumbers(
        curve=ec.SECP256R1(),
        x=int.from_bytes(device_public_key_raw[0:32], byteorder='big'),
        y=int.from_bytes(device_public_key_raw[32:64], byteorder='big'),
    ).public_key(default_backend())
    
    cert_spk_der = device_cert.public_key().public_bytes(
        format=PublicFormat.SubjectPublicKeyInfo,
        encoding=Encoding.DER
    )
    func_spk_der = device_public_key.public_bytes(
        format=PublicFormat.SubjectPublicKeyInfo,
        encoding=Encoding.DER
    )
    assert cert_spk_der == func_spk_der
    print('\tPASS')

    #see if the signer key in the device was used to issue the device certificate.
    print('Validate Signer key in Certificate: ', end='')
    signer_public_key_raw = bytearray(64)
    signer_public_key_raw = creds["signerPub"]
    
    signer_public_key = ec.EllipticCurvePublicNumbers(
        curve=ec.SECP256R1(),
        x=int.from_bytes(signer_public_key_raw[0:32], byteorder='big'),
        y=int.from_bytes(signer_public_key_raw[32:64], byteorder='big'),
    ).public_key(default_backend())

    signer_public_key.verify(
        signature=device_cert.signature,
        data=device_cert.tbs_certificate_bytes,
        signature_algorithm=ec.ECDSA(device_cert.signature_hash_algorithm)
    )
    print('\tPASS')

    print(f"\nDevice cert: {fileName}.crt")
    with open(fileName+'.crt', 'w') as f:
        f.write(cert_PEM)

ser = serial.Serial(args.com, 230400, timeout=0)
if ser.is_open:
    print("COM port connected.")
else:
    print("COM port cannot be connected.")
    sys.exit(-1)

ser.write(b'getstat\n')
time.sleep(.1)
response=ser.readlines()
response=[x.rstrip() for x in response]
#print(bytearray.fromhex(response[1].decode('utf-8')))
if b'01'!=response[1]:
    print("failed establishing connection with the kit.")
    sys.exit(-2)

print("Collecting device data. This takes a few seconds to run")
creds={}
creds["serial"]=getitem(ser,b'getserial\n').hex()
creds["devCer"]=getitem(ser,b'getcert 2\n',b'gethash A\n')
creds["signerPub"]=getitem(ser,b'getkey 6\n',b'gethash 6\n')
creds["devPub"]=getitem(ser,b'getkey 7\n',b'gethash 7\n')


for key in creds:
    if not key:
        print(f"Failed fetching {key}")
        sys.exit(-3)

process_devCert(creds=creds)