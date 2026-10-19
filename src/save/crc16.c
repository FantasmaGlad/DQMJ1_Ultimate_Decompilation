#include "game/save.h"

/*
 * Standard CCITT CRC16 implementation used by Nintendo DS save blocks
 * Polynomial: 0x1021 (x^16 + x^12 + x^5 + 1), Initial value: 0xFFFF
 */
u16 save_calculate_crc16(const u8 *buffer, u32 length) {
    u16 crc = 0xFFFF;
    u32 i;
    u32 j;

    if (buffer == NULL || length == 0) {
        return 0;
    }

    for (i = 0; i < length; i++) {
        crc ^= (u16)((u16)buffer[i] << 8);
        for (j = 0; j < 8; j++) {
            if (crc & 0x8000) {
                crc = (u16)((crc << 1) ^ 0x1021);
            } else {
                crc <<= 1;
            }
        }
    }

    return crc;
}

BOOL save_verify_integrity(const u8 *save_buffer, u32 total_size) {
    const SaveBlockHeader *header;
    u16 computed_crc;

    if (save_buffer == NULL || total_size < sizeof(SaveBlockHeader)) {
        return FALSE;
    }

    header = (const SaveBlockHeader *)save_buffer;

    /* Verify Magic 'DQMJ' = 0x4A4D5144 (little-endian) */
    if (header->magic_header != 0x4A4D5144) {
        return FALSE;
    }

    /* Compute CRC over payload following header */
    if (total_size < sizeof(SaveBlockHeader) + header->payload_length) {
        return FALSE;
    }

    computed_crc = save_calculate_crc16(save_buffer + sizeof(SaveBlockHeader), header->payload_length);
    return (computed_crc == header->checksum_crc16);
}
