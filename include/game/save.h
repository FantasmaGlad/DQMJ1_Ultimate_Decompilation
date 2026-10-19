#ifndef GAME_SAVE_H
#define GAME_SAVE_H

#include "../types.h"

/*
 * Save block header format
 * Verified across 512 KB EEPROM saves (Slot 1 & Slot 2 backup)
 */
typedef struct {
    u32 magic_header;           /* Magic constant ('DQMJ' = 0x4A4D5144) */
    u32 save_counter;           /* Incremented on each successful save */
    u32 payload_length;         /* Length of serialized data following header */
    u16 checksum_crc16;         /* CRC16-CCITT computed over payload */
    u16 format_version;         /* Save format revision */
} ALIGN(4) SaveBlockHeader;

/*
 * Calculates standard CCITT CRC16 for save integrity validation.
 *
 * @param buffer Input byte array
 * @param length Byte count
 * @return 16-bit CRC checksum
 */
u16 save_calculate_crc16(const u8 *buffer, u32 length);

/*
 * Validates a save data block against its embedded checksum.
 */
BOOL save_verify_integrity(const u8 *save_buffer, u32 total_size);

#endif /* GAME_SAVE_H */
