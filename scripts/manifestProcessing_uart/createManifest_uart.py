"""
Manifest generation
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

from cryptoauthlib import *
from common import *
from manifest_generation_helper import *
import argparse
import serial
import sys
import time
from hashlib import sha256


parser = argparse.ArgumentParser(description='Generate Manifest File over UART for PIC32MZW1 Curiosity Board')
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
creds["key0"]=getitem(ser,b'getkey 0\n',b'gethash 0\n')
creds["key1"]=getitem(ser,b'getkey 1\n',b'gethash 1\n')
creds["key2"]=getitem(ser,b'getkey 2\n',b'gethash 2\n')
creds["key3"]=getitem(ser,b'getkey 3\n',b'gethash 3\n')
creds["key4"]=getitem(ser,b'getkey 4\n',b'gethash 4\n')
creds["rootPub"]=getitem(ser,b'getkey 5\n',b'gethash 5\n')
creds["signerPub"]=getitem(ser,b'getkey 6\n',b'gethash 6\n')
creds["devPub"]=getitem(ser,b'getkey 7\n',b'gethash 7\n')
creds["rootCer"]=getitem(ser,b'getcert 0\n',b'gethash 8\n')
creds["signerCer"]=getitem(ser,b'getcert 1\n',b'gethash 9\n')
creds["devCer"]=getitem(ser,b'getcert 2\n',b'gethash A\n')


for key in creds:
    if not key:
        print(f"Failed fetching {key}")
        sys.exit(-3)

print("Collected device data. Creating Manifest")

logger_cert = create_log_signer()

manifest_data, manifest_name = tng_data(creds=creds)