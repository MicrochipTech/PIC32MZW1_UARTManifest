# PIC32MZW1_UARTManifest
Tool framework to extract device certificates and manifest file from the TNGTLS device onboard a WFI32 module 

## Manifest genration 
Read execution instructions at [scripts/manifestProcessing_uart/readme.md](scripts/manifestProcessing_uart/readme.md)

## Device certificate 
Read execution instructions at [scripts/manifestProcessing_uart/readme_deviceCertificate.md](scripts/manifestProcessing_uart/readme_deviceCertificate.md)


## What does the firmware do?

The firmware recieves commands over UART (***230400 8N1***) and responds with the corresponding data fetched from the TNGTLS attached on I2C2 interface of PIC32MZW1 / WFI32. 

The FW has commands to fetch the information stored in the TNGTLS slots as well as the sha256 of the data sent over UART. This message hash can be used to verify the sanity of the information recieved over UART. 

FW commands:

```
1. getserial
2. getstat
    0 : init failure
    1 : init success
3. getkey <n>
    0 : Slot0 key
    1 : Slot1 key
    2 : Slot2 key
    3 : Slot3 key
    4 : Slot4 key
    5 : root Public key
    6 : signer Public key
    7 : device Public key
4. getcert <n>
    0 : root certificate
    1 : signer certificate
    2 : device certificate
5. gethash <n>
    0 : Slot0 key hash
    1 : Slot1 key hash
    2 : Slot2 key hash
    3 : Slot3 key hash
    4 : Slot4 key hash
    5 : root Public key hash
    6 : signer Public key hash
    7 : device Public key hash
    8 : root certificate hash
    9 : signer certificate hash
    a : device certificate hash
```

> ***Note***: `gethash` should be called only after the corresponding `getkey` or `getcert` is executed. Else the command will return `0` 
