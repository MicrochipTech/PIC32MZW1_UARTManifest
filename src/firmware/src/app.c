/*******************************************************************************
  MPLAB Harmony Application Source File

  Company:
    Microchip Technology Inc.

  File Name:
    app.c

  Summary:
    This file contains the source code for the MPLAB Harmony application.

  Description:
    This file contains the source code for the MPLAB Harmony application.  It
    implements the logic of the application's state machine and it may call
    API routines of other MPLAB Harmony modules in the system, such as drivers,
    system services, and middleware.  However, it does not call any of the
    system interfaces (such as the "Initialize" and "Tasks" functions) of any of
    the modules in the system or make any assumptions about when those functions
    are called.  That is the responsibility of the configuration-specific system
    files.
 *******************************************************************************/

// *****************************************************************************
// *****************************************************************************
// Section: Included Files
// *****************************************************************************
// *****************************************************************************

#include "app.h"
#include "system/console/sys_console.h"
#include "atca_basic.h"
#include "tng_atcacert_client.h"
#include "host/atca_host.h"

// *****************************************************************************
// *****************************************************************************
// Section: Global Data Definitions
// *****************************************************************************
// *****************************************************************************

// *****************************************************************************

#define SHA256_DIGEST_SIZE 32

APP_DATA appData;

extern ATCAIfaceCfg atecc608_0_init_data;
uint8_t sernum[9];
char displayStr[ATCA_SERIAL_NUM_SIZE * 3];
size_t displen = sizeof (displayStr);
ATCA_STATUS status;
bool stat = false;


uint8_t pubKey0_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t pubKey1_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t pubKey2_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t pubKey3_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t pubKey4_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t rootPubKey_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t signerPubKey_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t devicePubKey_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t rootCert_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t signerCert_hash[SHA256_DIGEST_SIZE] = {0};
uint8_t deviceCert_hash[SHA256_DIGEST_SIZE] = {0};

void _APP_Commands_GetStatus(SYS_CMD_DEVICE_NODE* pCmdIO, int argc, char** argv) {
    SYS_CONSOLE_PRINT("%02x\r\n", stat);
}

void _APP_Commands_GetSerial(SYS_CMD_DEVICE_NODE* pCmdIO, int argc, char** argv) {
    SYS_CONSOLE_PRINT("%s\r\n", displayStr);
}

void _APP_Commands_GetKey(SYS_CMD_DEVICE_NODE* pCmdIO, int argc, char** argv) {
    uint8_t public_key[ATCA_PUB_KEY_SIZE] = {0};
    uint8_t* element = NULL;
    if (argc == 2) {
        switch (*argv[1]) {
            case '0':
                status = atcab_get_pubkey(0, public_key);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, pubKey0_hash);
                    element = public_key;
                }
                break;
            case '1':
                status = atcab_get_pubkey(1, public_key);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, pubKey1_hash);
                    element = public_key;
                }
                break;
            case '2':
                status = atcab_get_pubkey(2, public_key);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, pubKey2_hash);
                    element = public_key;
                }
                break;
            case '3':
                status = atcab_get_pubkey(3, public_key);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, pubKey3_hash);
                    element = public_key;
                }
                break;
            case '4':
                status = atcab_get_pubkey(4, public_key);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, pubKey4_hash);
                    element = public_key;
                }
                break;
            case '5':
                status = tng_atcacert_root_public_key(public_key);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, rootPubKey_hash);
                    element = public_key;
                }
                break;
            case '6':
                status = tng_atcacert_signer_public_key(public_key, NULL);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, signerPubKey_hash);
                    element = public_key;
                }
                break;
            case '7':
                status = tng_atcacert_device_public_key(public_key, NULL);
                if (ATCA_SUCCESS == status) {
                    atcah_sha256(ATCA_PUB_KEY_SIZE, public_key, devicePubKey_hash);
                    element = public_key;
                }
                break;
            default:
                break;
        }

        if (NULL != element) {
            for (int i = 0; i < ATCA_PUB_KEY_SIZE; i++) {
                SYS_CONSOLE_PRINT("%02x ", element[i]);
            }
        } else {
            for (int i = 0; i < ATCA_PUB_KEY_SIZE; i++) {
                SYS_CONSOLE_PRINT("00 ");
            }
        }
        SYS_CONSOLE_PRINT("\r\n");
    }
}

void _APP_Commands_GetHash(SYS_CMD_DEVICE_NODE* pCmdIO, int argc, char** argv) {
    uint8_t* element = NULL;
    if (argc == 2) {
        switch (*argv[1]) {
            case '0':
                element = pubKey0_hash;
                break;
            case '1':
                element = pubKey1_hash;
                break;
            case '2':
                element = pubKey2_hash;
                break;
            case '3':
                element = pubKey3_hash;
                break;
            case '4':
                element = pubKey4_hash;
                break;
            case '5':
                element = rootPubKey_hash;
                break;
            case '6':
                element = signerPubKey_hash;
                break;
            case '7':
                element = devicePubKey_hash;
                break;
            case '8':
                element = rootCert_hash;
                break;
            case '9':
                element = signerCert_hash;
                break;
            case 'A':
                element = deviceCert_hash;
                break;
            default:
                break;
        }
    }
    if (NULL != element) {
        for (int i = 0; i < SHA256_DIGEST_SIZE; i++) {
            SYS_CONSOLE_PRINT("%02x ", element[i]);
        }
    }
    SYS_CONSOLE_PRINT("\r\n");
}

#if 0
void _APP_Commands_GetSize(SYS_CMD_DEVICE_NODE* pCmdIO, int argc, char** argv) {
    size_t retSize = 0;
    if (argc == 2) {
        switch (*argv[1]) {
            case '0':
                status = tng_atcacert_root_cert_size(&rootCertSize);
                if (ATCA_SUCCESS == status) {
                    retSize = rootCertSize;
                }
                break;
            case '1':
                status = tng_atcacert_max_signer_cert_size(&signerCertSize);
                if (ATCA_SUCCESS == status) {
                    uint8_t signerCert[signerCertSize];
                    status = tng_atcacert_read_signer_cert((uint8_t*) & signerCert, &signerCertSize);
                    if (ATCA_SUCCESS == status) {
                        retSize = signerCertSize;
                    }
                }
                break;
            case '2':
                status = tng_atcacert_max_signer_cert_size(&signerCertSize);
                if (ATCA_SUCCESS == status) {
                    uint8_t signerCert[signerCertSize];
                    status = tng_atcacert_read_signer_cert((uint8_t*) & signerCert, &signerCertSize);
                    if (ATCA_SUCCESS == status) {
                        status = tng_atcacert_max_device_cert_size(&deviceCertSize);
                        if (ATCA_SUCCESS == status) {
                            uint8_t deviceCert[deviceCertSize];
                            status = tng_atcacert_read_device_cert((uint8_t*) & deviceCert, &deviceCertSize, (uint8_t*) & signerCert);
                            if (ATCA_SUCCESS == status) {
                                retSize = deviceCertSize;
                            }
                        }
                    }
                }
                break;
            default:
                break;
        }
        SYS_CONSOLE_PRINT("%02x\r\n", retSize);
    }
}
#endif 

void _APP_Commands_GetCert(SYS_CMD_DEVICE_NODE* pCmdIO, int argc, char** argv) {
    uint8_t *element = 0;
    size_t elemSize = 0;
    size_t rootCertSize = 0;
    size_t signerCertSize = 0;
    size_t deviceCertSize = 0;
    uint8_t *rootCert=NULL;
    uint8_t *signerCert=NULL;
    uint8_t *deviceCert=NULL;
    
    if (argc == 2) {
        switch (*argv[1]) {
            case '0':
                status = tng_atcacert_root_cert_size(&rootCertSize);
                if (ATCA_SUCCESS == status) {
                    rootCert=(uint8_t*)malloc(rootCertSize);
                    status = tng_atcacert_root_cert(rootCert, &rootCertSize);
                    if (ATCA_SUCCESS == status) {
                        atcah_sha256(rootCertSize, rootCert, rootCert_hash);
                        element = rootCert;
                        elemSize = rootCertSize;
                    }
                }
                break;
            case '1':
                status = tng_atcacert_max_signer_cert_size(&signerCertSize);
                if (ATCA_SUCCESS == status) {
                    signerCert=(uint8_t*)malloc(signerCertSize);
                    status = tng_atcacert_read_signer_cert(signerCert, &signerCertSize);
                    if (ATCA_SUCCESS == status) {
                        atcah_sha256(signerCertSize, signerCert, signerCert_hash);
                        element = signerCert;
                        elemSize = signerCertSize;
                    }
                }
                break;
            case '2':
                /*Read signer cert*/
                status = tng_atcacert_max_signer_cert_size(&signerCertSize);
                if (ATCA_SUCCESS == status) {
                    signerCert=(uint8_t*)malloc(signerCertSize);
                    status = tng_atcacert_read_signer_cert(signerCert, &signerCertSize);
                    if (ATCA_SUCCESS == status) {
                        status = tng_atcacert_max_device_cert_size(&deviceCertSize);
                        if (ATCA_SUCCESS == status) {
                            deviceCert=(uint8_t*)malloc(deviceCertSize);
                            status = tng_atcacert_read_device_cert(deviceCert, &deviceCertSize, signerCert);
                            if (ATCA_SUCCESS == status) {
                                atcah_sha256(deviceCertSize, deviceCert, deviceCert_hash);
                                element = deviceCert;
                                elemSize = deviceCertSize;
                            }
                        }
                    }
                }
                break;
            default:
                break;
        }
        for (int i = 0; i < elemSize; i++) {
            SYS_CONSOLE_PRINT("%02x ", element[i]);
        }
        SYS_CONSOLE_PRINT("\r\n");
        free(rootCert);
        free(signerCert);
        free(deviceCert);
    }
}


static const SYS_CMD_DESCRIPTOR appCmdTbl[] = {
    {"getstat", _APP_Commands_GetStatus, ": get Status"},
    {"getserial", _APP_Commands_GetSerial, ": get Serial"},
    {"getkey", _APP_Commands_GetKey, ": get parameter key"},
    {"gethash", _APP_Commands_GetHash, ": get parameter hash"},
    //{"getsize", _APP_Commands_GetSize, ": get cert size"},
    {"getcert", _APP_Commands_GetCert, ": get cert"},
};

bool APP_Commands_Init() {
    if (!SYS_CMD_ADDGRP(appCmdTbl, sizeof (appCmdTbl) / sizeof (*appCmdTbl), "app", ": app commands")) {
        SYS_ERROR(SYS_ERROR_ERROR, "Failed to create Commands\r\n", 0);
        return false;
    }
    return true;
}

void APP_Initialize(void) {
    /* Place the App state machine in its initial state. */
    APP_Commands_Init();
    appData.state = APP_STATE_INIT;
}

void APP_Tasks(void) {
    status = ATCA_TX_FAIL;
    /* Check the application's current state. */
    switch (appData.state) {
            /* Application's initial state. */
        case APP_STATE_INIT:
        {
            status = atcab_init(&atecc608_0_init_data);
            if (ATCA_SUCCESS == status) {
                status = atcab_read_serial_number(sernum);
                status = atcab_bin2hex(sernum, 9, displayStr, &displen);
                stat = true;
                appData.state = APP_STATE_SERVICE_TASKS;
            } else {
                SYS_CONSOLE_PRINT("Failed to initialize atcab\r\n");
                stat = false;
                appData.state = APP_STATE_ERROR;
            }
            break;
        }
        case APP_STATE_SERVICE_TASKS:
        {
            break;
        }
        case APP_STATE_ERROR:
        {
            break;
        }
            /* The default state should never be executed. */
        default:
        {
            /* TODO: Handle error in application's state machine. */
            break;
        }
    }
}


/*******************************************************************************
 End of File
 */
