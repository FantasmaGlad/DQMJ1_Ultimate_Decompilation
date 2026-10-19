#ifndef GAME_SCRIPT_H
#define GAME_SCRIPT_H

#include "../types.h"

/*
 * Event Script VM Opcodes (.evt binary format)
 * Decoded through tools/evt_vm.py and cutscene disassembly
 */
#define EVT_OP_NOP              0x00
#define EVT_OP_END              0x01
#define EVT_OP_WAIT             0x02
#define EVT_OP_JUMP             0x04
#define EVT_OP_JUMP_IF          0x05
#define EVT_OP_SET_FLAG         0x0A
#define EVT_OP_CLEAR_FLAG       0x0B
#define EVT_OP_CHECK_FLAG       0x0C
#define EVT_OP_DIALOGUE_SHOW    0x1A
#define EVT_OP_CAMERA_SPLINE    0x24
#define EVT_OP_ACTOR_SPAWN      0x30
#define EVT_OP_ACTOR_ANIMATE    0x35
#define EVT_OP_CHEST_SPAWN      0x5F  /* Spawns 3D chest with item ID at coordinates */
#define EVT_OP_BATTLE_START     0x72
#define EVT_OP_BGM_PLAY         0x80
#define EVT_OP_SFX_PLAY         0x85

/*
 * Event VM execution context
 */
typedef struct {
    const u8 *bytecode_ptr;
    u32       program_counter;
    u16       wait_frames;
    u8        is_active;
    u8        halt_requested;
    u32       variables[16];
} EventVmContext;

#endif /* GAME_SCRIPT_H */
