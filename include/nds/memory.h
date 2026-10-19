#ifndef NDS_MEMORY_H
#define NDS_MEMORY_H

/*
 * Nintendo DS Memory Map Layout
 * Verified against NTR-AJRP-EUR cartridge ROM header and manifest.json
 */

#define HW_ITCM_BASE            0x01FF8000  /* Instruction TCM (ARM9, 32 KB) */
#define HW_MAIN_RAM_BASE        0x02000000  /* Main RAM Base (arm9.bin executable) */
#define HW_MAIN_RAM_END         0x023FFFFF  /* Main RAM End (4 MB total) */
#define HW_OVERLAY_BASE         0x02184B40  /* Dynamic Overlay Load Address (0000, 0001, 0002) */
#define HW_ARM7_RAM_BASE        0x02380000  /* ARM7 Subsystem Base (arm7.bin) */
#define HW_DTCM_BASE            0x027E0000  /* Data TCM (ARM9, 16 KB) */
#define HW_SHARED_WRAM_BASE     0x037F8000  /* Shared WRAM (ARM9/ARM7, 32 KB) */
#define HW_IO_REG_BASE          0x04000000  /* Memory Mapped I/O Registers */
#define HW_VRAM_BASE            0x06800000  /* Video RAM (656 KB total across banks A-I) */
#define HW_ROM_CART_BASE        0x08000000  /* Cartridge ROM Space */

#endif /* NDS_MEMORY_H */
