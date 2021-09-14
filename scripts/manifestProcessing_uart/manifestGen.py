import serial
import sys
import time
from hashlib import sha256



def getitem(cosnole, itemCommand, verificationCommand):
    try:
        ser.write(itemCommand)
        time.sleep(0.3)
        response=ser.readlines()
        response=[x.rstrip() for x in response]
        response=bytearray.fromhex(response[1].decode('utf-8'))
        h = sha256()
        h.update(response)
        dataHash = h.digest()

        ser.write(verificationCommand)
        time.sleep(.2)
        verResponse=ser.readlines()
        verResponse=[x.rstrip() for x in verResponse]
        responseHash=bytearray.fromhex(verResponse[1].decode('utf-8'))
        if dataHash==responseHash:
            return response
        else:
            return False  
    except:
        return False

ser = serial.Serial('COM3', 230400, timeout=0)
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



