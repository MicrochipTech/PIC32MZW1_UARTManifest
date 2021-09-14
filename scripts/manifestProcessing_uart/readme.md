# Generating Device Manifest File over UART for PIC32MZW1

The WFI32E01 module on the curiosity board has an on-board TNG module. The primary security elements of the TNG can be extracted via UART by flashing the firmware present in this project. This includes the device certificate, public keys in different slots etc that are required to generate the device's manifest file by scripts in this folder. 

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
    python createManifest_uart.py -c COM3
    ```
    
    > ***Note***: Make sure that the correct COM port is passed to the script.
    
1. A manifest file with the device serial number prefix will be generated in the scripts folder.
1. Store the `json` file as well as the `log_signer` certificate.
    - `log_signer` certificate is a self signed certificate used to sign the manifest. This is essential to validate the authenticity of the manifest file during device registration.
