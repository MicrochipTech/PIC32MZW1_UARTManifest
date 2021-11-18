# Generating Device Manifest File over UART for PIC32MZW1

The WFI32E01 module on the curiosity board has an on-board TNG module. The primary security elements of the TNG can be extracted via UART by flashing the firmware present in this project. This includes the device certificate, public keys in different slots etc. The `get_device_certiticate_uart.py` script in this folder lets you extract and verify the device certificate. 

Follow these steps to generate the manifest file of a curiosity board running the FW available in this repository:

1. Clone this repo to your PC.
1. Make sure that you have python 3 installed in your PC
1. Install python dependencies from the `requirements.txt` file in this scripts folder. 
    ```sh
    python -m pip install -r requirements.txt
    ```
1. Power up the Curiosity board.
    - Make sure that a USB cable is connected to the PC from J204 (`USB Power`).
1. Flash the firmware present in this repo.

    > ***Note:*** you can either compile the firmware from the [sources](../../../../tree/main/src/firmware) or download the hex file from the [releases tab](https://github.com/MicrochipTech/PIC32MZW1_UARTManifest/releases)

1. Connect UART1 to the PC using a USB to UART converter. Make sure that you dont open a terminal but make a note of the COM port.
1. Execute the following commands from the cloned repo. 
    ```sh
    cd scripts\ManifestProcessing
    python get_device_certiticate_uart.py -c COM3
    ```
    
    > ***Note***: Make sure that the correct COM port is passed to the script.
    
1. The device certificate with the name from the CN field of the certificate will be generated in the scripts folder.
