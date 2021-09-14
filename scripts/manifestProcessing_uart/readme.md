# Generating Device Manifest File over UART for PIC32MZW1

The WFI32E01 module on the curiosity board has an on-board TNG module. The primary security elements of the TNG can be exposed via UART by flashing the firmware present in this project. This includes the device certificate, public keys in different slots etc that are required to generate the device's manifest file by scripts in this folder. 

Follow these steps to generate the manifest file of a curiosity board running the OOB demo:

- Clone this repo to your PC.
- Make sure that you have python 3 installed in your PC
- Install python dependencies from the `requirements.txt` file in this scripts folder. 
    ```sh
    python -m pip install -r requirements.txt
    ```
- Power up the Curiosity board.
    - Make sure that a USB cable is connected to the PC from J204 (`USB Power`).
- Flash the firmware present in this repo.
- Connect UART1 to the PC using a USB to UART converter. Make sure that you dont open a terminal but make a note of the COM port.
- Execute the following commands from the cloned repo. Make sure that the correct COM port is passed to the script.
    ```sh
    cd scripts\ManifestProcessing
    python createManifest_msd.py -c COM3
    ```
- A manifest file with the device serial number prefix will be generated in the scripts folder.
- Store the `json` file as well as the `log_signer` certificate.
    - `log_signer` certificate is a self signed certificate used to sign the manifest. This is essential to validate the authenticity of the manifest file during device registration.