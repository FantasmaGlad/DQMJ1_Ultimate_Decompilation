// ============================================================
// Module   : arm7_t
// Programme: arm7.bin
// Langage  : ARM:LE:32:v4t
// Base     : 00000000
// ============================================================
// Code pseudo-C issu du decompileur Ghidra.
// Les noms sont automatiques (FUN_xxxx, DAT_xxxx, LAB_xxxx) :
// les renommer est notre travail.

// ---- FUN_023801b0 @ 023801b0 ----

void FUN_023801b0(void)

{
  ushort uVar1;
  bool bVar2;
  undefined2 uVar3;
  uint uVar4;
  uint uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  int iVar8;
  int iVar9;
  ushort *puVar10;
  undefined4 in_r3;
  uint uVar11;
  uint uVar12;
  undefined2 auStack_324 [11];
  byte abStack_30e [54];
  byte abStack_2d8 [160];
  byte local_238 [2];
  ushort local_236;
  int local_234;
  undefined1 auStack_230 [8];
  undefined1 auStack_228 [100];
  ushort local_1c4 [8];
  byte abStack_1b4 [2];
  ushort local_1b2 [69];
  undefined1 auStack_128 [112];
  ushort local_b8;
  undefined4 uStack_28;
  
  uStack_28 = in_r3;
  FUN_02384adc();
  FUN_0238406c();
  func_0x0137d5bc(0x20,2,&local_234);
  local_234 = local_234 << 3;
  func_0x0137d5bc(local_234,0x100,auStack_228);
  func_0x0137d5bc(local_234 + 0x100,0x100,auStack_128);
  uVar11 = 0;
  func_0x0137d5bc(0x1d,1,local_238);
  if (local_238[0] == 0xff) {
    bVar2 = false;
  }
  else if ((local_238[0] & 0x50) == 0) {
    bVar2 = false;
  }
  else {
    bVar2 = true;
  }
  if (bVar2) {
    uVar4 = FUN_02380634();
    for (uVar12 = 0; uVar12 < 2; uVar12 = uVar12 + 1 & 0xffff) {
      iVar8 = uVar12 * 0x100;
      uVar5 = thunk_EXT_FUN_038035a0(DAT_02380604,auStack_228 + iVar8,0x70);
      if (((uVar5 == *(ushort *)(abStack_1b4 + iVar8 + -2)) && (local_1c4[uVar12 * 0x80 + 6] < 0x80)
          ) && (uVar5 = thunk_EXT_FUN_038035a0(DAT_02380604,abStack_1b4 + iVar8,0x8a),
               uVar5 == *(ushort *)(auStack_128 + iVar8 + -2))) {
        if (((uint)local_1b2[uVar12 * 0x80] & 1 << (ushort)abStack_1b4[iVar8 + 1]) != 0) {
          if ((uVar4 & local_1b2[uVar12 * 0x80]) != 0) {
            local_1c4[uVar12 * 0x80] =
                 local_1c4[uVar12 * 0x80] & 0xfff8 | abStack_1b4[iVar8 + 1] & 7;
          }
          if ((uVar4 & 0x40 & ~(uint)local_1b2[uVar12 * 0x80]) != 0) {
            uVar11 = 3;
            goto LAB_023803a0;
          }
          uVar11 = uVar11 | 1 << (uVar12 & 0xff);
        }
      }
    }
  }
  else {
    uVar12 = FUN_02380634();
    uVar6 = DAT_02380604;
    if ((uVar12 & 0x40) != 0) {
      uVar11 = 3;
      goto LAB_023803a0;
    }
    uVar12 = 0;
    do {
      uVar4 = thunk_EXT_FUN_038035a0(uVar6,auStack_228 + uVar12 * 0x100,0x70);
      if ((uVar4 == *(ushort *)(abStack_1b4 + uVar12 * 0x100 + -2)) &&
         (local_1c4[uVar12 * 0x80 + 6] < 0x80)) {
        uVar11 = uVar11 | 1 << (uVar12 & 0xff);
      }
      uVar12 = uVar12 + 1 & 0xffff;
    } while (uVar12 < 2);
  }
  if (uVar11 != 1 && uVar11 != 2) {
    if (uVar11 == 3) {
      if ((local_1c4[6] + 1 & 0x7f) == local_b8) {
        uVar11 = 2;
      }
      else {
        uVar11 = 1;
      }
    }
    else {
      uVar11 = 0;
    }
  }
LAB_023803a0:
  if ((int)uVar11 < 3) {
    if (uVar11 == 0) {
      FUN_023860ac(0,DAT_02380608,0x74);
    }
    else {
      if (local_238[uVar11 * 0x100 + DAT_0238060c] < 10) {
        for (iVar8 = 10; (int)(uint)abStack_30e[uVar11 * 0x100] < iVar8; iVar8 = iVar8 + -1) {
          auStack_324[uVar11 * 0x80 + iVar8] = 0;
        }
      }
      if (local_238[uVar11 * 0x100 + DAT_02380610] < 0x1a) {
        for (iVar8 = 0x1a; (int)(uint)abStack_2d8[uVar11 * 0x100] < iVar8; iVar8 = iVar8 + -1) {
          (abStack_30e + iVar8 * 2 + uVar11 * 0x100)[0] = 0;
          (abStack_30e + iVar8 * 2 + uVar11 * 0x100)[1] = 0;
        }
      }
      FUN_023860c0(auStack_228 + (uVar11 - 1) * 0x100,DAT_02380608,0x74);
    }
  }
  else {
    FUN_023860ac(0xffffffff,DAT_02380608,0x74);
  }
  func_0x0137d5bc(0x36,6,auStack_230);
  iVar8 = DAT_02380608;
  FUN_023861b8(auStack_230,DAT_02380608 + 0x74,6);
  func_0x0137d5bc(0x3c,2,&local_236);
  uVar3 = FUN_0238f0d4(local_236 >> 1);
  *(undefined2 *)(iVar8 + 0x7a) = uVar3;
  thunk_EXT_FUN_037fe14c();
  uVar6 = FUN_02384b84(8);
  uVar7 = FUN_02384b98(8);
  iVar8 = FUN_02384f14(8,uVar7,uVar6,1);
  iVar9 = FUN_02384b84(8);
  FUN_02386124(iVar8,0,iVar9 - iVar8);
  FUN_02384c80(8,iVar8);
  uVar6 = FUN_02384b84(8);
  uVar7 = FUN_02384b98(8);
  iVar8 = FUN_02384fbc(8,uVar7,uVar6);
  if (iVar8 < 0) {
    FUN_02385f74();
  }
  FUN_02384ee0(8,iVar8);
  uVar11 = FUN_0238505c(8,iVar8);
  if (uVar11 < 0x2100) {
    FUN_02385f74();
  }
  FUN_02386f34(6);
  FUN_023865fc();
  FUN_02383934(1,DAT_02380614);
  FUN_02383a68(1);
  puVar10 = DAT_02380618 + 0x102;
  *DAT_02380618 = *DAT_02380618 | 8;
  uVar1 = *puVar10;
  *puVar10 = 1;
  FUN_02385df0(1,uVar1);
  thunk_EXT_FUN_03802f8c(0xffffffff);
  FUN_0238a71c(0xf);
  func_0x0137dcc8(0xc);
  FUN_0238d188(iVar8);
  FUN_0238b7c0(2);
  do {
    thunk_EXT_FUN_0380356e();
    iVar8 = FUN_02385eb8();
    if (iVar8 != 0) {
      FUN_0238e310(0);
      FUN_02385efc();
    }
    FUN_0238e548();
    FUN_0238b608();
  } while( true );
}



// ---- thunk_EXT_FUN_038035a0 @ 0238061c ----

void thunk_EXT_FUN_038035a0(void)

{
                    /* WARNING: Could not recover jumptable at 0x02380620. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02380624)();
  return;
}



// ---- thunk_EXT_FUN_0380356e @ 02380628 ----

void thunk_EXT_FUN_0380356e(void)

{
                    /* WARNING: Could not recover jumptable at 0x0238062c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02380630)();
  return;
}



// ---- FUN_02380634 @ 02380634 ----

undefined4 FUN_02380634(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if (*DAT_02380668 != -0x80) {
    if (*DAT_02380668 == '@') {
      uVar1 = 0x80;
    }
    return uVar1;
  }
  return 0x40;
}



// ---- FUN_02380748 @ 02380748 ----

void FUN_02380748(int param_1,int param_2)

{
  undefined2 uVar1;
  int iVar2;
  uint uVar3;
  int iVar4;
  
  iVar4 = *DAT_023807f8;
  FUN_02383aa0(DAT_023807fc);
  iVar2 = iVar4 + 0xbc + param_2 * 8;
  if (*(short *)(iVar2 + 2) == 0) {
    *(undefined2 *)(iVar2 + 2) = 1;
    *(undefined2 *)(iVar4 + 0xbc + param_2 * 8) = 0xffff;
    uVar3 = (uint)*(ushort *)(iVar4 + param_1 * 2 + 8);
    uVar1 = (undefined2)param_2;
    if (uVar3 == 0xffff) {
      *(undefined2 *)(iVar4 + param_1 * 2) = uVar1;
    }
    else {
      *(undefined2 *)(iVar4 + uVar3 * 8 + 0xbc) = uVar1;
    }
    *(undefined2 *)(iVar4 + param_1 * 2 + 8) = uVar1;
    if (param_1 < (int)(uint)*(ushort *)(iVar4 + 0x10)) {
      *(short *)(iVar4 + 0x10) = (short)param_1;
    }
  }
  FUN_02383a68();
  if ((param_1 != 3) && (*(short *)(iVar4 + 0x12) == 3)) {
    FUN_023847c4(*(undefined4 *)(*DAT_023807f8 + 0x308),0,0);
  }
  return;
}



// ---- FUN_0238095c @ 0238095c ----

undefined4 FUN_0238095c(int *param_1,int *param_2)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  int iVar3;
  
  if (*(ushort *)((int)param_2 + 10) == DAT_02380a18) {
    if ((short)param_2[2] == *(short *)((int)param_1 + 10)) {
      FUN_02383aa0(0x1000000);
      *(short *)(param_1 + 2) = (short)param_1[2] + -1;
      if ((short)param_1[2] == 0) {
        *param_1 = -1;
        param_1[1] = -1;
      }
      else if (param_2 == (int *)*param_1) {
        puVar2 = (undefined4 *)param_2[1];
        *param_1 = (int)puVar2;
        *puVar2 = 0xffffffff;
      }
      else {
        iVar3 = *param_2;
        if (param_2 == (int *)param_1[1]) {
          param_1[1] = iVar3;
          *(undefined4 *)(iVar3 + 4) = 0xffffffff;
        }
        else {
          *(int *)param_2[1] = iVar3;
          *(int *)(*param_2 + 4) = param_2[1];
        }
      }
      *(undefined2 *)(param_2 + 2) = 0;
      FUN_02383a68();
      uVar1 = 0;
    }
    else {
      uVar1 = 2;
    }
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}



// ---- FUN_02380b38 @ 02380b38 ----

int FUN_02380b38(undefined4 param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 uVar2;
  
  if (*(ushort *)(param_3 + 10) == DAT_02380ba0) {
    uVar2 = FUN_02383aa0(0x1000000);
    iVar1 = FUN_0238095c(param_1,param_3);
    if (iVar1 == 0) {
      iVar1 = FUN_02380ba4(param_2,param_3);
    }
    FUN_02383a68(uVar2);
  }
  else {
    iVar1 = 1;
  }
  return iVar1;
}



// ---- FUN_02380ba4 @ 02380ba4 ----

undefined4 FUN_02380ba4(undefined4 *param_1,int *param_2)

{
  undefined4 uVar1;
  int iVar2;
  
  if (*(ushort *)((int)param_2 + 10) == DAT_02380c2c) {
    if ((short)param_2[2] == 0) {
      FUN_02383aa0(0x1000000);
      if (*(short *)(param_1 + 2) == 0) {
        *param_2 = -1;
        *param_1 = param_2;
      }
      else {
        iVar2 = param_1[1];
        *param_2 = iVar2;
        *(int **)(iVar2 + 4) = param_2;
      }
      param_2[1] = -1;
      *(undefined2 *)(param_2 + 2) = *(undefined2 *)((int)param_1 + 10);
      param_1[1] = param_2;
      *(short *)(param_1 + 2) = *(short *)(param_1 + 2) + 1;
      FUN_02383a68();
      uVar1 = 0;
    }
    else {
      uVar1 = 2;
    }
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}



// ---- FUN_02380c38 @ 02380c38 ----

void FUN_02380c38(undefined4 param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  undefined2 uVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  code *pcVar7;
  ushort uVar8;
  int iVar9;
  ushort uVar10;
  uint uVar11;
  uint uVar12;
  bool bVar13;
  
  piVar1 = DAT_02380ee8;
  uVar8 = 0;
  iVar4 = *DAT_02380ee8;
  uVar10 = 0;
  if (*(short *)(iVar4 + 0x428) != 0) {
    return;
  }
  iVar3 = *(int *)(iVar4 + 0x200);
  *(int *)(iVar4 + 0x424) = iVar3;
  if (iVar3 == -1) {
    return;
  }
  iVar5 = *piVar1;
  iVar9 = iVar3 + (uint)*(ushort *)(iVar3 + 0xe) * 2;
  if (*(short *)(iVar5 + 0x33e) == 0) {
    uVar11 = (uint)*(ushort *)(iVar3 + 0xc);
    if (uVar11 == *(ushort *)(iVar9 + 0x10)) {
      uVar6 = uVar11 & 0xff00;
      if (uVar6 < 0x101) {
        if (uVar6 < 0x100) {
          if ((*(ushort *)(iVar3 + 0xc) & 0xff00) != 0) goto LAB_02380e00;
          uVar11 = uVar11 & 0xff;
          uVar10 = 1;
          uVar6 = 0xb;
          param_2 = DAT_02380eec;
          if ((*(ushort *)(iVar4 + 0x428) & 1) == 0) {
            uVar8 = (ushort)(*(ushort *)(iVar5 + 0x34c) < 0x20);
          }
          else {
            uVar8 = 2;
          }
        }
        else {
          uVar11 = uVar11 & 0xff;
          uVar10 = 2;
          uVar6 = 5;
          uVar8 = (ushort)(*(short *)(iVar5 + 0x34c) != 0x40);
          param_2 = DAT_02380ef0;
        }
      }
      else if (uVar6 < 0x201) {
        if (uVar6 == 0x200) {
          uVar11 = uVar11 & 0xff;
          if (uVar11 < 0x40) {
            uVar10 = 4;
            uVar8 = (ushort)(*(ushort *)(iVar5 + 0x34c) < 0x10);
            uVar6 = 0x17;
            param_2 = DAT_02380ef4;
          }
          else if (uVar11 < 0x80) {
            uVar10 = 8;
            uVar8 = (ushort)(*(short *)(iVar5 + 0x34c) != 0x40);
            uVar11 = uVar11 - 0x40 & 0xffff;
            uVar6 = 6;
            param_2 = DAT_02380ef8;
          }
          else if (uVar11 < 0xc0) {
            uVar8 = (ushort)(*(ushort *)(iVar5 + 0x34c) < 0x10);
            uVar11 = uVar11 - 0x80 & 0xffff;
            uVar10 = 0x10;
            uVar6 = 0x17;
            param_2 = DAT_02380efc;
          }
          else {
            uVar8 = (ushort)(*(ushort *)(iVar5 + 0x34c) < 0x10);
            uVar11 = uVar11 - 0xc0 & 0xffff;
            uVar10 = 0x20;
            uVar6 = 6;
            param_2 = DAT_02380f00;
          }
        }
        else {
LAB_02380e00:
          uVar11 = 1;
          uVar6 = 0;
          uVar10 = 0;
        }
      }
      else {
        if (uVar6 != 0x300) goto LAB_02380e00;
        uVar11 = uVar11 & 0xff;
        uVar10 = 0x40;
        uVar6 = 0xb;
        param_2 = DAT_02380f04;
      }
      if (uVar6 < uVar11) {
        uVar8 = 3;
      }
      else {
        uVar6 = uVar11 * 8;
        uVar12 = (uint)*(ushort *)(param_2 + uVar6);
        bVar13 = uVar12 <= *(ushort *)(iVar3 + 0xe);
        if (bVar13) {
          iVar5 = param_2 + uVar6;
          uVar6 = (uint)*(ushort *)(iVar9 + 0x12);
          uVar12 = (uint)*(ushort *)(iVar5 + 2);
        }
        if (!bVar13 || uVar6 < uVar12) {
          uVar8 = 4;
        }
      }
      if (uVar8 == 0) {
        uVar8 = *(ushort *)(iVar4 + 0x428);
        *(ushort *)(iVar4 + 0x428) = uVar8 | uVar10;
        pcVar7 = *(code **)(param_2 + uVar11 * 8 + 4);
        uVar2 = (*pcVar7)(iVar3,iVar9 + 0x10,pcVar7,uVar8,param_4);
        *(undefined2 *)(iVar9 + 0x14) = uVar2;
        if (*(short *)(iVar9 + 0x14) == 0x80) {
          return;
        }
        if (*(short *)(iVar9 + 0x14) == 0x81) {
          *(ushort *)(iVar4 + 0x428) = *(ushort *)(iVar4 + 0x428) & ~uVar10;
          goto LAB_02380ebc;
        }
      }
      else {
        *(undefined2 *)(iVar9 + 0x12) = 1;
        *(ushort *)(iVar9 + 0x14) = uVar8;
      }
    }
    else {
      *(undefined2 *)(iVar9 + 0x14) = 0xd;
    }
  }
  else {
    *(undefined2 *)(iVar9 + 0x12) = 1;
    *(undefined2 *)(iVar9 + 0x14) = 6;
  }
  *(ushort *)(iVar4 + 0x428) = *(ushort *)(iVar4 + 0x428) & ~uVar10;
  FUN_02380f08(*DAT_02380ee8 + 0x200,*(int *)(iVar4 + 0x424));
LAB_02380ebc:
  if (*(short *)(*DAT_02380ee8 + 0x208) != 0) {
    FUN_02380748(2,0xb);
  }
  return;
}



// ---- FUN_02380f08 @ 02380f08 ----

void FUN_02380f08(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  
  iVar1 = *DAT_02380f8c;
  if (*(short *)(iVar1 + 0x1fc) == 0) {
    iVar1 = FUN_023847c4(*(undefined4 *)(iVar1 + 0x304),param_2,0,iVar1,param_4);
    if (iVar1 == 0) {
      FUN_02380b38(param_1,*DAT_02380f8c + 500,param_2);
    }
    else {
      FUN_0238095c(param_1,param_2);
    }
  }
  else {
    FUN_02380b38(param_1,iVar1 + 500,param_2);
    FUN_02380748(2,0x13);
  }
  return;
}



// ---- FUN_023837b4 @ 023837b4 ----

void FUN_023837b4(int param_1)

{
  uint uVar1;
  ushort uVar2;
  int iVar3;
  code *pcVar4;
  int iVar5;
  
  iVar5 = param_1 * 0xc;
  pcVar4 = *(code **)(DAT_0238382c + iVar5);
  uVar2 = *(ushort *)(DAT_02383830 + param_1 * 2);
  *(undefined4 *)(DAT_0238382c + iVar5) = 0;
  uVar1 = 1 << (uVar2 & 0xff);
  if (pcVar4 != (code *)0x0) {
    (*pcVar4)(*(undefined4 *)(DAT_02383834 + iVar5));
  }
  iVar3 = DAT_0238383c;
  *DAT_02383838 = *DAT_02383838 | uVar1;
  if (*(int *)(iVar3 + iVar5) == 0) {
    FUN_02383aa0(uVar1);
  }
  return;
}



// ---- FUN_02383910 @ 02383910 ----

void FUN_02383910(void)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  
  puVar1 = DAT_0238392c;
  DAT_0238392c[1] = 0;
  puVar2 = DAT_02383930;
  *puVar1 = 0;
  *puVar2 = 0;
  return;
}



// ---- FUN_02383934 @ 02383934 ----

void FUN_02383934(uint param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  int iVar4;
  undefined4 *puVar5;
  
  iVar3 = DAT_023839cc;
  puVar2 = DAT_023839c8;
  iVar1 = DAT_023839c4;
  iVar4 = 0;
  do {
    if ((param_1 & 1) != 0) {
      if ((iVar4 < 8) || (0xb < iVar4)) {
        if ((iVar4 < 3) || (6 < iVar4)) {
          puVar5 = puVar2;
          if (iVar4 != 0) {
            *(undefined4 *)(iVar1 + iVar4 * 4) = param_2;
            puVar5 = (undefined4 *)0x0;
          }
        }
        else {
          puVar5 = (undefined4 *)((iVar4 + 1) * 0xc + iVar3);
        }
      }
      else {
        puVar5 = (undefined4 *)((iVar4 + -8) * 0xc + iVar3);
      }
      if (puVar5 != (undefined4 *)0x0) {
        *puVar5 = param_2;
        puVar5[1] = 1;
        puVar5[2] = 0;
      }
    }
    iVar4 = iVar4 + 1;
    param_1 = param_1 >> 1;
  } while (iVar4 < 0x19);
  return;
}



// ---- FUN_023839d0 @ 023839d0 ----

void FUN_023839d0(int param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  int iVar2;
  
  iVar1 = DAT_02383a14;
  iVar2 = param_1 * 0xc;
  *(undefined4 *)(DAT_02383a10 + iVar2) = param_2;
  *(undefined4 *)(iVar1 + iVar2) = param_3;
  FUN_02383a68(1 << (param_1 + 3U & 0xff));
  *(undefined4 *)(DAT_02383a18 + iVar2) = 1;
  return;
}



// ---- FUN_02383a1c @ 02383a1c ----

ulonglong FUN_02383a1c(undefined4 param_1)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  
  uVar2 = FUN_02383a50();
  uVar4 = *DAT_02383a4c;
  puVar3 = DAT_02383a4c + -2;
  *DAT_02383a4c = param_1;
  uVar1 = *(undefined2 *)puVar3;
  *(undefined2 *)puVar3 = uVar2;
  return (ulonglong)CONCAT24(uVar1,uVar4);
}



// ---- FUN_02383a50 @ 02383a50 ----

undefined2 FUN_02383a50(void)

{
  undefined2 uVar1;
  
  uVar1 = *DAT_02383a64;
  *DAT_02383a64 = 0;
  return uVar1;
}



// ---- FUN_02383a68 @ 02383a68 ----

ulonglong FUN_02383a68(uint param_1)

{
  uint uVar1;
  undefined2 uVar2;
  uint *puVar3;
  uint uVar4;
  
  uVar2 = FUN_02383a50();
  uVar4 = *DAT_02383a9c;
  puVar3 = DAT_02383a9c + -2;
  *DAT_02383a9c = uVar4 | param_1;
  uVar1 = *puVar3;
  *(undefined2 *)puVar3 = uVar2;
  return (ulonglong)CONCAT24((short)uVar1,uVar4);
}



// ---- FUN_02383aa0 @ 02383aa0 ----

ulonglong FUN_02383aa0(uint param_1)

{
  uint uVar1;
  undefined2 uVar2;
  uint *puVar3;
  uint uVar4;
  
  uVar2 = FUN_02383a50();
  uVar4 = *DAT_02383ad8;
  puVar3 = DAT_02383ad8 + -2;
  *DAT_02383ad8 = uVar4 & ~param_1;
  uVar1 = *puVar3;
  *(undefined2 *)puVar3 = uVar2;
  return (ulonglong)CONCAT24((short)uVar1,uVar4);
}



// ---- FUN_02383adc @ 02383adc ----

ulonglong FUN_02383adc(undefined4 param_1)

{
  undefined2 uVar1;
  undefined2 uVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  
  uVar2 = FUN_02383a50();
  uVar4 = *DAT_02383b0c;
  puVar3 = DAT_02383b0c + -3;
  *DAT_02383b0c = param_1;
  uVar1 = *(undefined2 *)puVar3;
  *(undefined2 *)puVar3 = uVar2;
  return (ulonglong)CONCAT24(uVar1,uVar4);
}



// ---- FUN_02383b10 @ 02383b10 ----

void FUN_02383b10(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  iVar1 = DAT_02383b7c;
  if (*DAT_02383b78 == 0) {
    *DAT_02383b78 = 1;
    *(undefined2 *)(iVar1 + 6) = 0;
    while (puVar2 = DAT_02383b80, *(short *)(iVar1 + 4) != 0x7f) {
      thunk_EXT_FUN_03803554(0x400);
    }
    *DAT_02383b80 = 0xffffffff;
    puVar2[1] = 0xffff0000;
    *(undefined2 *)(iVar1 + 6) = 0xbf;
  }
  return;
}



// ---- thunk_EXT_FUN_03803554 @ 02383b84 ----

void thunk_EXT_FUN_03803554(void)

{
                    /* WARNING: Could not recover jumptable at 0x02383b88. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02383b8c)();
  return;
}



// ---- FUN_02383c0c @ 02383c0c ----

int FUN_02383c0c(undefined4 param_1,int param_2,code *param_3,int param_4)

{
  undefined4 uVar1;
  int iVar2;
  
  if (param_4 == 0) {
    uVar1 = FUN_02385e04();
  }
  else {
    uVar1 = FUN_02385e30();
  }
  iVar2 = FUN_023862e8(param_1,param_2);
  if (iVar2 == 0) {
    if (param_3 != (code *)0x0) {
      (*param_3)();
    }
    *(short *)(param_2 + 4) = (short)param_1;
  }
  if (param_4 == 0) {
    FUN_02385e18(uVar1);
  }
  else {
    FUN_02385e44();
  }
  return iVar2;
}



// ---- FUN_02383c80 @ 02383c80 ----

void FUN_02383c80(undefined4 param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  
  uVar2 = DAT_02383ccc;
  uVar1 = DAT_02383cc8;
  while (iVar3 = FUN_02383c0c(param_1,uVar1,uVar2,1), 0 < iVar3) {
    thunk_EXT_FUN_03803554(0x400);
  }
  return;
}



// ---- FUN_02383cd0 @ 02383cd0 ----

void FUN_02383cd0(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02383ce0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02383ce4)(param_1,DAT_02383ce8,DAT_02383cec,1);
  return;
}



// ---- thunk_EXT_FUN_037fbb20 @ 02383cf0 ----

void thunk_EXT_FUN_037fbb20(void)

{
                    /* WARNING: Could not recover jumptable at 0x02383cf4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02383cf8)();
  return;
}



// ---- FUN_02383cfc @ 02383cfc ----

void FUN_02383cfc(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02383d0c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02383d10)(param_1,DAT_02383d14,DAT_02383d18,1);
  return;
}



// ---- FUN_02383d24 @ 02383d24 ----

undefined2 FUN_02383d24(int param_1)

{
  return *(undefined2 *)(param_1 + 4);
}



// ---- FUN_02383d2c @ 02383d2c ----

int FUN_02383d2c(void)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  uint *puVar4;
  
  uVar3 = 0;
  uVar1 = 0x80000000;
  while (((*DAT_02383dbc & uVar1) == 0 && (uVar3 = uVar3 + 1, uVar3 != 0x20))) {
    uVar1 = uVar1 >> 1;
  }
  if (uVar3 == 0x20) {
    puVar4 = DAT_02383dbc + 1;
    uVar3 = 0;
    uVar1 = 0x80000000;
    while (((*puVar4 & uVar1) == 0 && (uVar3 = uVar3 + 1, uVar3 != 0x20))) {
      uVar1 = uVar1 >> 1;
    }
    if (uVar3 == 0x20) {
      return DAT_02383dc0;
    }
    iVar2 = 0xa0;
  }
  else {
    iVar2 = 0x80;
    puVar4 = DAT_02383dbc;
  }
  *puVar4 = *puVar4 & ~(0x80000000U >> (uVar3 & 0xff));
  return iVar2 + uVar3;
}



// ---- FUN_02383dc4 @ 02383dc4 ----

void FUN_02383dc4(int param_1)

{
  uint *puVar1;
  uint uVar2;
  
  if (param_1 + -0xa0 < 0) {
    uVar2 = param_1 - 0x80;
    puVar1 = DAT_02383df0;
  }
  else {
    uVar2 = param_1 - 0xa0;
    puVar1 = DAT_02383df0 + 1;
  }
  *puVar1 = *puVar1 | 0x80000000U >> (uVar2 & 0xff);
  return;
}



// ---- FUN_02383df4 @ 02383df4 ----

void FUN_02383df4(int *param_1,int param_2)

{
  int iVar1;
  int iVar2;
  
  for (iVar2 = *param_1; (iVar2 != 0 && (*(uint *)(iVar2 + 0x54) <= *(uint *)(param_2 + 0x54)));
      iVar2 = *(int *)(iVar2 + 100)) {
    if (iVar2 == param_2) {
      return;
    }
  }
  if (iVar2 != 0) {
    iVar1 = *(int *)(iVar2 + 0x60);
    if (iVar1 == 0) {
      *param_1 = param_2;
    }
    else {
      *(int *)(iVar1 + 100) = param_2;
    }
    *(int *)(param_2 + 0x60) = iVar1;
    *(int *)(param_2 + 100) = iVar2;
    *(int *)(iVar2 + 0x60) = param_2;
    return;
  }
  iVar2 = param_1[1];
  if (iVar2 == 0) {
    *param_1 = param_2;
  }
  else {
    *(int *)(iVar2 + 100) = param_2;
  }
  *(int *)(param_2 + 0x60) = iVar2;
  *(undefined4 *)(param_2 + 100) = 0;
  param_1[1] = param_2;
  return;
}



// ---- FUN_02383e6c @ 02383e6c ----

int FUN_02383e6c(int *param_1,int param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar2 = *param_1;
  do {
    iVar1 = iVar2;
    if (iVar1 == 0) {
      return 0;
    }
    iVar2 = *(int *)(iVar1 + 100);
  } while (iVar1 != param_2);
  iVar3 = *(int *)(iVar1 + 0x60);
  if (*param_1 == iVar1) {
    *param_1 = iVar2;
  }
  else {
    *(int *)(iVar3 + 100) = iVar2;
  }
  if (param_1[1] == iVar1) {
    param_1[1] = iVar3;
  }
  else {
    *(int *)(iVar2 + 0x60) = iVar3;
  }
  return iVar1;
}



// ---- FUN_02383ef4 @ 02383ef4 ----

void FUN_02383ef4(int param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  iVar1 = DAT_02383f50;
  iVar2 = *(int *)(DAT_02383f50 + 0x2c);
  iVar4 = 0;
  while ((iVar3 = iVar2, iVar3 != 0 && (*(uint *)(iVar3 + 0x54) < *(uint *)(param_1 + 0x54)))) {
    iVar4 = iVar3;
    iVar2 = *(int *)(iVar3 + 0x4c);
  }
  if (iVar4 == 0) {
    *(int *)(param_1 + 0x4c) = *(int *)(DAT_02383f50 + 0x2c);
    *(int *)(iVar1 + 0x2c) = param_1;
  }
  else {
    *(undefined4 *)(param_1 + 0x4c) = *(undefined4 *)(iVar4 + 0x4c);
    *(int *)(iVar4 + 0x4c) = param_1;
  }
  return;
}



// ---- FUN_02383f98 @ 02383f98 ----

void FUN_02383f98(void)

{
  undefined2 *puVar1;
  int iVar2;
  int iVar3;
  code *pcVar4;
  int iVar5;
  
  puVar1 = DAT_02384068;
  if (DAT_02384064[1] == 0) {
    if ((*(short *)((int)DAT_02384064 + 0x26) == 0) && (iVar2 = FUN_02385e5c(), iVar2 != 0x12)) {
      iVar5 = *(int *)DAT_02384064[2];
      iVar2 = FUN_023844a0();
      if ((iVar5 != iVar2 && iVar2 != 0) &&
         ((*(int *)(iVar5 + 0x48) == 2 || (iVar3 = FUN_0238473c(iVar5), iVar3 == 0)))) {
        if ((code *)*DAT_02384064 != (code *)0x0) {
          (*(code *)*DAT_02384064)(iVar5,iVar2);
        }
        pcVar4 = *(code **)(puVar1 + 6);
        if (pcVar4 != (code *)0x0) {
          (*pcVar4)(iVar5,iVar2);
        }
        DAT_02384064[10] = iVar2;
        FUN_02384770(iVar2);
      }
    }
    else {
      *puVar1 = 1;
    }
  }
  return;
}



// ---- FUN_0238406c @ 0238406c ----

void FUN_0238406c(void)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  int iVar5;
  int iVar6;
  
  uVar2 = DAT_02384134;
  iVar1 = DAT_02384130;
  if (*(int *)(DAT_02384130 + 0xc) == 0) {
    *(undefined4 *)(DAT_02384130 + 0xc) = 1;
    *(undefined4 *)(iVar1 + 8) = uVar2;
    *(undefined4 *)(iVar1 + 300) = 0x10;
    *(undefined4 *)(iVar1 + 0x128) = 0;
    *(undefined4 *)(iVar1 + 0x120) = 1;
    *(undefined4 *)(iVar1 + 0x124) = 0;
    uVar2 = DAT_0238413c;
    iVar3 = DAT_02384138;
    *(undefined4 *)(iVar1 + 0x130) = 0;
    *(undefined4 *)(iVar1 + 0x2c) = uVar2;
    *(undefined4 *)(iVar1 + 0x28) = uVar2;
    iVar1 = DAT_02384130;
    iVar5 = DAT_02384140;
    if (0 < iVar3) {
      iVar5 = DAT_02384148 - DAT_02384144;
    }
    iVar6 = DAT_02384148 - DAT_02384144;
    *(int *)(DAT_02384130 + 0x150) = iVar6;
    *(int *)(iVar1 + 0x14c) = iVar5 - iVar3;
    uVar2 = DAT_0238414c;
    *(undefined4 *)(iVar1 + 0x154) = 0;
    *(undefined4 *)(iVar6 + -4) = uVar2;
    uVar2 = DAT_02384154;
    **(undefined4 **)(iVar1 + 0x14c) = DAT_02384150;
    *(undefined4 *)(iVar1 + 0x15c) = 0;
    *(undefined4 *)(iVar1 + 0x158) = 0;
    *(undefined2 *)(iVar1 + 0x24) = 0;
    puVar4 = DAT_02384158;
    *(undefined2 *)(iVar1 + 0x26) = 0;
    *puVar4 = uVar2;
    FUN_02384634();
  }
  return;
}



// ---- FUN_0238415c @ 0238415c ----

void FUN_0238415c(int param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5,
                 undefined4 param_6)

{
  undefined4 uVar1;
  undefined4 uVar2;
  int iVar3;
  
  uVar2 = FUN_02385e04();
  iVar3 = *(int *)(DAT_02384254 + 0x20) + 1;
  *(int *)(DAT_02384254 + 0x20) = iVar3;
  *(undefined4 *)(param_1 + 0x54) = param_6;
  *(int *)(param_1 + 0x50) = iVar3;
  *(undefined4 *)(param_1 + 0x48) = 0;
  *(undefined4 *)(param_1 + 0x58) = 0;
  FUN_02383ef4(param_1);
  *(int *)(param_1 + 0x78) = param_4;
  *(int *)(param_1 + 0x74) = param_4 - param_5;
  *(undefined4 *)(param_1 + 0x7c) = 0;
  uVar1 = DAT_0238425c;
  *(undefined4 *)(*(int *)(param_1 + 0x78) + -4) = DAT_02384258;
  **(undefined4 **)(param_1 + 0x74) = uVar1;
  *(undefined4 *)(param_1 + 0x84) = 0;
  *(undefined4 *)(param_1 + 0x80) = 0;
  FUN_023846d0(param_1,param_2,param_4 + -4);
  uVar1 = DAT_02384260;
  *(undefined4 *)(param_1 + 4) = param_3;
  *(undefined4 *)(param_1 + 0x3c) = uVar1;
  FUN_023860ac(0,(param_4 - param_5) + 4,param_5 + -8);
  *(undefined4 *)(param_1 + 0x68) = 0;
  *(undefined4 *)(param_1 + 0x6c) = 0;
  *(undefined4 *)(param_1 + 0x70) = 0;
  *(undefined4 *)(param_1 + 0x98) = 0;
  *(undefined4 *)(param_1 + 0x5c) = 0;
  *(undefined4 *)(param_1 + 100) = 0;
  *(undefined4 *)(param_1 + 0x60) = 0;
  FUN_023860ac(0,param_1 + 0x88,0xc);
  *(undefined4 *)(param_1 + 0x94) = 0;
  FUN_02385e18(uVar2);
  return;
}



// ---- FUN_02384398 @ 02384398 ----

void FUN_02384398(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  
  uVar1 = FUN_02385e04();
  iVar2 = **(int **)(DAT_023843e8 + 8);
  if (param_1 != 0) {
    *(int *)(iVar2 + 0x5c) = param_1;
    FUN_02383df4(param_1,iVar2);
  }
  *(undefined4 *)(iVar2 + 0x48) = 0;
  FUN_02383f98();
  FUN_02385e18(uVar1);
  return;
}



// ---- FUN_023843ec @ 023843ec ----

void FUN_023843ec(int *param_1)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  
  uVar1 = FUN_02385e04();
  if (*param_1 != 0) {
    while( true ) {
      iVar3 = *param_1;
      if (iVar3 == 0) break;
      if (iVar3 != 0) {
        iVar2 = *(int *)(iVar3 + 100);
        *param_1 = iVar2;
        if (iVar2 == 0) {
          param_1[1] = 0;
          *(undefined4 *)(iVar3 + 0x5c) = 0;
        }
        else {
          *(undefined4 *)(iVar2 + 0x60) = 0;
        }
      }
      *(undefined4 *)(iVar3 + 0x48) = 1;
      *(undefined4 *)(iVar3 + 0x5c) = 0;
      *(undefined4 *)(iVar3 + 100) = 0;
      *(undefined4 *)(iVar3 + 0x60) = 0;
    }
    param_1[1] = 0;
    *param_1 = 0;
    FUN_02383f98();
  }
  FUN_02385e18(uVar1);
  return;
}



// ---- FUN_02384474 @ 02384474 ----

void FUN_02384474(int param_1)

{
  undefined4 uVar1;
  
  uVar1 = FUN_02385e04();
  *(undefined4 *)(param_1 + 0x48) = 1;
  FUN_02383f98();
  FUN_02385e18(uVar1);
  return;
}



// ---- FUN_023844a0 @ 023844a0 ----

void FUN_023844a0(undefined4 param_1,int param_2)

{
  int iVar1;
  
  iVar1 = *(int *)(DAT_023844c4 + 0x2c);
  while( true ) {
    if (iVar1 != 0) {
      param_2 = *(int *)(iVar1 + 0x48);
    }
    if (iVar1 == 0 || param_2 == 1) break;
    iVar1 = *(int *)(iVar1 + 0x4c);
  }
  return;
}



// ---- FUN_023844c8 @ 023844c8 ----

undefined4 FUN_023844c8(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  
  iVar2 = FUN_02385e04();
  iVar4 = 0;
  for (iVar5 = *(int *)(DAT_02384568 + 0x2c); iVar5 != 0 && iVar5 != param_1;
      iVar5 = *(int *)(iVar5 + 0x4c)) {
    iVar4 = iVar5;
  }
  iVar1 = iVar2;
  if (iVar5 != 0) {
    iVar1 = DAT_0238456c;
  }
  if (iVar5 != 0 && iVar5 != iVar1) {
    if (*(int *)(iVar5 + 0x54) != param_2) {
      if (iVar4 == 0) {
        *(undefined4 *)(DAT_02384568 + 0x2c) = *(undefined4 *)(param_1 + 0x4c);
      }
      else {
        *(undefined4 *)(iVar4 + 0x4c) = *(undefined4 *)(param_1 + 0x4c);
      }
      *(int *)(param_1 + 0x54) = param_2;
      FUN_02383ef4(param_1);
      FUN_02383f98();
    }
    FUN_02385e18(iVar2);
    uVar3 = 1;
  }
  else {
    FUN_02385e18(iVar2);
    uVar3 = 0;
  }
  return uVar3;
}



// ---- FUN_02384570 @ 02384570 ----

void FUN_02384570(uint param_1)

{
  ulonglong uVar1;
  undefined4 uVar2;
  uint uVar3;
  int local_3c;
  undefined1 auStack_38 [44];
  
  FUN_02385490(auStack_38);
  local_3c = **(int **)(DAT_02384608 + 8);
  uVar2 = FUN_02385e04();
  uVar1 = (ulonglong)DAT_0238460c;
  uVar3 = (uint)(uVar1 * param_1 >> 0x20);
  *(undefined1 **)(local_3c + 0x94) = auStack_38;
  FUN_023855cc(auStack_38,(uint)(uVar1 * param_1) >> 6 | uVar3 * 0x4000000,uVar3 >> 6,DAT_02384610,
               &local_3c);
  while (local_3c != 0) {
    FUN_02384398(0);
  }
  FUN_02385e18(uVar2);
  return;
}



// ---- FUN_02384634 @ 02384634 ----

undefined4 FUN_02384634(undefined4 param_1)

{
  undefined4 uVar1;
  
  FUN_02385e04();
  uVar1 = *(undefined4 *)(DAT_0238465c + 0x30);
  *(undefined4 *)(DAT_0238465c + 0x30) = param_1;
  FUN_02385e18();
  return uVar1;
}



// ---- FUN_023846d0 @ 023846d0 ----

void FUN_023846d0(undefined4 *param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  uint uVar2;
  
  param_1[0x10] = param_2 + 4U;
  param_1[0x11] = param_3;
  uVar2 = param_3 - 0x40;
  if ((uVar2 & 4) != 0) {
    uVar2 = param_3 - 0x44;
  }
  param_1[0xe] = uVar2;
  if ((param_2 + 4U & 1) == 0) {
    uVar1 = 0x1f;
  }
  else {
    uVar1 = 0x3f;
  }
  *param_1 = uVar1;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xf] = 0;
  return;
}



// ---- FUN_0238473c @ 0238473c ----

undefined4 FUN_0238473c(int *param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  int iVar1;
  int unaff_r4;
  int unaff_r5;
  int unaff_r6;
  int unaff_r7;
  int unaff_r8;
  int unaff_r9;
  int unaff_r10;
  int unaff_r11;
  int in_r12;
  int in_lr;
  char in_NG;
  char in_ZR;
  char in_CY;
  char in_OV;
  byte in_Q;
  
  iVar1 = (uint)(byte)(in_NG << 4 | in_ZR << 3 | in_CY << 2 | in_OV << 1 | in_Q) << 0x1b;
  *param_1 = iVar1;
  param_1[0x11] = (int)register0x00000054;
  param_1[1] = 1;
  param_1[2] = (int)(param_1 + 1);
  param_1[3] = iVar1;
  param_1[4] = param_4;
  param_1[5] = unaff_r4;
  param_1[6] = unaff_r5;
  param_1[7] = unaff_r6;
  param_1[8] = unaff_r7;
  param_1[9] = unaff_r8;
  param_1[10] = unaff_r9;
  param_1[0xb] = unaff_r10;
  param_1[0xc] = unaff_r11;
  param_1[0xd] = in_r12;
  param_1[0xe] = (int)register0x00000054;
  param_1[0xf] = in_lr;
  param_1[0x10] = (int)FUN_02384770;
  return 0;
}



// ---- FUN_02384770 @ 02384770 ----

void FUN_02384770(int param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02384798. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)(*(int *)(param_1 + 0x3c) + -4))
            (*(undefined4 *)(param_1 + 4),*(undefined4 *)(param_1 + 8),
             *(undefined4 *)(param_1 + 0xc),*(undefined4 *)(param_1 + 0x10));
  return;
}



// ---- FUN_0238479c @ 0238479c ----

void FUN_0238479c(undefined4 *param_1,undefined4 param_2,undefined4 param_3)

{
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  param_1[4] = param_2;
  param_1[5] = param_3;
  param_1[6] = 0;
  param_1[7] = 0;
  return;
}



// ---- FUN_023847c4 @ 023847c4 ----

undefined4 FUN_023847c4(int param_1,undefined4 param_2,uint param_3)

{
  undefined4 uVar1;
  int extraout_r1;
  
  uVar1 = FUN_02385e04();
  while( true ) {
    if (*(int *)(param_1 + 0x1c) < *(int *)(param_1 + 0x14)) {
      FUN_0238e8c8(*(int *)(param_1 + 0x18) + *(int *)(param_1 + 0x1c));
      *(undefined4 *)(*(int *)(param_1 + 0x10) + extraout_r1 * 4) = param_2;
      *(int *)(param_1 + 0x1c) = *(int *)(param_1 + 0x1c) + 1;
      FUN_023843ec(param_1 + 8);
      FUN_02385e18(uVar1);
      return 1;
    }
    if ((param_3 & 1) == 0) break;
    FUN_02384398(param_1);
  }
  FUN_02385e18(uVar1);
  return 0;
}



// ---- FUN_02384850 @ 02384850 ----

undefined4 FUN_02384850(int param_1,undefined4 *param_2,uint param_3)

{
  undefined4 uVar1;
  undefined4 extraout_r1;
  
  uVar1 = FUN_02385e04();
  while( true ) {
    if (*(int *)(param_1 + 0x1c) != 0) {
      if (param_2 != (undefined4 *)0x0) {
        *param_2 = *(undefined4 *)(*(int *)(param_1 + 0x10) + *(int *)(param_1 + 0x18) * 4);
      }
      FUN_0238e8c8(*(int *)(param_1 + 0x18) + 1,*(undefined4 *)(param_1 + 0x14));
      *(undefined4 *)(param_1 + 0x18) = extraout_r1;
      *(int *)(param_1 + 0x1c) = *(int *)(param_1 + 0x1c) + -1;
      FUN_023843ec(param_1);
      FUN_02385e18(uVar1);
      return 1;
    }
    if ((param_3 & 1) == 0) break;
    FUN_02384398(param_1 + 8);
  }
  FUN_02385e18(uVar1);
  return 0;
}



// ---- FUN_023848ec @ 023848ec ----

undefined4 FUN_023848ec(int param_1,undefined4 *param_2,uint param_3)

{
  undefined4 uVar1;
  
  uVar1 = FUN_02385e04();
  while( true ) {
    if (*(int *)(param_1 + 0x1c) != 0) {
      if (param_2 != (undefined4 *)0x0) {
        *param_2 = *(undefined4 *)(*(int *)(param_1 + 0x10) + *(int *)(param_1 + 0x18) * 4);
      }
      FUN_02385e18(uVar1);
      return 1;
    }
    if ((param_3 & 1) == 0) break;
    FUN_02384398(param_1 + 8);
  }
  FUN_02385e18(uVar1);
  return 0;
}



// ---- FUN_02384978 @ 02384978 ----

void FUN_02384978(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  
  uVar1 = FUN_02385e04();
  iVar2 = *(int *)(DAT_023849f8 + 4);
  do {
    if (*(int *)(param_1 + 8) == 0) {
      *(int *)(param_1 + 8) = iVar2;
      *(int *)(param_1 + 0xc) = *(int *)(param_1 + 0xc) + 1;
      FUN_02384a94(iVar2,param_1);
LAB_023849e8:
      FUN_02385e18(uVar1);
      return;
    }
    if (*(int *)(param_1 + 8) == iVar2) {
      *(int *)(param_1 + 0xc) = *(int *)(param_1 + 0xc) + 1;
      goto LAB_023849e8;
    }
    *(int *)(iVar2 + 0x68) = param_1;
    FUN_02384398(param_1);
    *(undefined4 *)(iVar2 + 0x68) = 0;
  } while( true );
}



// ---- FUN_02384a94 @ 02384a94 ----

void FUN_02384a94(int param_1,int param_2)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0x70);
  if (iVar1 == 0) {
    *(int *)(param_1 + 0x6c) = param_2;
  }
  else {
    *(int *)(iVar1 + 0x10) = param_2;
  }
  *(int *)(param_2 + 0x14) = iVar1;
  *(undefined4 *)(param_2 + 0x10) = 0;
  *(int *)(param_1 + 0x70) = param_2;
  return;
}



// ---- FUN_02384adc @ 02384adc ----

void FUN_02384adc(void)

{
  FUN_02384b0c();
  thunk_EXT_FUN_037fe14c();
  FUN_02383b10();
  FUN_02383910();
  FUN_02385218();
  FUN_0238543c();
  FUN_0238406c();
  FUN_02385e80();
  FUN_0238e088();
  return;
}



// ---- FUN_02384b0c @ 02384b0c ----

void FUN_02384b0c(void)

{
  if (*DAT_02384b44 == 0) {
    *DAT_02384b44 = 1;
    FUN_02384b48();
    FUN_02384b48(7);
    FUN_02384b48(8);
  }
  return;
}



// ---- FUN_02384b48 @ 02384b48 ----

void FUN_02384b48(int param_1)

{
  undefined4 uVar1;
  
  uVar1 = FUN_02384bac();
  *(undefined4 *)(param_1 * 4 + 0x27ffdc4) = uVar1;
  uVar1 = FUN_02384c28(param_1);
  *(undefined4 *)(param_1 * 4 + 0x27ffda0) = uVar1;
  return;
}



// ---- FUN_02384b84 @ 02384b84 ----

undefined4 FUN_02384b84(int param_1)

{
  return *(undefined4 *)(param_1 * 4 + 0x27ffdc4);
}



// ---- FUN_02384b98 @ 02384b98 ----

undefined4 FUN_02384b98(int param_1)

{
  return *(undefined4 *)(param_1 * 4 + 0x27ffda0);
}



// ---- FUN_02384bac @ 02384bac ----

uint FUN_02384bac(int param_1)

{
  uint uVar1;
  
  if (param_1 == 1) {
    return DAT_02384c14;
  }
  if (param_1 == 7) {
    return 0x3800000;
  }
  if (param_1 != 8) {
    return 0;
  }
  uVar1 = 0x3800000;
  if (0x3800000 < DAT_02384c20) {
    uVar1 = DAT_02384c20;
  }
  if (DAT_02384c24 != 0) {
    if (DAT_02384c24 < 0) {
      uVar1 = uVar1 - DAT_02384c24;
    }
    else {
      uVar1 = (DAT_02384c1c - DAT_02384c18) - DAT_02384c24;
    }
    return uVar1;
  }
  return uVar1;
}



// ---- FUN_02384c28 @ 02384c28 ----

uint FUN_02384c28(int param_1)

{
  uint uVar1;
  
  if (param_1 == 1) {
    return DAT_02384c78;
  }
  if (param_1 != 7) {
    if (param_1 != 8) {
      return 0;
    }
    uVar1 = 0x3800000;
    if (0x3800000 < DAT_02384c7c) {
      uVar1 = DAT_02384c7c;
    }
    return uVar1;
  }
  uVar1 = DAT_02384c7c;
  if (0x3800000 < DAT_02384c7c) {
    uVar1 = 0x3800000;
  }
  return uVar1;
}



// ---- FUN_02384c80 @ 02384c80 ----

void FUN_02384c80(int param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 * 4 + 0x27ffda0) = param_2;
  return;
}



// ---- FUN_02384c94 @ 02384c94 ----

int FUN_02384c94(int param_1,int *param_2)

{
  if ((int *)param_2[1] != (int *)0x0) {
    *(int *)param_2[1] = *param_2;
  }
  if (*param_2 == 0) {
    param_1 = param_2[1];
  }
  else {
    *(int *)(*param_2 + 4) = param_2[1];
  }
  return param_1;
}



// ---- FUN_02384cbc @ 02384cbc ----

uint * FUN_02384cbc(uint *param_1,uint *param_2)

{
  uint *puVar1;
  uint *puVar2;
  uint *puVar3;
  
  puVar2 = (uint *)0x0;
  for (puVar3 = param_1; (puVar3 != (uint *)0x0 && (puVar3 < param_2)); puVar3 = (uint *)puVar3[1])
  {
    puVar2 = puVar3;
  }
  *param_2 = (uint)puVar2;
  param_2[1] = (uint)puVar3;
  if (puVar3 != (uint *)0x0) {
    *puVar3 = (uint)param_2;
    if ((uint *)((int)param_2 + param_2[2]) == puVar3) {
      param_2[2] = param_2[2] + puVar3[2];
      puVar3 = (uint *)puVar3[1];
      param_2[1] = (uint)puVar3;
      if (puVar3 != (uint *)0x0) {
        *puVar3 = (uint)param_2;
      }
    }
  }
  puVar1 = param_2;
  if (puVar2 != (uint *)0x0) {
    puVar2[1] = (uint)param_2;
    puVar1 = param_1;
    if ((uint *)((int)puVar2 + puVar2[2]) == param_2) {
      puVar2[2] = puVar2[2] + param_2[2];
      puVar2[1] = (uint)puVar3;
      if (puVar3 != (uint *)0x0) {
        *puVar3 = (uint)puVar2;
      }
    }
  }
  return puVar1;
}



// ---- FUN_02384d64 @ 02384d64 ----

undefined4 * FUN_02384d64(int param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  int *piVar4;
  int iVar5;
  undefined4 *puVar6;
  int iVar7;
  uint uVar8;
  
  uVar1 = FUN_02385e04();
  piVar4 = *(int **)(DAT_02384e70 + param_1 * 4);
  if (piVar4 == (int *)0x0) {
    FUN_02385e18();
    puVar2 = (undefined4 *)0x0;
  }
  else {
    if (param_2 < 0) {
      param_2 = *piVar4;
    }
    iVar7 = param_2 * 0xc + piVar4[4];
    uVar8 = param_3 + 0x3fU & 0xffffffe0;
    for (puVar2 = *(undefined4 **)(iVar7 + 4);
        (puVar2 != (undefined4 *)0x0 && ((int)puVar2[2] < (int)uVar8));
        puVar2 = (undefined4 *)puVar2[1]) {
    }
    if (puVar2 == (undefined4 *)0x0) {
      FUN_02385e18(uVar1);
      puVar2 = (undefined4 *)0x0;
    }
    else {
      iVar5 = puVar2[2];
      if (iVar5 - uVar8 < 0x40) {
        uVar3 = FUN_02384c94(*(undefined4 **)(iVar7 + 4),puVar2);
        *(undefined4 *)(iVar7 + 4) = uVar3;
      }
      else {
        puVar2[2] = uVar8;
        piVar4 = (int *)((int)puVar2 + uVar8);
        piVar4[2] = iVar5 - uVar8;
        *(undefined4 *)((int)puVar2 + uVar8) = *puVar2;
        puVar6 = (undefined4 *)puVar2[1];
        piVar4[1] = (int)puVar6;
        if (puVar6 != (undefined4 *)0x0) {
          *puVar6 = piVar4;
        }
        if (*piVar4 == 0) {
          *(int **)(iVar7 + 4) = piVar4;
        }
        else {
          *(int **)(*piVar4 + 4) = piVar4;
        }
      }
      puVar6 = *(undefined4 **)(iVar7 + 8);
      *puVar2 = 0;
      puVar2[1] = puVar6;
      if (puVar6 != (undefined4 *)0x0) {
        *puVar6 = puVar2;
      }
      *(undefined4 **)(iVar7 + 8) = puVar2;
      FUN_02385e18(uVar1);
      puVar2 = puVar2 + 8;
    }
  }
  return puVar2;
}



// ---- FUN_02384ee0 @ 02384ee0 ----

undefined4 FUN_02384ee0(int param_1,undefined4 param_2)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  
  FUN_02385e04();
  puVar1 = *(undefined4 **)(DAT_02384f10 + param_1 * 4);
  uVar2 = *puVar1;
  *puVar1 = param_2;
  FUN_02385e18();
  return uVar2;
}



// ---- FUN_02384f14 @ 02384f14 ----

undefined4 FUN_02384f14(int param_1,undefined4 *param_2,uint param_3,int param_4)

{
  int iVar1;
  int iVar2;
  
  FUN_02385e04();
  *(undefined4 **)(DAT_02384fb8 + param_1 * 4) = param_2;
  param_2[4] = param_2 + 5;
  param_2[1] = param_4;
  for (iVar2 = 0; iVar2 < (int)param_2[1]; iVar2 = iVar2 + 1) {
    iVar1 = param_2[4];
    *(undefined4 *)(iVar1 + iVar2 * 0xc) = 0xffffffff;
    iVar1 = iVar1 + iVar2 * 0xc;
    *(undefined4 *)(iVar1 + 8) = 0;
    *(undefined4 *)(iVar1 + 4) = 0;
  }
  *param_2 = 0xffffffff;
  param_2[2] = param_2[4] + param_4 * 0xc + 0x1fU & 0xffffffe0;
  param_2[3] = param_3 & 0xffffffe0;
  FUN_02385e18();
  return param_2[2];
}



// ---- FUN_02384fbc @ 02384fbc ----

int FUN_02384fbc(int param_1,int param_2,uint param_3)

{
  int *piVar1;
  int iVar2;
  undefined4 *puVar3;
  int iVar4;
  int iVar5;
  
  FUN_02385e04();
  iVar5 = *(int *)(DAT_02385058 + param_1 * 4);
  puVar3 = (undefined4 *)(param_2 + 0x1fU & 0xffffffe0);
  iVar2 = 0;
  while( true ) {
    if (*(int *)(iVar5 + 4) <= iVar2) {
      FUN_02385e18();
      return -1;
    }
    iVar4 = *(int *)(iVar5 + 0x10);
    piVar1 = (int *)(iVar4 + iVar2 * 0xc);
    if (*(int *)(iVar4 + iVar2 * 0xc) < 0) break;
    iVar2 = iVar2 + 1;
  }
  *piVar1 = (param_3 & 0xffffffe0) - (int)puVar3;
  *puVar3 = 0;
  puVar3[1] = 0;
  puVar3[2] = *piVar1;
  piVar1[1] = (int)puVar3;
  piVar1[2] = 0;
  FUN_02385e18();
  return iVar2;
}



// ---- FUN_0238505c @ 0238505c ----

int FUN_0238505c(int param_1,int param_2)

{
  int *piVar1;
  int iVar2;
  uint uVar3;
  uint *puVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  uint *puVar8;
  int iVar9;
  uint *puVar10;
  
  iVar5 = 0;
  iVar6 = 0;
  iVar7 = -1;
  FUN_02385e04();
  piVar1 = *(int **)(DAT_023851f8 + param_1 * 4);
  iVar9 = piVar1[4];
  if (param_2 == -1) {
    param_2 = *piVar1;
  }
  if (((iVar9 != 0) && (-1 < param_2)) && (param_2 < piVar1[1])) {
    uVar3 = param_2 * 0xc;
    iVar2 = *(int *)(iVar9 + uVar3);
    iVar9 = iVar9 + uVar3;
    if (-1 < iVar2) {
      puVar10 = *(uint **)(iVar9 + 8);
      if (puVar10 != (uint *)0x0) {
        uVar3 = *puVar10;
      }
      if (puVar10 == (uint *)0x0 || uVar3 == 0) {
        while (puVar10 != (uint *)0x0) {
          if (((puVar10 < (uint *)piVar1[2]) || (puVar4 = (uint *)piVar1[3], puVar4 <= puVar10)) ||
             (((uint)puVar10 & 0x1f) != 0)) goto LAB_023851e8;
          puVar8 = (uint *)puVar10[1];
          if (puVar8 != (uint *)0x0) {
            puVar4 = (uint *)*puVar8;
          }
          if (((puVar8 != (uint *)0x0 && puVar4 != puVar10) || (uVar3 = puVar10[2], uVar3 < 0x40))
             || (((uVar3 & 0x1f) != 0 ||
                 ((iVar5 = iVar5 + uVar3, iVar5 < 1 || (puVar10 = puVar8, iVar2 < iVar5))))))
          goto LAB_023851e8;
        }
        puVar10 = *(uint **)(iVar9 + 4);
        if (puVar10 != (uint *)0x0) {
          uVar3 = *puVar10;
        }
        if (puVar10 == (uint *)0x0 || uVar3 == 0) goto LAB_023851d8;
      }
    }
  }
LAB_023851e8:
  FUN_02385e18();
  return iVar7;
LAB_023851d8:
  if (puVar10 == (uint *)0x0) {
    if (iVar5 == iVar2) {
      iVar7 = iVar6;
    }
    goto LAB_023851e8;
  }
  if (((puVar10 < (uint *)piVar1[2]) || (puVar4 = (uint *)piVar1[3], puVar4 <= puVar10)) ||
     (((uint)puVar10 & 0x1f) != 0)) goto LAB_023851e8;
  puVar8 = (uint *)puVar10[1];
  if (puVar8 != (uint *)0x0) {
    puVar4 = (uint *)*puVar8;
  }
  if (((puVar8 != (uint *)0x0 && puVar4 != puVar10) || (uVar3 = puVar10[2], uVar3 < 0x40)) ||
     (((uVar3 & 0x1f) != 0 ||
      ((puVar8 != (uint *)0x0 && (puVar8 <= (uint *)((int)puVar10 + uVar3))))))) goto LAB_023851e8;
  iVar5 = iVar5 + uVar3;
  iVar6 = iVar6 + (uVar3 - 0x20);
  if ((iVar5 < 1) || (puVar10 = puVar8, iVar2 < iVar5)) goto LAB_023851e8;
  goto LAB_023851d8;
}



// ---- FUN_023851fc @ 023851fc ----

void FUN_023851fc(uint param_1)

{
  *DAT_02385214 = *DAT_02385214 | (ushort)(1 << (param_1 & 0xff));
  return;
}



// ---- FUN_02385218 @ 02385218 ----

void FUN_02385218(void)

{
  short *psVar1;
  undefined2 *puVar2;
  undefined4 uVar3;
  undefined4 in_r3;
  
  if (*DAT_02385288 == 0) {
    *DAT_02385288 = 1;
    FUN_023851fc(0);
    psVar1 = DAT_02385288;
    psVar1[4] = 0;
    puVar2 = DAT_0238528c;
    psVar1[5] = 0;
    psVar1[6] = 0;
    psVar1[7] = 0;
    *puVar2 = 0;
    uVar3 = DAT_02385290;
    puVar2[-1] = 0;
    *puVar2 = 0xc1;
    FUN_02383934(8,uVar3,0xc1,puVar2,in_r3);
    FUN_02383a68(8);
    psVar1 = DAT_02385288;
    psVar1[2] = 0;
    psVar1[3] = 0;
  }
  return;
}



// ---- FUN_02385294 @ 02385294 ----

undefined2 FUN_02385294(void)

{
  return *DAT_023852a0;
}



// ---- FUN_0238530c @ 0238530c ----

undefined8 FUN_0238530c(void)

{
  ushort uVar1;
  bool bVar2;
  uint local_c;
  uint local_8;
  
  FUN_02385e04();
  uVar1 = *DAT_023853a4;
  local_c = *(uint *)(DAT_023853a8 + 8) & DAT_023853ac - 0x10000;
  local_8 = *(uint *)(DAT_023853a8 + 0xc) & DAT_023853ac;
  if (((*(uint *)(DAT_023853a4 + 0x8a) & 8) != 0) && ((uVar1 & 0x8000) == 0)) {
    bVar2 = 0xfffffffe < local_c;
    local_c = local_c + 1;
    local_8 = local_8 + bVar2;
  }
  FUN_02385e18();
  return CONCAT44(local_8 << 0x10 | local_c >> 0x10,(uint)uVar1 | local_c << 0x10);
}



// ---- FUN_023853b0 @ 023853b0 ----

void FUN_023853b0(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined2 *puVar1;
  uint uVar2;
  int iVar3;
  uint uVar4;
  undefined8 uVar5;
  
  uVar5 = FUN_0238530c();
  *DAT_0238542c = 0;
  uVar4 = *(uint *)(param_1 + 0xc) - (uint)uVar5;
  iVar3 = *(int *)(param_1 + 0x10) -
          ((int)((ulonglong)uVar5 >> 0x20) + (uint)(*(uint *)(param_1 + 0xc) < (uint)uVar5));
  FUN_023839d0(1,DAT_02385430,0,*(int *)(param_1 + 0x10),param_4);
  puVar1 = DAT_02385438;
  uVar2 = DAT_02385434;
  if ((-1 < iVar3) && (uVar2 = 0, iVar3 < (int)(uint)(uVar4 < 0x10000))) {
    uVar2 = ~uVar4 & 0xffff;
  }
  *DAT_02385438 = (short)uVar2;
  puVar1[1] = 0xc1;
  FUN_02383a68(0x10);
  return;
}



// ---- FUN_0238543c @ 0238543c ----

void FUN_0238543c(void)

{
  short *psVar1;
  
  if (*DAT_0238547c == 0) {
    *DAT_0238547c = 1;
    FUN_023851fc();
    psVar1 = DAT_0238547c;
    psVar1[2] = 0;
    psVar1[3] = 0;
    psVar1[4] = 0;
    psVar1[5] = 0;
    FUN_02383aa0(0x10);
  }
  return;
}



// ---- FUN_02385480 @ 02385480 ----

undefined2 FUN_02385480(void)

{
  return *DAT_0238548c;
}



// ---- FUN_02385490 @ 02385490 ----

void FUN_02385490(undefined4 *param_1)

{
  *param_1 = 0;
  param_1[2] = 0;
  return;
}



// ---- FUN_023854a0 @ 023854a0 ----

void FUN_023854a0(int param_1,undefined4 param_2,undefined4 param_3)

{
  longlong lVar1;
  longlong lVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  int iVar8;
  uint uVar9;
  bool bVar10;
  undefined8 uVar11;
  longlong lVar12;
  
  lVar1 = CONCAT44(param_3,param_2);
  if (*(int *)(param_1 + 0x20) != 0 || *(int *)(param_1 + 0x1c) != 0) {
    uVar11 = FUN_0238530c();
    uVar5 = (uint)((ulonglong)uVar11 >> 0x20);
    uVar4 = (uint)uVar11;
    uVar7 = *(uint *)(param_1 + 0x28);
    uVar9 = *(uint *)(param_1 + 0x24);
    lVar1 = *(longlong *)(param_1 + 0x24);
    bVar10 = uVar5 <= uVar7;
    if (uVar7 == uVar5) {
      bVar10 = uVar4 <= uVar9;
    }
    if (!bVar10) {
      lVar2 = *(longlong *)(param_1 + 0x1c);
      lVar12 = FUN_0238e880(uVar4 - uVar9,uVar5 - (uVar7 + (uVar4 < uVar9)),
                            *(undefined4 *)(param_1 + 0x1c),*(undefined4 *)(param_1 + 0x20));
      lVar1 = (lVar12 + 1) * lVar2 + lVar1;
    }
  }
  iVar8 = (int)((ulonglong)lVar1 >> 0x20);
  *(uint *)(param_1 + 0xc) = (uint)lVar1;
  iVar6 = DAT_023855c8;
  *(int *)(param_1 + 0x10) = iVar8;
  iVar3 = DAT_023855c8;
  iVar6 = *(int *)(iVar6 + 4);
  while( true ) {
    if (iVar6 == 0) {
      *(undefined4 *)(param_1 + 0x18) = 0;
      iVar6 = *(int *)(iVar3 + 8);
      *(int *)(iVar3 + 8) = param_1;
      *(int *)(param_1 + 0x14) = iVar6;
      if (iVar6 == 0) {
        *(int *)(iVar3 + 8) = param_1;
        *(int *)(iVar3 + 4) = param_1;
        FUN_023853b0(param_1);
      }
      else {
        *(int *)(iVar6 + 0x18) = param_1;
      }
      return;
    }
    if ((int)(iVar8 - (*(int *)(iVar6 + 0x10) + (uint)((uint)lVar1 < *(uint *)(iVar6 + 0xc)))) < 0)
    break;
    iVar6 = *(int *)(iVar6 + 0x18);
  }
  *(undefined4 *)(param_1 + 0x14) = *(undefined4 *)(iVar6 + 0x14);
  *(int *)(iVar6 + 0x14) = param_1;
  *(int *)(param_1 + 0x18) = iVar6;
  if (*(int *)(param_1 + 0x14) == 0) {
    *(int *)(DAT_023855c8 + 4) = param_1;
    FUN_023853b0(param_1);
    return;
  }
  *(int *)(*(int *)(param_1 + 0x14) + 0x18) = param_1;
  return;
}



// ---- FUN_023855cc @ 023855cc ----

void FUN_023855cc(int *param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5)

{
  undefined4 uVar1;
  undefined4 uVar2;
  longlong lVar3;
  int iVar4;
  
  iVar4 = param_4;
  if ((param_1 == (int *)0x0) || (*param_1 != 0)) {
    FUN_02385f74();
  }
  uVar1 = FUN_02385e04();
  param_1[7] = 0;
  param_1[8] = 0;
  *param_1 = param_4;
  param_1[1] = param_5;
  lVar3 = FUN_0238530c();
  lVar3 = lVar3 + CONCAT44(param_3,param_2);
  uVar2 = (undefined4)lVar3;
  FUN_023854a0(param_1,uVar2,(int)((ulonglong)lVar3 >> 0x20),uVar2,iVar4);
  FUN_02385e18(uVar1);
  return;
}



// ---- FUN_0238563c @ 0238563c ----

void FUN_0238563c(int *param_1,int param_2,int param_3,int param_4,int param_5,int param_6,
                 int param_7)

{
  undefined4 uVar1;
  
  if ((param_1 == (int *)0x0) || (*param_1 != 0)) {
    FUN_02385f74();
  }
  uVar1 = FUN_02385e04();
  param_1[7] = param_4;
  param_1[8] = param_5;
  param_1[9] = param_2;
  param_1[10] = param_3;
  *param_1 = param_6;
  param_1[1] = param_7;
  FUN_023854a0(param_1,0,0);
  FUN_02385e18(uVar1);
  return;
}



// ---- FUN_023856b0 @ 023856b0 ----

void FUN_023856b0(int *param_1)

{
  undefined4 uVar1;
  int iVar2;
  
  uVar1 = FUN_02385e04();
  if (*param_1 == 0) {
    FUN_02385e18();
  }
  else {
    iVar2 = param_1[6];
    if (iVar2 == 0) {
      *(int *)(DAT_02385734 + 8) = param_1[5];
    }
    else {
      *(int *)(iVar2 + 0x14) = param_1[5];
    }
    if (param_1[5] == 0) {
      *(int *)(DAT_02385734 + 4) = iVar2;
      if (iVar2 != 0) {
        FUN_023853b0();
      }
    }
    else {
      *(int *)(param_1[5] + 0x18) = iVar2;
    }
    *param_1 = 0;
    param_1[7] = 0;
    param_1[8] = 0;
    FUN_02385e18(uVar1);
  }
  return;
}



// ---- FUN_02385748 @ 02385748 ----

void FUN_02385748(void)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  code *pcVar5;
  bool bVar6;
  undefined8 uVar7;
  
  *DAT_02385830 = 0;
  FUN_02383aa0(0x10);
  *DAT_02385834 = *DAT_02385834 | 0x10;
  uVar7 = FUN_0238530c();
  iVar1 = DAT_02385838;
  uVar2 = (uint)((ulonglong)uVar7 >> 0x20);
  puVar4 = *(undefined4 **)(DAT_02385838 + 4);
  if (puVar4 != (undefined4 *)0x0) {
    bVar6 = (uint)puVar4[4] <= uVar2;
    if (uVar2 == puVar4[4]) {
      bVar6 = (uint)puVar4[3] <= (uint)uVar7;
    }
    if (bVar6) {
      iVar3 = puVar4[6];
      *(int *)(DAT_02385838 + 4) = iVar3;
      if (iVar3 == 0) {
        *(undefined4 *)(iVar1 + 8) = 0;
      }
      else {
        *(undefined4 *)(iVar3 + 0x14) = 0;
      }
      pcVar5 = (code *)*puVar4;
      if (puVar4[8] == 0 && puVar4[7] == 0) {
        *puVar4 = 0;
      }
      if (pcVar5 != (code *)0x0) {
        (*pcVar5)(puVar4[1]);
      }
      if (puVar4[8] != 0 || puVar4[7] != 0) {
        *puVar4 = pcVar5;
        FUN_023854a0(puVar4,0,0);
      }
      if (*(int *)(DAT_02385838 + 4) != 0) {
        FUN_023853b0();
      }
    }
    else {
      FUN_023853b0(puVar4);
    }
  }
  return;
}



// ---- FUN_0238583c @ 0238583c ----

void FUN_0238583c(void)

{
  short *psVar1;
  
  psVar1 = DAT_02385884;
  if (*DAT_02385884 == 0) {
    *DAT_02385884 = 1;
    psVar1[6] = 0;
    psVar1[7] = 0;
    psVar1[8] = 0;
    psVar1[9] = 0;
    FUN_02383aa0(4);
    psVar1 = DAT_02385884;
    psVar1[4] = 0;
    psVar1[5] = 0;
    psVar1[2] = 0;
    psVar1[3] = 0;
  }
  return;
}



// ---- FUN_02385888 @ 02385888 ----

undefined2 FUN_02385888(void)

{
  return *DAT_02385894;
}



// ---- FUN_02385898 @ 02385898 ----

void FUN_02385898(int param_1)

{
  int iVar1;
  int iVar2;
  
  iVar2 = *(int *)(DAT_02385910 + 0xc);
  while( true ) {
    if (iVar2 == 0) {
      FUN_02385914();
      return;
    }
    if ((*(uint *)(param_1 + 0xc) <= *(uint *)(iVar2 + 0xc)) &&
       ((*(uint *)(iVar2 + 0xc) != *(uint *)(param_1 + 0xc) ||
        (*(short *)(param_1 + 0x10) < *(short *)(iVar2 + 0x10))))) break;
    iVar2 = *(int *)(iVar2 + 0x18);
  }
  iVar1 = *(int *)(iVar2 + 0x14);
  *(int *)(param_1 + 0x14) = iVar1;
  *(int *)(param_1 + 0x18) = iVar2;
  *(int *)(iVar2 + 0x14) = param_1;
  if (iVar1 == 0) {
    *(int *)(DAT_02385910 + 0xc) = param_1;
    FUN_02385abc();
    return;
  }
  *(int *)(iVar1 + 0x18) = param_1;
  return;
}



// ---- FUN_02385914 @ 02385914 ----

void FUN_02385914(int param_1)

{
  int iVar1;
  int iVar2;
  
  iVar1 = DAT_0238594c;
  iVar2 = *(int *)(DAT_0238594c + 0x10);
  *(int *)(param_1 + 0x14) = iVar2;
  *(undefined4 *)(param_1 + 0x18) = 0;
  *(int *)(iVar1 + 0x10) = param_1;
  if (iVar2 == 0) {
    *(int *)(iVar1 + 0xc) = param_1;
    FUN_02385abc();
  }
  else {
    *(int *)(iVar2 + 0x18) = param_1;
  }
  return;
}



// ---- FUN_02385950 @ 02385950 ----

void FUN_02385950(int param_1)

{
  int iVar1;
  int iVar2;
  
  if (param_1 != 0) {
    iVar2 = *(int *)(param_1 + 0x18);
    iVar1 = *(int *)(param_1 + 0x14);
    if (iVar2 == 0) {
      *(int *)(DAT_02385984 + 0x10) = iVar1;
    }
    else {
      *(int *)(iVar2 + 0x14) = iVar1;
    }
    if (iVar1 == 0) {
      *(int *)(DAT_02385984 + 0xc) = iVar2;
    }
    else {
      *(int *)(iVar1 + 0x18) = iVar2;
    }
    return;
  }
  return;
}



// ---- FUN_02385988 @ 02385988 ----

void FUN_02385988(undefined4 *param_1)

{
  *param_1 = 0;
  param_1[2] = 0;
  param_1[8] = 0;
  return;
}



// ---- FUN_0238599c @ 0238599c ----

void FUN_0238599c(int *param_1,int param_2,undefined2 param_3,int param_4,int param_5)

{
  ushort uVar1;
  undefined4 uVar2;
  int iVar3;
  
  uVar2 = FUN_02385e04();
  if ((param_1 == (int *)0x0) || (*param_1 != 0)) {
    FUN_02385f74();
  }
  uVar1 = *DAT_02385a28;
  iVar3 = FUN_02385dac((uint)uVar1);
  param_1[7] = 0;
  *(short *)(param_1 + 4) = (short)param_2;
  if (param_2 <= (int)(uint)uVar1) {
    iVar3 = iVar3 + 1;
  }
  param_1[3] = iVar3;
  *(undefined2 *)((int)param_1 + 0x12) = param_3;
  *param_1 = param_4;
  param_1[1] = param_5;
  param_1[9] = 0;
  FUN_02385898(param_1);
  FUN_02385e18(uVar2);
  return;
}



// ---- FUN_02385abc @ 02385abc ----

void FUN_02385abc(int param_1)

{
  ushort *puVar1;
  
  FUN_02383934(4,DAT_02385b10);
  puVar1 = DAT_02385b14;
  *DAT_02385b14 =
       *DAT_02385b14 & 0x3f | (ushort)((uint)((int)*(short *)(param_1 + 0x10) << 0x18) >> 0x10) |
       (ushort)((int)((int)*(short *)(param_1 + 0x10) & 0x100U) >> 1);
  *puVar1 = *puVar1 | 0x20;
  FUN_02383a68(4);
  return;
}



// ---- FUN_02385b18 @ 02385b18 ----

void FUN_02385b18(int param_1,int param_2)

{
  if (param_2 == 0) {
    FUN_02385f74();
  }
  if (param_1 != 0) {
    *(int *)(param_1 + 8) = param_2;
  }
  return;
}



// ---- FUN_02385b3c @ 02385b3c ----

void FUN_02385b3c(int *param_1)

{
  undefined4 uVar1;
  
  uVar1 = FUN_02385e04();
  param_1[9] = 1;
  if (*param_1 == 0) {
    FUN_02385e18();
  }
  else {
    FUN_02385950(param_1);
    *param_1 = 0;
    FUN_02385e18(uVar1);
  }
  return;
}



// ---- FUN_02385b88 @ 02385b88 ----

void FUN_02385b88(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  
  uVar1 = FUN_02385e04();
  if (param_1 == 0) {
    FUN_02385f74();
  }
  iVar2 = *(int *)(DAT_02385bf8 + 0xc);
  if (iVar2 == 0) {
    iVar3 = 0;
  }
  else {
    iVar3 = *(int *)(iVar2 + 0x18);
  }
  while (iVar2 != 0) {
    if (*(int *)(iVar2 + 8) == param_1) {
      FUN_02385b3c();
    }
    iVar2 = iVar3;
    if (iVar3 == 0) {
      iVar3 = 0;
    }
    else {
      iVar3 = *(int *)(iVar3 + 0x18);
    }
  }
  FUN_02385e18(uVar1);
  return;
}



// ---- FUN_02385dac @ 02385dac ----

undefined4 FUN_02385dac(int param_1)

{
  FUN_02385e04();
  if (param_1 < *(int *)(DAT_02385dec + 4)) {
    *(int *)(DAT_02385dec + 8) = *(int *)(DAT_02385dec + 8) + 1;
  }
  *(int *)(DAT_02385dec + 4) = param_1;
  FUN_02385e18();
  return *(undefined4 *)(DAT_02385dec + 8);
}



// ---- FUN_02385df0 @ 02385df0 ----

longlong FUN_02385df0(void)

{
  char in_NG;
  char in_ZR;
  char in_CY;
  char in_OV;
  byte in_Q;
  
  return (ulonglong)((uint)(byte)(in_NG << 4 | in_ZR << 3 | in_CY << 2 | in_OV << 1 | in_Q) << 0x1b)
         << 0x20;
}



// ---- FUN_02385e04 @ 02385e04 ----

longlong FUN_02385e04(void)

{
  char in_NG;
  char in_ZR;
  char in_CY;
  char in_OV;
  byte in_Q;
  
  return (ulonglong)
         ((uint)(byte)(in_NG << 4 | in_ZR << 3 | in_CY << 2 | in_OV << 1 | in_Q) << 0x1b | 0x80) <<
         0x20;
}



// ---- FUN_02385e18 @ 02385e18 ----

undefined4 FUN_02385e18(void)

{
  return 0;
}



// ---- FUN_02385e30 @ 02385e30 ----

longlong FUN_02385e30(void)

{
  char in_NG;
  char in_ZR;
  char in_CY;
  char in_OV;
  byte in_Q;
  
  return (ulonglong)
         ((uint)(byte)(in_NG << 4 | in_ZR << 3 | in_CY << 2 | in_OV << 1 | in_Q) << 0x1b | 0xc0) <<
         0x20;
}



// ---- FUN_02385e44 @ 02385e44 ----

undefined4 FUN_02385e44(void)

{
  return 0;
}



// ---- FUN_02385e5c @ 02385e5c ----

undefined4 FUN_02385e5c(void)

{
  return 0;
}



// ---- FUN_02385e68 @ 02385e68 ----

void FUN_02385e68(int param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02385e78. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02385e7c)((int)(param_1 + ((uint)(param_1 >> 1) >> 0x1e)) >> 2);
  return;
}



// ---- FUN_02385e80 @ 02385e80 ----

void FUN_02385e80(void)

{
  short *psVar1;
  undefined4 uVar2;
  undefined4 in_r3;
  
  uVar2 = DAT_02385eb4;
  psVar1 = DAT_02385eb0;
  if (*DAT_02385eb0 == 0) {
    *DAT_02385eb0 = 1;
    FUN_023863d8(0xc,uVar2,psVar1,1,in_r3);
  }
  return;
}



// ---- FUN_02385eb8 @ 02385eb8 ----

undefined2 FUN_02385eb8(void)

{
  return *(undefined2 *)(DAT_02385ec4 + 2);
}



// ---- FUN_02385efc @ 02385efc ----

void FUN_02385efc(void)

{
  int iVar1;
  
  FUN_02385ff8(0);
  FUN_02385ff8(1);
  FUN_02385ff8(2);
  FUN_02385ff8(3);
  FUN_02383a1c(0x40000);
  FUN_02383adc(0xffffffff);
  FUN_023866f0();
  do {
    iVar1 = FUN_0238644c(0xc,0x1000,0);
  } while (iVar1 != 0);
  *DAT_02385f70 = 0;
  FUN_0238efc0();
  return;
}



// ---- FUN_02385f74 @ 02385f74 ----

void FUN_02385f74(void)

{
  FUN_0238e310(0);
  do {
    FUN_02385e04();
    thunk_EXT_FUN_0380356e();
  } while( true );
}



// ---- FUN_02385f8c @ 02385f8c ----

void FUN_02385f8c(int param_1)

{
  FUN_02385e04();
  do {
  } while ((*(uint *)((param_1 * 3 + 2) * 4 + 0x40000b0) & 0x80000000) != 0);
  if (param_1 == 0) {
    uRam040000b0 = 0;
    uRam040000b4 = 0;
    uRam040000b8 = DAT_02385ff4;
  }
  FUN_02385e18();
  return;
}



// ---- FUN_02385ff8 @ 02385ff8 ----

void FUN_02385ff8(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  uint uVar4;
  
  uVar2 = FUN_02385e04();
  iVar1 = (param_1 * 6 + 5) * 2;
  *(ushort *)(iVar1 + 0x40000b0) = *(ushort *)(iVar1 + 0x40000b0) & 0xcdff;
  *(ushort *)(iVar1 + 0x40000b0) = *(ushort *)(iVar1 + 0x40000b0) & 0x7fff;
  uVar4 = (uint)*(ushort *)(iVar1 + 0x40000b0);
  uVar3 = (uint)*(ushort *)(iVar1 + 0x40000b0);
  if (param_1 == 0) {
    uRam040000b0 = 0;
    uVar4 = 0x40000b0;
    uRam040000b4 = 0;
    uRam040000b8 = DAT_02386074;
    uVar3 = DAT_02386074;
  }
  FUN_02385e18(uVar2,uVar3,uVar4);
  return;
}



// ---- FUN_023860ac @ 023860ac ----

void FUN_023860ac(undefined4 param_1,undefined4 *param_2,int param_3)

{
  param_3 = (int)param_2 + param_3;
  for (; (int)param_2 < param_3; param_2 = param_2 + 1) {
    *param_2 = param_1;
  }
  return;
}



// ---- FUN_023860c0 @ 023860c0 ----

void FUN_023860c0(undefined4 *param_1,undefined4 *param_2,int param_3)

{
  undefined4 uVar1;
  
  param_3 = (int)param_2 + param_3;
  for (; (int)param_2 < param_3; param_2 = param_2 + 1) {
    uVar1 = *param_1;
    param_1 = param_1 + 1;
    *param_2 = uVar1;
  }
  return;
}



// ---- FUN_02386124 @ 02386124 ----

void FUN_02386124(uint *param_1,uint param_2,uint param_3)

{
  uint *puVar1;
  uint *puVar2;
  uint uVar3;
  uint *puVar4;
  
  if (param_3 == 0) {
    return;
  }
  if (((uint)param_1 & 1) != 0) {
    *(ushort *)((int)param_1 + -1) = *(ushort *)((int)param_1 + -1) & 0xff | (ushort)(param_2 << 8);
    param_1 = (uint *)((int)param_1 + 1);
    param_3 = param_3 - 1;
    if (param_3 == 0) {
      return;
    }
  }
  if (1 < param_3) {
    uVar3 = param_2 | param_2 << 8;
    puVar1 = param_1;
    if (((uint)param_1 & 2) != 0) {
      puVar1 = (uint *)((int)param_1 + 2);
      *(ushort *)param_1 = (ushort)uVar3;
      param_3 = param_3 - 2;
      if (param_3 == 0) {
        return;
      }
    }
    param_2 = uVar3 | uVar3 << 0x10;
    if ((param_3 & 0xfffffffc) != 0) {
      puVar4 = (uint *)((param_3 & 0xfffffffc) + (int)puVar1);
      puVar2 = puVar1;
      do {
        puVar1 = puVar2 + 1;
        *puVar2 = param_2;
        puVar2 = puVar1;
      } while (puVar1 < puVar4);
    }
    param_1 = puVar1;
    if ((param_3 & 2) != 0) {
      param_1 = (uint *)((int)puVar1 + 2);
      *(ushort *)puVar1 = (ushort)uVar3;
    }
  }
  if ((param_3 & 1) == 0) {
    return;
  }
  *(ushort *)param_1 = (ushort)param_2 & 0xff | (ushort)*param_1 & 0xff00;
  return;
}



// ---- FUN_023861b8 @ 023861b8 ----

void FUN_023861b8(ushort *param_1,ushort *param_2,uint param_3)

{
  ushort uVar1;
  ushort uVar2;
  ushort *puVar3;
  ushort *puVar4;
  ushort *puVar5;
  ushort *puVar6;
  ushort *puVar7;
  
  if (param_3 == 0) {
    return;
  }
  if (((uint)param_2 & 1) != 0) {
    if (((uint)param_1 & 1) == 0) {
      uVar1 = *param_1;
    }
    else {
      uVar1 = *(ushort *)((int)param_1 + -1) >> 8;
    }
    *(ushort *)((int)param_2 + -1) = *(ushort *)((int)param_2 + -1) & 0xff | uVar1 << 8;
    param_1 = (ushort *)((int)param_1 + 1);
    param_2 = (ushort *)((int)param_2 + 1);
    param_3 = param_3 - 1;
    if (param_3 == 0) {
      return;
    }
  }
  if ((((uint)param_2 ^ (uint)param_1) & 1) == 0) {
    puVar3 = param_2;
    if ((((uint)param_2 ^ (uint)param_1) & 2) == 0) {
      if (1 < param_3) {
        puVar4 = param_1;
        puVar6 = param_2;
        if (((uint)param_2 & 2) != 0) {
          puVar4 = param_1 + 1;
          puVar6 = param_2 + 1;
          *param_2 = *param_1;
          param_3 = param_3 - 2;
          if (param_3 == 0) {
            return;
          }
        }
        if ((param_3 & 0xfffffffc) != 0) {
          puVar7 = (ushort *)((param_3 & 0xfffffffc) + (int)puVar6);
          puVar3 = puVar4;
          puVar5 = puVar6;
          do {
            puVar4 = puVar3 + 2;
            puVar6 = puVar5 + 2;
            *(undefined4 *)puVar5 = *(undefined4 *)puVar3;
            puVar3 = puVar4;
            puVar5 = puVar6;
          } while (puVar6 < puVar7);
        }
        param_1 = puVar4;
        puVar3 = puVar6;
        if ((param_3 & 2) != 0) {
          param_1 = puVar4 + 1;
          puVar3 = puVar6 + 1;
          *puVar6 = *puVar4;
        }
      }
    }
    else if ((param_3 & 0xfffffffe) != 0) {
      puVar4 = param_1;
      puVar6 = param_2;
      do {
        param_1 = puVar4 + 1;
        puVar3 = puVar6 + 1;
        *puVar6 = *puVar4;
        puVar4 = param_1;
        puVar6 = puVar3;
      } while (puVar3 < (ushort *)((param_3 & 0xfffffffe) + (int)param_2));
    }
    if ((param_3 & 1) != 0) {
      *puVar3 = *puVar3 & 0xff00 | *param_1 & 0xff;
      return;
    }
    return;
  }
  param_1 = (ushort *)((uint)param_1 & 0xfffffffe);
  uVar1 = *param_1;
  while( true ) {
    uVar2 = uVar1 >> 8;
    if (param_3 < 2) break;
    param_1 = param_1 + 1;
    uVar1 = *param_1;
    *param_2 = uVar2 | uVar1 << 8;
    param_2 = param_2 + 1;
    param_3 = param_3 - 2;
  }
  if ((param_3 - 2 & 1) != 0) {
    *param_2 = *param_2 & 0xff00 | uVar2;
    return;
  }
  return;
}



// ---- FUN_023862e8 @ 023862e8 ----

undefined4 FUN_023862e8(undefined4 param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  
  uVar1 = *param_2;
  *param_2 = param_1;
  return uVar1;
}



// ---- thunk_EXT_FUN_037fe14c @ 023862f0 ----

void thunk_EXT_FUN_037fe14c(void)

{
                    /* WARNING: Could not recover jumptable at 0x023862f4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_023862f8)();
  return;
}



// ---- FUN_023863d8 @ 023863d8 ----

void FUN_023863d8(uint param_1,int param_2)

{
  int iVar1;
  uint uVar2;
  
  FUN_02385e04();
  iVar1 = DAT_02386424;
  *(int *)(DAT_02386420 + param_1 * 4) = param_2;
  if (param_2 == 0) {
    uVar2 = *(uint *)(iVar1 + 0x38c) & ~(1 << (param_1 & 0xff));
  }
  else {
    uVar2 = *(uint *)(iVar1 + 0x38c) | 1 << (param_1 & 0xff);
  }
  *(uint *)(iVar1 + 0x38c) = uVar2;
  FUN_02385e18();
  return;
}



// ---- FUN_02386428 @ 02386428 ----

bool FUN_02386428(uint param_1,int param_2)

{
  return (*(uint *)(DAT_02386448 + param_2 * 4 + 0x388) & 1 << (param_1 & 0xff)) != 0;
}



// ---- FUN_0238644c @ 0238644c ----

void FUN_0238644c(void)

{
  FUN_02386484();
  return;
}



// ---- FUN_02386484 @ 02386484 ----

undefined4 FUN_02386484(undefined4 param_1)

{
  undefined4 uVar1;
  
  if ((*DAT_023864e0 & 0x4000) == 0) {
    FUN_02385e04(*DAT_023864e0);
    if ((*DAT_023864e0 & 2) == 0) {
      *(undefined4 *)(DAT_023864e0 + 2) = param_1;
      FUN_02385e18();
      uVar1 = 0;
    }
    else {
      FUN_02385e18();
      uVar1 = 0xfffffffe;
    }
  }
  else {
    uVar1 = 0xffffffff;
    *DAT_023864e0 = *DAT_023864e0 | 0xc000;
  }
  return uVar1;
}



// ---- FUN_023865fc @ 023865fc ----

undefined4 FUN_023865fc(void)

{
  int iVar1;
  undefined4 uVar2;
  longlong lVar3;
  
  iVar1 = FUN_02385294();
  if ((iVar1 == 0) || (iVar1 = FUN_02385480(), iVar1 == 0)) {
    uVar2 = 0;
  }
  else if (*DAT_02386688 == 0) {
    FUN_02385490(DAT_0238668c);
    lVar3 = FUN_0238530c();
    FUN_0238563c(DAT_0238668c,(int)(lVar3 + (ulonglong)DAT_02386694),
                 (int)(lVar3 + (ulonglong)DAT_02386694 >> 0x20),DAT_02386694,0,DAT_02386690,0);
    uVar2 = 1;
    *DAT_02386688 = 1;
  }
  else {
    uVar2 = 0;
  }
  return uVar2;
}



// ---- FUN_023866f0 @ 023866f0 ----

void FUN_023866f0(void)

{
  undefined1 *puVar1;
  int iVar2;
  
  iVar2 = 0;
  *DAT_0238673c = *DAT_0238673c & 0x7f;
  do {
    FUN_02386a5c(iVar2,1);
    puVar1 = DAT_02386740;
    iVar2 = iVar2 + 1;
  } while (iVar2 < 0x10);
  *DAT_02386740 = 0;
  puVar1[1] = 0;
  return;
}



// ---- FUN_02386744 @ 02386744 ----

void FUN_02386744(void)

{
  *DAT_02386788 = *DAT_02386788 & 0x7f;
  thunk_EXT_FUN_03803582(0x80);
  FUN_02385e68(0x40000);
  FUN_0238cc98(1);
  *DAT_0238678c = *DAT_0238678c & 0xfffe;
  return;
}



// ---- thunk_EXT_FUN_03803582 @ 02386790 ----

void thunk_EXT_FUN_03803582(void)

{
                    /* WARNING: Could not recover jumptable at 0x02386794. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02386798)();
  return;
}



// ---- FUN_02386a5c @ 02386a5c ----

void FUN_02386a5c(int param_1,uint param_2)

{
  uint uVar1;
  
  uVar1 = *(uint *)(param_1 * 0x10 + 0x4000400) & 0x7fffffff;
  if ((param_2 & 1) != 0) {
    uVar1 = uVar1 | 0x8000;
  }
  *(uint *)(param_1 * 0x10 + 0x4000400) = uVar1;
  return;
}



// ---- FUN_02386a84 @ 02386a84 ----

void FUN_02386a84(uint param_1,undefined4 param_2,short param_3,undefined4 param_4)

{
  undefined1 uVar1;
  int iVar2;
  
  iVar2 = *DAT_02386af0;
  *(char *)(DAT_02386af4 + param_1) = (char)param_2;
  if ((0 < iVar2) && ((DAT_02386af8 & 1 << (param_1 & 0xff)) != 0)) {
    uVar1 = *(undefined1 *)(param_1 * 0x10 + 0x4000402);
    param_2 = FUN_02386c7c(param_2,uVar1,uVar1,iVar2,param_4);
  }
  *(ushort *)(param_1 * 0x10 + 0x4000400) = (ushort)param_2 | param_3 << 8;
  return;
}



// ---- FUN_02386b14 @ 02386b14 ----

void FUN_02386b14(uint param_1,int param_2)

{
  int *piVar1;
  undefined1 uVar2;
  int iVar3;
  
  iVar3 = *DAT_02386b78;
  *(char *)(DAT_02386b7c + param_1) = (char)param_2;
  piVar1 = DAT_02386b80;
  if (-1 < iVar3) {
    param_2 = iVar3;
  }
  *(char *)(param_1 * 0x10 + 0x4000402) = (char)param_2;
  if ((0 < *piVar1) && ((DAT_02386b84 & 1 << (param_1 & 0xff)) != 0)) {
    uVar2 = FUN_02386c7c(*(undefined1 *)(DAT_02386b88 + param_1));
    *(undefined1 *)(param_1 * 0x10 + 0x4000400) = uVar2;
  }
  return;
}



// ---- FUN_02386c1c @ 02386c1c ----

void FUN_02386c1c(undefined4 param_1)

{
  int iVar1;
  uint uVar2;
  undefined1 uVar3;
  uint uVar4;
  
  uVar2 = DAT_02386c78;
  iVar1 = DAT_02386c74;
  *DAT_02386c70 = param_1;
  uVar4 = 0;
  do {
    if ((uVar2 & 1 << (uVar4 & 0xff)) != 0) {
      uVar3 = FUN_02386c7c(*(undefined1 *)(iVar1 + uVar4),*(undefined1 *)(uVar4 * 0x10 + 0x4000402))
      ;
      *(undefined1 *)(uVar4 * 0x10 + 0x4000400) = uVar3;
    }
    uVar4 = uVar4 + 1;
  } while ((int)uVar4 < 0x10);
  return;
}



// ---- FUN_02386c7c @ 02386c7c ----

int FUN_02386c7c(int param_1,int param_2)

{
  if (param_2 < 0x18) {
    return param_1 * (*DAT_02386ce0 * (param_2 + 0x28) + (DAT_02386ce4 - *DAT_02386ce0) * 0x40) >>
           0x15;
  }
  if (param_2 < 0x69) {
    return param_1;
  }
  return param_1 * (-*DAT_02386ce0 * (param_2 + -0x28) + (*DAT_02386ce0 + 0x7fff) * 0x40) >> 0x15;
}



// ---- FUN_02386e94 @ 02386e94 ----

int FUN_02386e94(int param_1)

{
  if (param_1 < 0x20) {
    return (int)*(char *)(DAT_02386efc + param_1);
  }
  if (0x3f < param_1) {
    if (0x5f < param_1) {
      return *(char *)(DAT_02386efc + (0x20 - (param_1 + -0x60))) * -0x1000000 >> 0x18;
    }
    return *(char *)(DAT_02386efc + param_1 + -0x40) * -0x1000000 >> 0x18;
  }
  return (int)*(char *)(DAT_02386efc + (0x40 - param_1));
}



// ---- FUN_02386f00 @ 02386f00 ----

uint FUN_02386f00(void)

{
  uint uVar1;
  
  uVar1 = *DAT_02386f28 * DAT_02386f2c + DAT_02386f30;
  *DAT_02386f28 = uVar1;
  return uVar1 >> 0x10;
}



// ---- FUN_02386f34 @ 02386f34 ----

void FUN_02386f34(undefined4 param_1)

{
  if (*DAT_02386f90 == 0) {
    *DAT_02386f90 = 1;
    FUN_02389f14();
    FUN_0238415c(DAT_02386f94,DAT_02386f98,0,DAT_02386f9c,0x400,param_1);
    FUN_02384474(DAT_02386f94);
  }
  return;
}



// ---- FUN_02387020 @ 02387020 ----

void FUN_02387020(void)

{
  return;
}



// ---- FUN_02387024 @ 02387024 ----

void FUN_02387024(void)

{
  return;
}



// ---- FUN_023871a0 @ 023871a0 ----

void FUN_023871a0(void)

{
  int iVar1;
  undefined4 *puVar2;
  int iVar3;
  int iVar4;
  
  iVar1 = DAT_023871f4;
  iVar4 = 0;
  do {
    iVar3 = iVar1 + iVar4 * 0x54;
    *(char *)(iVar1 + iVar4 * 0x54) = (char)iVar4;
    iVar4 = iVar4 + 1;
    *(byte *)(iVar3 + 3) = *(byte *)(iVar3 + 3) & 6;
    puVar2 = DAT_023871f8;
  } while (iVar4 < 0x10);
  DAT_023871f8[1] = 0;
  *puVar2 = 0;
  return;
}



// ---- FUN_0238779c @ 0238779c ----

undefined4 FUN_0238779c(int param_1,undefined4 *param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  *(undefined1 *)(param_1 + 1) = 0;
  uVar1 = param_2[1];
  uVar2 = param_2[2];
  *(undefined4 *)(param_1 + 0x38) = *param_2;
  *(undefined4 *)(param_1 + 0x3c) = uVar1;
  *(undefined4 *)(param_1 + 0x40) = uVar2;
  *(undefined4 *)(param_1 + 0x44) = param_3;
  FUN_02387ef4(param_1,param_4);
  return 1;
}



// ---- FUN_023877d8 @ 023877d8 ----

undefined4 FUN_023877d8(byte *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  
  if (*param_1 < 8) {
    uVar1 = 0;
  }
  else if (*param_1 < 0xe) {
    param_1[1] = 1;
    *(undefined4 *)(param_1 + 0x44) = param_2;
    uVar1 = DAT_02387820;
    *(short *)(param_1 + 0x3c) = (short)DAT_02387820;
    FUN_02387ef4(param_1,param_3,param_3,uVar1,param_4);
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}



// ---- FUN_02387824 @ 02387824 ----

undefined4 FUN_02387824(byte *param_1)

{
  undefined4 uVar1;
  
  uVar1 = DAT_02387864;
  if (*param_1 < 0xe) {
    uVar1 = 0;
  }
  else if (*param_1 < 0x10) {
    param_1[1] = 2;
    *(short *)(param_1 + 0x3c) = (short)uVar1;
    FUN_02387ef4();
    uVar1 = 1;
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}



// ---- FUN_02387910 @ 02387910 ----

void FUN_02387910(int param_1,int param_2)

{
  char cVar1;
  
  if (param_2 < 0x6d) {
    cVar1 = -1 - (char)param_2;
  }
  else {
    cVar1 = *(char *)(DAT_0238792c + (0x7f - param_2));
  }
  *(char *)(param_1 + 0x1c) = cVar1;
  return;
}



// ---- FUN_02387930 @ 02387930 ----

void FUN_02387930(int param_1,undefined4 param_2)

{
  undefined2 uVar1;
  
  uVar1 = FUN_02387ea0(param_2);
  *(undefined2 *)(param_1 + 0x1e) = uVar1;
  return;
}



// ---- FUN_0238794c @ 0238794c ----

void FUN_0238794c(int param_1,undefined1 param_2)

{
  *(undefined1 *)(param_1 + 0x1d) = param_2;
  return;
}



// ---- FUN_02387954 @ 02387954 ----

void FUN_02387954(int param_1,undefined4 param_2)

{
  undefined2 uVar1;
  
  uVar1 = FUN_02387ea0(param_2);
  *(undefined2 *)(param_1 + 0x20) = uVar1;
  return;
}



// ---- FUN_02387970 @ 02387970 ----

void FUN_02387970(int param_1)

{
  *(undefined1 *)(param_1 + 2) = 3;
  return;
}



// ---- FUN_0238797c @ 0238797c ----

byte FUN_0238797c(int param_1)

{
  return *(byte *)(param_1 + 3) & 1;
}



// ---- FUN_0238798c @ 0238798c ----

int FUN_0238798c(uint param_1,int param_2,int param_3,undefined4 param_4,undefined4 param_5)

{
  undefined4 uVar1;
  int iVar2;
  uint uVar3;
  int iVar4;
  code *pcVar5;
  int iVar6;
  int iVar7;
  int iVar8;
  
  uVar3 = ~DAT_02387b44[1];
  param_1 = param_1 & uVar3;
  if (param_3 == 0) {
    uVar3 = *DAT_02387b44;
  }
  if (param_3 == 0) {
    param_1 = param_1 & ~uVar3;
  }
  iVar7 = 0;
  iVar6 = 0;
  do {
    iVar2 = iVar6;
    if ((((param_1 & 1 << (uint)*(byte *)(DAT_02387b4c + iVar7)) != 0) &&
        (iVar8 = (uint)*(byte *)(DAT_02387b4c + iVar7) * 0x54 + DAT_02387b50, iVar2 = iVar8,
        iVar6 != 0)) && (iVar2 = iVar6, *(byte *)(iVar8 + 0x22) <= *(byte *)(iVar6 + 0x22))) {
      if (*(byte *)(iVar8 + 0x22) == *(byte *)(iVar6 + 0x22)) {
        iVar2 = (int)((*(ushort *)(iVar6 + 0x24) & 0xff) << 4) >>
                *(sbyte *)(DAT_02387b48 + ((int)(uint)*(ushort *)(iVar6 + 0x24) >> 8));
        iVar4 = (int)((*(ushort *)(iVar8 + 0x24) & 0xff) << 4) >>
                *(sbyte *)(DAT_02387b48 + ((int)(uint)*(ushort *)(iVar8 + 0x24) >> 8));
        if (iVar2 == iVar4) {
          iVar4 = 0;
        }
        else if (iVar2 < iVar4) {
          iVar4 = 1;
        }
        else {
          iVar4 = -1;
        }
        iVar2 = iVar6;
        if (-1 < iVar4) goto LAB_02387a50;
      }
      iVar2 = iVar8;
    }
LAB_02387a50:
    iVar7 = iVar7 + 1;
    iVar6 = iVar2;
    if (0xf < iVar7) {
      if (iVar2 == 0) {
        iVar2 = 0;
      }
      else if (param_2 < (int)(uint)*(byte *)(iVar2 + 0x22)) {
        iVar2 = 0;
      }
      else {
        pcVar5 = *(code **)(iVar2 + 0x48);
        if (pcVar5 != (code *)0x0) {
          (*pcVar5)(iVar2,0,*(undefined4 *)(iVar2 + 0x4c),pcVar5,param_4);
        }
        *(byte *)(iVar2 + 3) = *(byte *)(iVar2 + 3) & 6 | 0x10;
        *(undefined4 *)(iVar2 + 0x50) = 0;
        *(undefined4 *)(iVar2 + 0x48) = param_4;
        *(undefined4 *)(iVar2 + 0x4c) = param_5;
        *(undefined4 *)(iVar2 + 0x34) = 0;
        *(char *)(iVar2 + 0x22) = (char)param_2;
        *(undefined2 *)(iVar2 + 0x24) = 0x7f;
        *(byte *)(iVar2 + 3) = *(byte *)(iVar2 + 3) & 0xfd | 4;
        *(undefined1 *)(iVar2 + 8) = 0x3c;
        *(undefined1 *)(iVar2 + 5) = 0x3c;
        *(undefined1 *)(iVar2 + 9) = 0x7f;
        *(undefined1 *)(iVar2 + 10) = 0;
        *(undefined2 *)(iVar2 + 0xc) = 0;
        *(undefined2 *)(iVar2 + 6) = 0;
        *(undefined2 *)(iVar2 + 0xe) = 0;
        *(undefined1 *)(iVar2 + 0xb) = 0;
        *(undefined1 *)(iVar2 + 4) = 0x7f;
        *(undefined2 *)(iVar2 + 0x32) = 0;
        *(undefined4 *)(iVar2 + 0x18) = 0;
        *(undefined4 *)(iVar2 + 0x14) = 0;
        uVar1 = DAT_02387b54;
        *(undefined1 *)(iVar2 + 0x1c) = 0;
        *(short *)(iVar2 + 0x1e) = (short)uVar1;
        *(undefined1 *)(iVar2 + 0x1d) = 0x7f;
        *(short *)(iVar2 + 0x20) = (short)uVar1;
        FUN_02387dcc(iVar2 + 0x28);
      }
      return iVar2;
    }
  } while( true );
}



// ---- FUN_02387b58 @ 02387b58 ----

void FUN_02387b58(int param_1)

{
  if (param_1 != 0) {
    *(undefined4 *)(param_1 + 0x48) = 0;
    *(undefined4 *)(param_1 + 0x4c) = 0;
  }
  return;
}



// ---- FUN_02387b6c @ 02387b6c ----

void FUN_02387b6c(uint param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  code *pcVar3;
  int iVar4;
  uint uVar5;
  
  iVar2 = DAT_02387c18;
  iVar1 = DAT_02387c14;
  uVar5 = 0;
  for (; ((int)uVar5 < 0x10 && (param_1 != 0)); param_1 = param_1 >> 1) {
    if (((param_1 & 1) != 0) &&
       (iVar4 = uVar5 * 0x54 + iVar1, (*(uint *)(iVar2 + 4) & 1 << (uVar5 & 0xff)) == 0)) {
      pcVar3 = *(code **)(iVar4 + 0x48);
      if (pcVar3 != (code *)0x0) {
        (*pcVar3)(iVar4,0,*(undefined4 *)(iVar4 + 0x4c),pcVar3,param_4);
      }
      FUN_02386a5c(uVar5,0);
      *(undefined1 *)(iVar4 + 0x22) = 0;
      FUN_02387b58(iVar4);
      *(byte *)(iVar4 + 3) = *(byte *)(iVar4 + 3) & 6;
    }
    uVar5 = uVar5 + 1;
  }
  return;
}



// ---- FUN_02387dcc @ 02387dcc ----

void FUN_02387dcc(undefined1 *param_1)

{
  *param_1 = 0;
  param_1[2] = 0;
  param_1[3] = 1;
  param_1[1] = 0x10;
  *(undefined2 *)(param_1 + 4) = 0;
  return;
}



// ---- FUN_02387e50 @ 02387e50 ----

int FUN_02387e50(int param_1)

{
  int iVar1;
  
  if (*(char *)(param_1 + 2) == '\0') {
    iVar1 = 0;
  }
  else if (*(ushort *)(param_1 + 6) < *(ushort *)(param_1 + 4)) {
    iVar1 = 0;
  }
  else {
    iVar1 = FUN_02386e94(*(ushort *)(param_1 + 8) >> 8);
    iVar1 = (uint)*(byte *)(param_1 + 3) * (uint)*(byte *)(param_1 + 2) * iVar1;
  }
  return iVar1;
}



// ---- FUN_02387ea0 @ 02387ea0 ----

uint FUN_02387ea0(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  uint uVar1;
  
  uVar1 = DAT_02387ef0;
  if (param_1 != 0x7f) {
    if (param_1 == 0x7e) {
      uVar1 = 0x3c00;
    }
    else if (param_1 < 0x32) {
      uVar1 = param_1 * 2 + 1U & 0xffff;
    }
    else {
      uVar1 = FUN_0238e8c8(0x1e00,0x7e - param_1,param_3,param_4,param_4);
      uVar1 = uVar1 & 0xffff;
    }
  }
  return uVar1;
}



// ---- FUN_02387ef4 @ 02387ef4 ----

void FUN_02387ef4(int param_1,undefined4 param_2)

{
  *(undefined4 *)(param_1 + 0x10) = DAT_02387f28;
  *(undefined1 *)(param_1 + 2) = 0;
  *(undefined4 *)(param_1 + 0x34) = param_2;
  *(undefined2 *)(param_1 + 0x30) = 0;
  *(undefined2 *)(param_1 + 0x2e) = 0;
  *(byte *)(param_1 + 3) = *(byte *)(param_1 + 3) & 0xfe | 3;
  return;
}



// ---- FUN_023882cc @ 023882cc ----

undefined1 FUN_023882cc(int param_1)

{
  undefined1 uVar1;
  uint uVar2;
  
  uVar2 = *(uint *)(param_1 + 0x28);
  if ((uVar2 < *(uint *)(DAT_02388324 + 4)) || (*(uint *)(DAT_02388324 + 8) <= uVar2)) {
    FUN_023887c0(uVar2);
  }
  uVar1 = *(undefined1 *)(DAT_02388328 + (uVar2 - *(int *)(DAT_02388324 + 4)));
  *(int *)(param_1 + 0x28) = *(int *)(param_1 + 0x28) + 1;
  return uVar1;
}



// ---- FUN_023887c0 @ 023887c0 ----

void FUN_023887c0(uint param_1)

{
  int iVar1;
  undefined4 *puVar2;
  
  iVar1 = DAT_023887f8;
  puVar2 = (undefined4 *)(param_1 & 0xfffffffc);
  *(undefined4 **)(DAT_023887f8 + 4) = puVar2;
  *(undefined4 **)(iVar1 + 8) = puVar2 + 4;
  *(undefined4 *)(iVar1 + 0xc) = *puVar2;
  *(undefined4 *)(iVar1 + 0x10) = puVar2[1];
  *(undefined4 *)(iVar1 + 0x14) = puVar2[2];
  *(undefined4 *)(iVar1 + 0x18) = puVar2[3];
  return;
}



// ---- FUN_0238882c @ 0238882c ----

uint FUN_0238882c(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  ushort uVar1;
  short sVar2;
  ushort uVar3;
  short sVar4;
  int iVar5;
  uint uVar6;
  undefined4 uVar7;
  short *psVar8;
  int iVar9;
  uint unaff_r5;
  
  switch(param_3) {
  case 0:
    unaff_r5 = FUN_023882cc();
    break;
  case 1:
    uVar6 = FUN_023882cc();
    iVar5 = FUN_023882cc(param_1);
    unaff_r5 = (uVar6 | iVar5 << 8) & 0xffff;
    break;
  case 2:
    unaff_r5 = 0;
    do {
      uVar6 = FUN_023882cc(param_1);
      unaff_r5 = uVar6 & 0x7f | unaff_r5 << 7;
    } while ((uVar6 & 0x80) != 0);
    break;
  case 3:
    uVar1 = FUN_023882cc();
    sVar2 = FUN_023882cc(param_1);
    uVar3 = FUN_023882cc(param_1);
    sVar4 = FUN_023882cc(param_1);
    iVar9 = FUN_02386f00();
    iVar5 = (int)(short)(uVar1 | sVar2 << 8);
    unaff_r5 = (iVar9 * (((short)(uVar3 | sVar4 << 8) - iVar5) + 1) >> 0x10) + iVar5;
    break;
  case 4:
    uVar7 = FUN_023882cc();
    psVar8 = (short *)FUN_0238987c(param_2,uVar7);
    if (psVar8 != (short *)0x0) {
      unaff_r5 = (uint)*psVar8;
    }
  }
  return unaff_r5;
}



// ---- FUN_0238892c @ 0238892c ----

void FUN_0238892c(byte *param_1)

{
  byte bVar1;
  
  param_1[0x24] = 0;
  param_1[0x25] = 0;
  param_1[0x26] = 0;
  param_1[0x27] = 0;
  param_1[0x28] = 0;
  param_1[0x29] = 0;
  param_1[0x2a] = 0;
  param_1[0x2b] = 0;
  bVar1 = *param_1;
  *param_1 = bVar1 | 2;
  *param_1 = bVar1 & 0xfb | 2;
  *param_1 = bVar1 & 0xf3 | 2;
  *param_1 = bVar1 & 0xe3 | 2;
  *param_1 = bVar1 & 0x43 | 0x42;
  param_1[0x3b] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[0x12] = 0x40;
  param_1[4] = 0x7f;
  param_1[5] = 0x7f;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[6] = 0;
  param_1[0xc] = 0;
  param_1[0xd] = 0;
  param_1[0xe] = 0xff;
  param_1[0xf] = 0xff;
  param_1[0x10] = 0xff;
  param_1[0x11] = 0xff;
  param_1[1] = 0x7f;
  param_1[7] = 2;
  param_1[0x14] = 0x3c;
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  param_1[0x13] = 0;
  param_1[0x1e] = 0xff;
  param_1[0x1f] = 0xff;
  FUN_02387dcc(param_1 + 0x18);
  param_1[0x20] = 0;
  param_1[0x21] = 0;
  param_1[0x22] = 0;
  param_1[0x23] = 0;
  param_1[0x3c] = 0;
  param_1[0x3d] = 0;
  param_1[0x3e] = 0;
  param_1[0x3f] = 0;
  return;
}



// ---- FUN_02388a1c @ 02388a1c ----

void FUN_02388a1c(int param_1,undefined4 param_2,uint param_3,undefined4 param_4)

{
  int iVar1;
  int iVar2;
  
  FUN_02388bd4(param_1,param_2,0,param_4,param_4);
  for (iVar2 = *(int *)(param_1 + 0x3c); iVar2 != 0; iVar2 = *(int *)(iVar2 + 0x50)) {
    iVar1 = FUN_0238797c(iVar2);
    if (iVar1 != 0) {
      if (-1 < (int)param_3) {
        FUN_02387954(iVar2,param_3 & 0xff);
      }
      *(undefined1 *)(iVar2 + 0x22) = 1;
      FUN_02387970(iVar2);
    }
  }
  return;
}



// ---- FUN_02388a84 @ 02388a84 ----

void FUN_02388a84(int param_1)

{
  int iVar1;
  
  for (iVar1 = *(int *)(param_1 + 0x3c); iVar1 != 0; iVar1 = *(int *)(iVar1 + 0x50)) {
    FUN_02387b58(iVar1);
  }
  *(undefined4 *)(param_1 + 0x3c) = 0;
  return;
}



// ---- FUN_02388b74 @ 02388b74 ----

void FUN_02388b74(int param_1,int param_2,int param_3)

{
  int iVar1;
  int iVar2;
  
  if (param_2 == 1) {
    *(undefined1 *)(param_1 + 0x22) = 0;
    FUN_02387b58();
  }
  iVar1 = *(int *)(param_3 + 0x3c);
  if (*(int *)(param_3 + 0x3c) == param_1) {
    *(undefined4 *)(param_3 + 0x3c) = *(undefined4 *)(param_1 + 0x50);
  }
  else {
    do {
      iVar2 = iVar1;
      iVar1 = *(int *)(iVar2 + 0x50);
      if (iVar1 == 0) {
        return;
      }
    } while (iVar1 != param_1);
    *(undefined4 *)(iVar2 + 0x50) = *(undefined4 *)(param_1 + 0x50);
  }
  return;
}



// ---- FUN_02388bd4 @ 02388bd4 ----

void FUN_02388bd4(int param_1,int param_2,int param_3)

{
  byte bVar1;
  char cVar2;
  short sVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  uint uVar7;
  int iVar8;
  
  bVar1 = *(byte *)(param_1 + 7);
  uVar7 = (uint)*(byte *)(param_1 + 1);
  cVar2 = *(char *)(param_1 + 6);
  iVar6 = (int)*(char *)(param_1 + 8);
  if (uVar7 != 0x7f) {
    iVar6 = iVar6 * uVar7 + 0x40;
  }
  sVar3 = *(short *)(param_1 + 0xc);
  if (uVar7 != 0x7f) {
    iVar6 = iVar6 >> 7;
  }
  iVar4 = (int)*(short *)(DAT_02388d28 + (uint)*(byte *)(param_2 + 5) * 2) +
          (int)*(short *)(DAT_02388d28 + (uint)*(byte *)(param_1 + 4) * 2) +
          (int)*(short *)(DAT_02388d28 + (uint)*(byte *)(param_1 + 5) * 2);
  if (iVar4 < -0x8000) {
    iVar4 = -0x8000;
  }
  iVar5 = (int)*(short *)(param_1 + 10) + (int)*(short *)(param_2 + 6);
  if (iVar5 < -0x8000) {
    iVar5 = -0x8000;
  }
  iVar6 = iVar6 + *(char *)(param_1 + 9);
  if (iVar6 < -0x80) {
    iVar6 = -0x80;
  }
  else if (0x7f < iVar6) {
    iVar6 = 0x7f;
  }
  for (iVar8 = *(int *)(param_1 + 0x3c); iVar8 != 0; iVar8 = *(int *)(iVar8 + 0x50)) {
    *(short *)(iVar8 + 6) = (short)iVar5;
    if (*(char *)(iVar8 + 2) != '\x03') {
      *(short *)(iVar8 + 0xc) = (short)iVar4;
      *(short *)(iVar8 + 0xe) =
           (short)((uint)(((int)sVar3 + ((int)((int)cVar2 * (uint)bVar1 * 0x40) >> 7)) * 0x10000) >>
                  0x10);
      *(char *)(iVar8 + 0xb) = (char)iVar6;
      *(undefined1 *)(iVar8 + 4) = *(undefined1 *)(param_1 + 1);
      *(undefined2 *)(iVar8 + 0x28) = *(undefined2 *)(param_1 + 0x18);
      *(undefined2 *)(iVar8 + 0x2a) = *(undefined2 *)(param_1 + 0x1a);
      *(undefined2 *)(iVar8 + 0x2c) = *(undefined2 *)(param_1 + 0x1c);
      if ((*(int *)(iVar8 + 0x34) == 0) && (param_3 != 0)) {
        *(undefined1 *)(iVar8 + 0x22) = 1;
        FUN_02387970(iVar8);
      }
    }
  }
  return;
}



// ---- FUN_0238987c @ 0238987c ----

int FUN_0238987c(int param_1,int param_2)

{
  int iVar1;
  
  iVar1 = *DAT_023898bc;
  if (iVar1 == 0) {
    return 0;
  }
  if (param_2 < 0x10) {
    return (uint)*(byte *)(param_1 + 1) * 0x24 + iVar1 + 0x20 + param_2 * 2;
  }
  return iVar1 + 0x260 + (param_2 + -0x10) * 2;
}



// ---- FUN_02389984 @ 02389984 ----

undefined4 FUN_02389984(int param_1,uint param_2,int param_3,undefined2 *param_4)

{
  uint uVar1;
  undefined2 *puVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  
  if ((int)param_2 < 0) {
    return 0;
  }
  FUN_02387020(param_1);
  if (*(uint *)(param_1 + 0x38) <= param_2) {
    FUN_02387024();
    return 0;
  }
  uVar3 = *(uint *)(param_1 + param_2 * 4 + 0x3c);
  *(char *)param_4 = (char)uVar3;
  uVar1 = uVar3 >> 8;
  switch(uVar3 & 0xff) {
  case 0:
    break;
  case 1:
    goto LAB_02389a24;
  case 2:
    goto LAB_02389a24;
  case 3:
    goto LAB_02389a24;
  case 4:
    goto LAB_02389a24;
  case 5:
LAB_02389a24:
    iVar4 = 5;
    puVar2 = (undefined2 *)(param_1 + uVar1);
    do {
      param_4 = param_4 + 1;
      iVar4 = iVar4 + -1;
      *param_4 = *puVar2;
      puVar2 = puVar2 + 1;
    } while (iVar4 != 0);
LAB_02389af4:
    FUN_02387024();
    return 1;
  case 6:
    break;
  case 7:
    break;
  case 8:
    break;
  case 9:
    break;
  case 10:
    break;
  case 0xb:
    break;
  case 0xc:
    break;
  case 0xd:
    break;
  case 0xe:
    break;
  case 0xf:
    break;
  case 0x10:
    if ((param_3 < (int)(uint)*(byte *)(param_1 + uVar1)) ||
       ((int)(uint)*(byte *)(param_1 + uVar1 + 1) < param_3)) {
      FUN_02387024();
      return 0;
    }
    puVar2 = (undefined2 *)((param_3 - (uint)*(byte *)(param_1 + uVar1)) * 0xc + param_1 + uVar1);
    iVar4 = 6;
    do {
      puVar2 = puVar2 + 1;
      iVar4 = iVar4 + -1;
      *param_4 = *puVar2;
      param_4 = param_4 + 1;
    } while (iVar4 != 0);
    goto LAB_02389af4;
  case 0x11:
    iVar4 = 0;
    while ((int)(uint)*(byte *)(param_1 + uVar1 + iVar4) < param_3) {
      iVar4 = iVar4 + 1;
      if (7 < iVar4) {
        FUN_02387024();
        return 0;
      }
    }
    iVar5 = 6;
    puVar2 = (undefined2 *)(iVar4 * 0xc + param_1 + uVar1 + 8);
    do {
      iVar5 = iVar5 + -1;
      *param_4 = *puVar2;
      puVar2 = puVar2 + 1;
      param_4 = param_4 + 1;
    } while (iVar5 != 0);
    goto LAB_02389af4;
  }
  FUN_02387024();
  return 0;
}



// ---- FUN_02389b04 @ 02389b04 ----

uint FUN_02389b04(int param_1,int param_2)

{
  uint uVar1;
  
  FUN_02387020();
  uVar1 = *(uint *)(param_1 + param_2 * 4 + 0x3c);
  if (uVar1 == 0) {
    uVar1 = 0;
  }
  else if (uVar1 < 0x2000000) {
    uVar1 = param_1 + uVar1;
  }
  FUN_02387024();
  return uVar1;
}



// ---- FUN_02389b44 @ 02389b44 ----

bool FUN_02389b44(int param_1,undefined1 param_2,undefined4 param_3,undefined4 param_4,int param_5,
                 char *param_6)

{
  int iVar1;
  char cVar2;
  undefined4 uVar3;
  
  cVar2 = param_6[10];
  uVar3 = param_4;
  if (cVar2 == -1) {
    uVar3 = 0xffffffff;
    cVar2 = '\0';
  }
  switch(*param_6) {
  case '\0':
  default:
    iVar1 = 0;
    break;
  case '\x01':
    goto LAB_02389b90;
  case '\x02':
    iVar1 = FUN_023877d8(param_1,*(undefined2 *)(param_6 + 2),uVar3);
    break;
  case '\x03':
    iVar1 = FUN_02387824(param_1,uVar3,param_3,param_4,param_4);
    break;
  case '\x04':
LAB_02389b90:
    if (*param_6 == '\x01') {
      iVar1 = *(int *)(param_5 + (uint)*(ushort *)(param_6 + 4) * 8 + 0x18);
      if (iVar1 == 0) {
        iVar1 = 0;
      }
      else if ((uint)*(ushort *)(param_6 + 2) < *(uint *)(iVar1 + 0x38)) {
        iVar1 = FUN_02389b04();
      }
      else {
        iVar1 = 0;
      }
    }
    else {
      iVar1 = *(int *)(param_6 + 2);
    }
    if (iVar1 == 0) {
      iVar1 = 0;
    }
    else {
      iVar1 = FUN_0238779c(param_1,iVar1,iVar1 + 0xc,uVar3);
    }
  }
  if (iVar1 != 0) {
    *(undefined1 *)(param_1 + 8) = param_2;
    *(char *)(param_1 + 5) = param_6[6];
    *(char *)(param_1 + 9) = (char)param_3;
    FUN_02387910(param_1,param_6[7]);
    FUN_02387930(param_1,param_6[8]);
    FUN_0238794c(param_1,param_6[9]);
    FUN_02387954(param_1,cVar2);
    *(char *)(param_1 + 10) = param_6[0xb] + -0x40;
  }
  return iVar1 != 0;
}



// ---- FUN_02389f14 @ 02389f14 ----

void FUN_02389f14(void)

{
  undefined4 in_r3;
  
  FUN_0238479c(DAT_02389f48,DAT_02389f4c,8,in_r3,in_r3);
  FUN_023863d8(7,DAT_02389f50);
  *DAT_02389f54 = 0;
  return;
}



// ---- thunk_EXT_FUN_03802f8c @ 0238a654 ----

void thunk_EXT_FUN_03802f8c(void)

{
                    /* WARNING: Could not recover jumptable at 0x0238a658. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_0238a65c)();
  return;
}



// ---- FUN_0238a660 @ 0238a660 ----

void FUN_0238a660(void)

{
  undefined4 *puVar1;
  
  puVar1 = DAT_0238a704;
  DAT_0238a704[3] = 0xfffffffd;
  puVar1[0x3c] = 4;
  puVar1[4] = 0;
  puVar1[7] = 0;
  *puVar1 = 0;
  puVar1[2] = 0;
  puVar1[6] = 0;
  puVar1[5] = 0;
  puVar1[0x3e] = 0;
  puVar1[0x3d] = 0;
  FUN_0238415c(puVar1 + 0x12,DAT_0238a708,0,DAT_0238a70c,0x400,puVar1[0x3c]);
  FUN_02384474(puVar1 + 0x12);
  FUN_023863d8(0xb,DAT_0238a710);
  if (*DAT_0238a714 != 2) {
    *DAT_0238a718 = 1;
  }
  return;
}



// ---- FUN_0238a71c @ 0238a71c ----

undefined4 FUN_0238a71c(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  
  iVar1 = DAT_0238a758;
  uVar2 = FUN_02385e04();
  uVar3 = *(undefined4 *)(iVar1 + 0xf0);
  *(undefined4 *)(iVar1 + 0xf0) = param_1;
  FUN_023844c8(iVar1 + 0x48,param_1);
  FUN_02385e18(uVar2);
  return uVar3;
}



// ---- FUN_0238a75c @ 0238a75c ----

undefined4 FUN_0238a75c(void)

{
  return DAT_0238a764;
}



// ---- FUN_0238af70 @ 0238af70 ----

void FUN_0238af70(undefined4 param_1,undefined4 param_2)

{
  undefined1 *puVar1;
  
  puVar1 = DAT_0238afcc;
  do {
  } while ((*DAT_0238afc8 & 0x80000000) != 0);
  *DAT_0238afcc = 0xc0;
  puVar1[7] = (char)((uint)param_1 >> 0x18);
  puVar1[8] = (char)((uint)param_1 >> 0x10);
  puVar1[9] = (char)((uint)param_1 >> 8);
  puVar1[10] = (char)param_1;
  puVar1[0xb] = (char)((uint)param_2 >> 0x18);
  puVar1[0xc] = (char)((uint)param_2 >> 0x10);
  puVar1[0xd] = (char)((uint)param_2 >> 8);
  puVar1[0xe] = (char)param_2;
  return;
}



// ---- FUN_0238afd0 @ 0238afd0 ----

void FUN_0238afd0(void)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  code *pcVar4;
  
  puVar1 = DAT_0238b040;
  *(undefined4 *)*DAT_0238b040 = 0;
  pcVar4 = (code *)puVar1[0xf];
  uVar3 = puVar1[0x10];
  uVar2 = FUN_02385e04();
  puVar1[0x3f] = puVar1[0x3f] & 0xffffffb3;
  FUN_023843ec(puVar1 + 0x3d);
  if ((puVar1[0x3f] & 0x10) != 0) {
    FUN_02384474(puVar1 + 0x12);
  }
  FUN_02385e18(uVar2);
  if (pcVar4 != (code *)0x0) {
    (*pcVar4)(uVar3);
  }
  return;
}



// ---- FUN_0238b044 @ 0238b044 ----

uint FUN_0238b044(uint param_1)

{
  return *(uint *)(*DAT_0238b060 + 0x60) & 0xf8ffffff | param_1 | 0xa0000000;
}



// ---- FUN_0238b068 @ 0238b068 ----

undefined4 FUN_0238b068(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  uint *puVar1;
  uint uVar2;
  
  FUN_0238af70(0xb8000000,0,param_3,param_4,param_4);
  uVar2 = FUN_0238b044(0x7000000);
  puVar1 = DAT_0238b0b0;
  *DAT_0238b0b0 = uVar2 & 0xffffe000;
  do {
  } while ((*puVar1 & 0x800000) == 0);
  return *DAT_0238b0b4;
}



// ---- FUN_0238b0b8 @ 0238b0b8 ----

undefined4 FUN_0238b0b8(void)

{
  undefined4 uVar1;
  
  FUN_0238b0e8(DAT_0238b0e4,0,0);
  uVar1 = FUN_0238b068();
  FUN_0238afd0();
  return uVar1;
}



// ---- FUN_0238b0e8 @ 0238b0e8 ----

void FUN_0238b0e8(int param_1,undefined4 param_2,undefined4 param_3)

{
  undefined4 uVar1;
  
  uVar1 = FUN_02385e04();
  while ((*(uint *)(param_1 + 0xfc) & 4) != 0) {
    FUN_02384398(param_1 + 0xf4);
  }
  *(uint *)(param_1 + 0xfc) = *(uint *)(param_1 + 0xfc) | 4;
  *(undefined4 *)(param_1 + 0x3c) = param_2;
  *(undefined4 *)(param_1 + 0x40) = param_3;
  FUN_02385e18(uVar1);
  return;
}



// ---- FUN_0238b13c @ 0238b13c ----

void FUN_0238b13c(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  puVar2 = DAT_0238b1a0;
  iVar1 = DAT_0238b19c;
  if (*(int *)(DAT_0238b19c + 0xfc) == 0) {
    *(undefined4 *)(DAT_0238b19c + 0xfc) = 1;
    *(undefined4 *)(iVar1 + 0x28) = 0;
    *(undefined4 *)(iVar1 + 0x24) = 0;
    *(undefined4 *)(iVar1 + 0x20) = 0;
    *(undefined4 *)(iVar1 + 0x2c) = 0xffffffff;
    *(undefined4 *)(iVar1 + 0x3c) = 0;
    *(undefined4 *)(iVar1 + 0x40) = 0;
    *puVar2 = 0;
    FUN_0238a660();
    DAT_0238b1a0[8] = DAT_0238b1a4;
    FUN_0238b490();
  }
  return;
}



// ---- FUN_0238b490 @ 0238b490 ----

void FUN_0238b490(void)

{
  int iVar1;
  
  if (*(int *)(DAT_0238b4e0 + 8) == 0) {
    *(undefined4 *)(DAT_0238b4e0 + 8) = 1;
    thunk_EXT_FUN_037fe14c();
    do {
      iVar1 = FUN_02386428(0xe,0);
    } while (iVar1 == 0);
    FUN_023863d8(0xe,DAT_0238b4e4);
  }
  return;
}



// ---- FUN_0238b53c @ 0238b53c ----

undefined4 FUN_0238b53c(void)

{
  if (*(int *)(DAT_0238b57c + 0xc) == 0) {
    if ((*DAT_0238b580 & 0x80) == 0) {
      FUN_0238b5dc();
    }
    else {
      FUN_0238b584();
    }
  }
  return *(undefined4 *)(DAT_0238b57c + 0xc);
}



// ---- FUN_0238b584 @ 0238b584 ----

void FUN_0238b584(void)

{
  int iVar1;
  int iVar3;
  int *piVar2;
  
  if (*DAT_0238b5d4 == 0) {
    piVar2 = (int *)(DAT_0238b5d4 + -0x208);
  }
  else {
    piVar2 = (int *)(DAT_0238b5d4 + -8);
  }
  iVar1 = *piVar2;
  iVar3 = FUN_0238b0b8();
  *(uint *)(DAT_0238b5d8 + 0xc) = (uint)(iVar3 != iVar1);
  return;
}



// ---- FUN_0238b5dc @ 0238b5dc ----

bool FUN_0238b5dc(void)

{
  bool bVar1;
  
  bVar1 = (*DAT_0238b600 & 0x100000) == 0;
  if (!bVar1) {
    *(undefined4 *)(DAT_0238b604 + 0xc) = 1;
  }
  return bVar1;
}



// ---- FUN_0238b608 @ 0238b608 ----

void FUN_0238b608(void)

{
  int iVar1;
  
  if ((*(int *)(DAT_0238b6f4 + 4) == 0) && (*DAT_0238b6f8 != 2)) {
    if (*DAT_0238b6fc == 0xffffffff) {
      *DAT_0238b6fc = *(int *)(DAT_0238b6f8 + -2) + 10;
    }
    else if (*DAT_0238b6fc <= *(uint *)(DAT_0238b6f8 + -2)) {
      *DAT_0238b6fc = *(uint *)(DAT_0238b6f8 + -2) + 10;
      iVar1 = FUN_0238b53c();
      if (iVar1 != 0) {
        *(undefined4 *)(DAT_0238b6f4 + 4) = 1;
        iVar1 = FUN_0238a75c();
        if ((*(int *)(iVar1 + 0xc) == 0) && (DAT_0238b6fc[1] != 0)) {
          return;
        }
      }
      iVar1 = *(int *)(DAT_0238b6f4 + 4);
      DAT_0238b6fc[1] = 0;
      if (iVar1 != 0) {
        while (iVar1 = FUN_0238644c(0xe,0x11,0), iVar1 != 0) {
          thunk_EXT_FUN_03803554(100);
        }
      }
    }
  }
  return;
}



// ---- FUN_0238b7c0 @ 0238b7c0 ----

void FUN_0238b7c0(undefined4 param_1)

{
  short *psVar1;
  int iVar2;
  int iVar3;
  
  psVar1 = DAT_0238b8bc;
  if (*DAT_0238b8bc == 0) {
    *DAT_0238b8bc = 1;
    psVar1[2] = 0;
    psVar1[3] = 0;
    psVar1[4] = 5;
    psVar1[5] = 0;
    FUN_0238bc9c();
    func_0x0137cfb0();
    FUN_0238d2a0();
    FUN_0238c7d8();
    thunk_EXT_FUN_037fe14c();
    FUN_023863d8(6,DAT_0238b8c0);
    FUN_023863d8(9,DAT_0238b8c0);
    FUN_023863d8(8,DAT_0238b8c0);
    FUN_023863d8(4,DAT_0238b8c0);
    FUN_0238479c(DAT_0238b8c4,DAT_0238b8c8,0x10);
    iVar2 = DAT_0238b8cc;
    iVar3 = 0;
    do {
      FUN_02386124(iVar3 * 0x18 + iVar2,0,0x18);
      iVar3 = iVar3 + 1;
    } while (iVar3 < 0x10);
    psVar1 = DAT_0238b8bc;
    psVar1[0x248] = 0;
    psVar1[0x249] = 0;
    psVar1[0x24c] = 0;
    psVar1[0x24d] = 0;
    psVar1[0x24a] = 0;
    psVar1[0x24b] = 0;
    FUN_0238415c(DAT_0238b8d0,DAT_0238b8d4,0,DAT_0238b8c4,0x200,param_1);
    FUN_02384474(DAT_0238b8d0);
  }
  return;
}



// ---- FUN_0238bc9c @ 0238bc9c ----

void FUN_0238bc9c(void)

{
  int iVar1;
  undefined4 uVar2;
  undefined2 *puVar3;
  int iVar4;
  int iVar5;
  
  iVar4 = DAT_0238bd68;
  iVar5 = 0;
  *(undefined4 *)(DAT_0238bd68 + 0x24) = 0;
  *(undefined4 *)(iVar4 + 0x28) = 0x14;
  *(undefined4 *)(iVar4 + 0x2c) = 0x14;
  iVar4 = DAT_0238bd6c;
  do {
    iVar1 = iVar5 * 2;
    iVar5 = iVar5 + 1;
    *(undefined2 *)(iVar4 + iVar1) = 0;
  } while (iVar5 < 0x10);
  iVar4 = FUN_02385888();
  if (iVar4 == 0) {
    FUN_0238583c();
  }
  uVar2 = DAT_0238bd74;
  iVar4 = DAT_0238bd70;
  iVar5 = 0;
  do {
    FUN_02385988(iVar4 + iVar5 * 0x28);
    FUN_02385b18(iVar4 + iVar5 * 0x28,uVar2);
    puVar3 = DAT_0238bd80;
    iVar5 = iVar5 + 1;
  } while (iVar5 < 4);
  do {
  } while ((*DAT_0238bd78 & 0x80) != 0);
  *DAT_0238bd78 = (ushort)DAT_0238bd7c;
  *puVar3 = 0x84;
  do {
  } while ((puVar3[-1] & 0x80) != 0);
  FUN_0238bd88();
  *DAT_0238bd78 = (ushort)DAT_0238bd84;
  FUN_0238bd88();
  return;
}



// ---- FUN_0238bd88 @ 0238bd88 ----

void FUN_0238bd88(void)

{
  undefined2 *puVar1;
  
  puVar1 = DAT_0238bda8;
  *DAT_0238bda8 = 0;
  do {
  } while ((puVar1[-1] & 0x80) != 0);
  return;
}



// ---- FUN_0238c7d8 @ 0238c7d8 ----

void FUN_0238c7d8(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar2 = DAT_0238c80c;
  *(undefined4 *)(DAT_0238c80c + 4) = 1;
  iVar3 = 0;
  *(undefined4 *)(iVar2 + 0x28) = 0;
  iVar2 = DAT_0238c810;
  do {
    iVar1 = iVar3 * 2;
    iVar3 = iVar3 + 1;
    *(undefined2 *)(iVar2 + iVar1) = 0;
  } while (iVar3 < 0x10);
  return;
}



// ---- FUN_0238cb84 @ 0238cb84 ----

void FUN_0238cb84(undefined1 param_1,ushort param_2)

{
  ushort uVar1;
  ushort *puVar2;
  
  puVar2 = DAT_0238cbd0;
  do {
  } while ((*DAT_0238cbd0 & 0x80) != 0);
  uVar1 = (ushort)DAT_0238cbd4;
  *DAT_0238cbd0 = uVar1;
  *puVar2 = uVar1 + 0x600;
  FUN_0238cbdc(param_1);
  puVar2 = DAT_0238cbd0;
  *DAT_0238cbd0 = (ushort)DAT_0238cbd8;
  puVar2[1] = param_2 & 0xff;
  return;
}



// ---- FUN_0238cbdc @ 0238cbdc ----

void FUN_0238cbdc(ushort param_1)

{
  ushort *puVar1;
  
  puVar1 = DAT_0238cbfc;
  *DAT_0238cbfc = param_1 & 0xff;
  do {
  } while ((puVar1[-1] & 0x80) != 0);
  return;
}



// ---- FUN_0238cc00 @ 0238cc00 ----

ushort FUN_0238cc00(byte param_1)

{
  ushort uVar1;
  ushort *puVar2;
  
  puVar2 = DAT_0238cc64;
  do {
  } while ((*DAT_0238cc64 & 0x80) != 0);
  uVar1 = (ushort)DAT_0238cc68;
  *DAT_0238cc64 = uVar1;
  *puVar2 = uVar1 + 0x600;
  FUN_0238cbdc(param_1 | 0x80);
  puVar2 = DAT_0238cc64;
  *DAT_0238cc64 = (ushort)DAT_0238cc6c;
  puVar2[1] = 0;
  do {
  } while ((*puVar2 & 0x80) != 0);
  return *DAT_0238cc70 & 0xff;
}



// ---- FUN_0238cc74 @ 0238cc74 ----

void FUN_0238cc74(uint param_1)

{
  uint uVar1;
  
  uVar1 = FUN_0238cc00(0);
  FUN_0238cb84(0,uVar1 | param_1);
  return;
}



// ---- FUN_0238cc98 @ 0238cc98 ----

void FUN_0238cc98(byte param_1)

{
  byte bVar1;
  
  bVar1 = FUN_0238cc00(0);
  FUN_0238cb84(0,bVar1 & ~param_1);
  return;
}



// ---- FUN_0238ccc4 @ 0238ccc4 ----

void FUN_0238ccc4(undefined4 param_1)

{
  switch(param_1) {
  case 0:
    break;
  case 1:
    FUN_0238d15c(1);
    FUN_0238cde8(1);
    break;
  case 2:
    FUN_0238d15c(3);
    FUN_0238cde8(3);
    break;
  case 3:
    FUN_0238d15c(2);
    FUN_0238cde8(2);
    break;
  case 4:
    FUN_0238cc74(4);
    break;
  case 5:
    FUN_0238cc98(4);
    break;
  case 6:
    FUN_0238cc74(8);
    break;
  case 7:
    FUN_0238cc98(8);
    break;
  case 8:
    FUN_0238cc74(0xc);
    break;
  case 9:
    FUN_0238cc98(0xc);
    break;
  case 10:
    FUN_0238cc74(1);
    break;
  case 0xb:
    FUN_0238cc98(1);
    break;
  case 0xc:
    FUN_0238cc98(2);
    break;
  case 0xd:
    FUN_0238cc74(2);
    break;
  case 0xe:
    FUN_02386744();
    FUN_0238cc74(0x40);
    break;
  case 0xf:
    FUN_0238cc98(0x40);
  }
  return;
}



// ---- FUN_0238cde8 @ 0238cde8 ----

void FUN_0238cde8(int param_1)

{
  if (param_1 == 1) {
    FUN_0238cc98(0x10);
  }
  else if (param_1 == 2) {
    FUN_0238cc98(0x20);
    FUN_0238cc74(0x10);
  }
  else if (param_1 == 3) {
    FUN_0238cc74(0x30);
  }
  else {
    FUN_02385f74();
  }
  *DAT_0238ce4c = param_1;
  return;
}



// ---- FUN_0238d15c @ 0238d15c ----

void FUN_0238d15c(int param_1)

{
  undefined4 *puVar1;
  
  puVar1 = DAT_0238d174;
  if (param_1 < 0x10) {
    DAT_0238d174[1] = param_1;
    *puVar1 = 0;
  }
  return;
}



// ---- FUN_0238d188 @ 0238d188 ----

void FUN_0238d188(undefined4 param_1)

{
  undefined1 *puVar1;
  undefined4 uVar2;
  
  uVar2 = DAT_0238d1c8;
  puVar1 = DAT_0238d1c4;
  *(undefined4 *)(DAT_0238d1c4 + 4) = 0;
  *(undefined4 *)(puVar1 + 8) = param_1;
  FUN_02386124(uVar2,0,0xa4);
  FUN_0238d1fc(param_1);
  *DAT_0238d1c4 = 3;
  return;
}



// ---- FUN_0238d1fc @ 0238d1fc ----

void FUN_0238d1fc(undefined4 param_1)

{
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  
  local_54 = DAT_0238d294;
  local_50 = DAT_0238d298;
  local_4c = 0x600;
  local_48 = 4;
  local_34 = 0;
  local_30 = 8;
  local_28 = DAT_0238d29c;
  local_24 = 0x1c0;
  local_70 = 3;
  local_38 = 0x40;
  local_68 = 3;
  local_58 = 4;
  local_60 = 5;
  local_6c = 7;
  local_5c = 8;
  local_64 = 9;
  local_2c = param_1;
  func_0x013681b0(&local_54,&local_70);
  return;
}



// ---- FUN_0238d2a0 @ 0238d2a0 ----

void FUN_0238d2a0(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = 0;
  *(undefined4 *)(DAT_0238d2dc + 0x20) = 0;
  iVar2 = DAT_0238d2e0;
  do {
    iVar1 = iVar3 * 2;
    iVar3 = iVar3 + 1;
    *(undefined2 *)(iVar2 + iVar1) = 0;
  } while (iVar3 < 0x10);
  *DAT_0238d2e4 = *DAT_0238d2e4 & 0xff7f;
  return;
}



// ---- FUN_0238dd98 @ 0238dd98 ----

void FUN_0238dd98(void)

{
  undefined2 uVar1;
  undefined4 local_8 [2];
  
  local_8[0] = 0;
  thunk_EXT_FUN_03803594(local_8,DAT_0238ddc8,DAT_0238ddcc);
  uVar1 = FUN_02383d2c();
  *(undefined2 *)(DAT_0238ddd0 + 6) = uVar1;
  return;
}



// ---- thunk_EXT_FUN_03803594 @ 0238ddd4 ----

void thunk_EXT_FUN_03803594(void)

{
                    /* WARNING: Could not recover jumptable at 0x0238ddd8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_0238dddc)();
  return;
}



// ---- FUN_0238dde0 @ 0238dde0 ----

uint FUN_0238dde0(void)

{
  uint uVar1;
  
  if (*DAT_0238de28 == DAT_0238de2c) {
    uVar1 = 0;
  }
  else {
    if (-1 < (int)((uint)*(byte *)((int)DAT_0238de28 + 5) << 0x1e)) {
      FUN_0238de30();
    }
    uVar1 = (*(byte *)((int)DAT_0238de28 + 5) & 3) >> 1;
  }
  return uVar1;
}



// ---- FUN_0238de30 @ 0238de30 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_0238de30(void)

{
  int iVar1;
  uint uVar2;
  uint extraout_r1;
  uint uVar3;
  undefined4 uVar4;
  undefined4 local_18;
  undefined4 local_14;
  undefined1 auStack_10 [4];
  undefined4 local_c;
  
  uVar4 = 1;
  if (*DAT_0238df48 == 0xffff) {
    return 0;
  }
  if ((int)((uint)*(byte *)((int)DAT_0238df48 + 5) << 0x1e) < 0) {
    return 0;
  }
  iVar1 = FUN_0238dfd0(*(undefined2 *)(DAT_0238df4c + 6),auStack_10);
  if (iVar1 == 0) {
    FUN_02385e18(local_c);
    return 1;
  }
  FUN_0238df54(&local_18);
  uVar2 = 0x8000000;
  uVar3 = extraout_r1;
  if (DAT_080000b2 == -0x6a) {
    uVar2 = (uint)_DAT_080000be;
    uVar3 = (uint)*DAT_0238df48;
    if (uVar3 == uVar2) goto LAB_0238dec0;
  }
  else {
LAB_0238dec0:
    if (DAT_080000b2 != -0x6a) {
      uVar3 = (uint)*DAT_0238df48;
      uVar2 = (uint)*DAT_0238df50;
    }
    if ((DAT_080000b2 == -0x6a || uVar3 == uVar2) &&
       ((*(int *)(DAT_0238df48 + 4) == _DAT_080000ac ||
        (-1 < (int)((uint)*(byte *)((int)DAT_0238df48 + 5) << 0x1f))))) goto LAB_0238df18;
  }
  uVar4 = 0;
  *(byte *)((int)DAT_0238df48 + 5) = *(byte *)((int)DAT_0238df48 + 5) | 2;
LAB_0238df18:
  FUN_0238df98(local_18);
  FUN_0238dfb4(local_14);
  FUN_0238e020(*(undefined2 *)(DAT_0238df4c + 6),auStack_10);
  return uVar4;
}



// ---- FUN_0238df54 @ 0238df54 ----

void FUN_0238df54(int *param_1)

{
  ushort *puVar1;
  
  puVar1 = DAT_0238df94;
  *param_1 = (int)(*DAT_0238df94 & 0xc) >> 2;
  param_1[1] = (int)(*puVar1 & 0x10) >> 4;
  FUN_0238df98(3);
  FUN_0238dfb4(0);
  return;
}



// ---- FUN_0238df98 @ 0238df98 ----

void FUN_0238df98(short param_1)

{
  *DAT_0238dfb0 = *DAT_0238dfb0 & 0xfff3 | param_1 << 2;
  return;
}



// ---- FUN_0238dfb4 @ 0238dfb4 ----

void FUN_0238dfb4(short param_1)

{
  *DAT_0238dfcc = *DAT_0238dfcc & 0xffef | param_1 << 4;
  return;
}



// ---- FUN_0238dfd0 @ 0238dfd0 ----

undefined4 FUN_0238dfd0(undefined4 param_1,uint *param_2)

{
  uint uVar1;
  int iVar2;
  undefined4 uVar3;
  
  uVar1 = FUN_02385e04();
  param_2[1] = uVar1;
  uVar1 = FUN_02383d24(DAT_0238e01c);
  *param_2 = uVar1 & 0x80;
  if (((uVar1 & 0x80) == 0) && (iVar2 = FUN_02383cfc(param_1), iVar2 != 0)) {
    uVar3 = 0;
  }
  else {
    uVar3 = 1;
  }
  return uVar3;
}



// ---- FUN_0238e020 @ 0238e020 ----

void FUN_0238e020(undefined4 param_1,int *param_2)

{
  if (*param_2 == 0) {
    thunk_EXT_FUN_037fbb20();
  }
  FUN_02385e18(param_2[1]);
  return;
}



// ---- FUN_0238e048 @ 0238e048 ----

void FUN_0238e048(undefined4 param_1)

{
  int iVar1;
  
  while (iVar1 = FUN_0238644c(0xd,param_1,0), iVar1 != 0) {
    thunk_EXT_FUN_03803554(1);
  }
  return;
}



// ---- FUN_0238e088 @ 0238e088 ----

void FUN_0238e088(void)

{
  int iVar1;
  
  FUN_02385218();
  FUN_0238543c();
  FUN_02385490(DAT_0238e110);
  if (*(int *)(DAT_0238e114 + 10) == 0) {
    *(undefined4 *)(DAT_0238e114 + 10) = 1;
    FUN_0238dd98();
    iVar1 = FUN_02383d2c();
    if (iVar1 != -3) {
      *DAT_0238e114 = (short)iVar1;
      thunk_EXT_FUN_037fe14c();
      FUN_023863d8(0xd,DAT_0238e118);
      FUN_0238e128();
      FUN_023863d8(0xd,DAT_0238e11c);
      FUN_023863d8(0x10,DAT_0238e120);
      FUN_023863d8(0x11,DAT_0238e124);
    }
  }
  return;
}



// ---- FUN_0238e128 @ 0238e128 ----

void FUN_0238e128(void)

{
  ushort uVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  undefined4 uVar4;
  uint uVar5;
  byte bVar6;
  int iVar7;
  uint uVar8;
  
  if ((*(int *)(DAT_0238e284 + 8) == 0) &&
     (uVar1 = *DAT_0238e288, *(undefined4 *)(DAT_0238e284 + 8) = 1, (uVar1 & 1) != 0)) {
    uVar4 = FUN_02383a1c(0x40000);
    iVar7 = DAT_0238e284;
    uVar2 = *DAT_0238e28c;
    *DAT_0238e28c = 1;
    while (*(int *)(iVar7 + 0x28) != 1) {
      thunk_EXT_FUN_03803554(0x100);
    }
    uVar5 = *(uint *)(DAT_0238e284 + 0x18) & DAT_0238e290;
    bVar6 = 1;
    uVar3 = FUN_02383d2c();
    FUN_02383c80(uVar3);
    for (iVar7 = 0; iVar7 < 0x4e; iVar7 = iVar7 + 1) {
      uVar8 = (DAT_0238e294 ^ 0x84) & 0xffff;
      if ((iVar7 != 0x4c) && (uVar8 = DAT_0238e294, iVar7 == 0x4d)) {
        uVar8 = (DAT_0238e294 ^ 3) & 0xffff;
      }
      if ((uVar8 & *(ushort *)((uVar5 >> 6) * 0x20 + iVar7 * 2 + 0x2000004)) !=
          (uint)*(ushort *)(iVar7 * 2 + 0x8000004)) {
        bVar6 = 0;
        break;
      }
    }
    thunk_EXT_FUN_037fbb20(uVar3);
    FUN_02383dc4(uVar3);
    *(byte *)(DAT_0238e298 + 5) = *(byte *)(DAT_0238e298 + 5) & 0xfe | bVar6;
    FUN_0238e048(1);
    uVar3 = *DAT_0238e28c;
    *DAT_0238e28c = uVar2;
    FUN_02383a1c(uVar4,uVar3);
  }
  return;
}



// ---- FUN_0238e310 @ 0238e310 ----

void FUN_0238e310(uint *param_1)

{
  bool bVar1;
  undefined2 *puVar2;
  undefined4 uVar3;
  undefined2 *puVar4;
  uint uVar5;
  undefined4 uVar6;
  int iVar7;
  
  uVar5 = 0;
  if ((param_1 != (uint *)0x0) && (uVar5 = *param_1, uVar5 == 0)) {
    uVar5 = param_1[0x11] + 1;
    param_1[0x11] = uVar5;
    if ((param_1[0x10] != 0) && (uVar5 = param_1[0x11], param_1[0x10] < uVar5)) {
      param_1 = (uint *)0x0;
    }
  }
  if (param_1 != (uint *)0x0) {
    uVar5 = param_1[0xf];
  }
  if (param_1 != (uint *)0x0 && uVar5 != 0) {
    if (param_1 != (uint *)0x0) {
      uVar5 = FUN_02383d24(DAT_0238e530);
      if (((uVar5 & 0x80) == 0) && (iVar7 = FUN_02383cfc(*DAT_0238e52c), iVar7 != 0)) {
        FUN_023855cc(DAT_0238e53c,DAT_0238e544,0,DAT_0238e540,param_1);
      }
      else {
        puVar2 = DAT_0238e534;
        if (*param_1 == param_1[1]) {
          *(undefined4 *)(DAT_0238e52c + 2) = 0;
          *puVar2 = 0;
          FUN_023855cc(DAT_0238e53c,param_1[2],0,DAT_0238e540,param_1);
          *param_1 = 0;
        }
        else if ((*param_1 & 1) == 0) {
          *(undefined4 *)(DAT_0238e52c + 2) = 2;
          *puVar2 = 2;
          FUN_023855cc(DAT_0238e53c,param_1[(*param_1 >> 1) + 3],0,DAT_0238e540,param_1);
          *param_1 = *param_1 + 1;
        }
        else {
          *(undefined4 *)(DAT_0238e52c + 2) = 0;
          *puVar2 = 0;
          FUN_023855cc(DAT_0238e53c,param_1[(*param_1 >> 1) + 9],0,DAT_0238e540,param_1);
          *param_1 = *param_1 + 1;
        }
        if ((uVar5 & 0x80) == 0) {
          FUN_02383cd0(*DAT_0238e52c);
        }
      }
    }
  }
  else {
    uVar6 = FUN_02385e04();
    puVar4 = DAT_0238e534;
    uVar3 = DAT_0238e530;
    puVar2 = DAT_0238e52c;
    if (*(int *)(DAT_0238e52c + 2) == 2) {
      bVar1 = false;
      while (!bVar1) {
        uVar5 = FUN_02383d24(uVar3);
        if (((uVar5 & 0x80) == 0) && (iVar7 = FUN_02383cfc(*puVar2), iVar7 != 0)) {
          FUN_02385e68(DAT_0238e538);
        }
        else {
          *(undefined4 *)(puVar2 + 2) = 0;
          bVar1 = true;
          *puVar4 = 0;
          if ((uVar5 & 0x80) == 0) {
            FUN_02383cd0(*puVar2);
          }
        }
      }
    }
    FUN_023856b0(DAT_0238e53c);
    FUN_02385e18(uVar6);
  }
  return;
}



// ---- FUN_0238e548 @ 0238e548 ----

void FUN_0238e548(void)

{
  int iVar1;
  undefined4 uVar2;
  bool bVar3;
  
  if (DAT_0238e638[1] == 0xffffffff) {
    DAT_0238e638[1] = *DAT_0238e63c + 10;
  }
  else {
    bVar3 = *(int *)(DAT_0238e640 + 0x10) == 0;
    iVar1 = DAT_0238e640;
    if (bVar3) {
      iVar1 = *(int *)(DAT_0238e640 + 0xc);
    }
    if ((bVar3 && iVar1 == 0) && ((uint)DAT_0238e638[1] <= *DAT_0238e63c)) {
      DAT_0238e638[1] = *DAT_0238e63c + 10;
      uVar2 = FUN_0238dde0();
      *(undefined4 *)(DAT_0238e640 + 0xc) = uVar2;
      iVar1 = FUN_0238de30();
      if (iVar1 == 0) {
        if (*DAT_0238e638 != 0) {
          *(undefined4 *)(DAT_0238e640 + 0x10) = 1;
          return;
        }
        *(undefined4 *)(DAT_0238e640 + 0xc) = 1;
      }
      iVar1 = *(int *)(DAT_0238e640 + 0xc);
      *DAT_0238e638 = 0;
      if (iVar1 != 0) {
        while (iVar1 = FUN_0238644c(0xd,0x11,0), iVar1 != 0) {
          FUN_02384570(100);
        }
      }
    }
  }
  return;
}



// ---- FUN_0238e880 @ 0238e880 ----

/* WARNING: Removing unreachable block (ram,0x0238e820) */
/* WARNING: Removing unreachable block (ram,0x0238e824) */
/* WARNING: Removing unreachable block (ram,0x0238e828) */
/* WARNING: Removing unreachable block (ram,0x0238e82c) */
/* WARNING: Removing unreachable block (ram,0x0238e858) */
/* WARNING: Removing unreachable block (ram,0x0238e8b8) */

ulonglong FUN_0238e880(uint param_1,uint param_2,uint param_3,uint param_4)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  int iVar9;
  bool bVar10;
  bool bVar11;
  
  if (param_4 == 0 && param_3 == 0) {
    return CONCAT44(param_2,param_1);
  }
  if (param_2 == 0 && param_4 == 0) {
    uVar4 = FUN_0238eadc(param_1,param_3);
    return (ulonglong)uVar4;
  }
  if (param_2 == 0 && param_1 == 0) {
    return 0;
  }
  iVar7 = 1;
  iVar8 = 0;
  if (-1 < (int)param_4) {
    do {
      iVar7 = iVar8;
      bVar10 = CARRY4(param_3,param_3);
      param_3 = param_3 * 2;
      param_4 = param_4 * 2 + (uint)bVar10;
      iVar8 = iVar7 + 1;
    } while (-1 < (int)param_4);
    iVar7 = iVar7 + 2;
  }
  for (; (-1 < (int)param_2 && (iVar7 != 1)); iVar7 = iVar7 + -1) {
    bVar10 = CARRY4(param_1,param_1);
    param_1 = param_1 * 2;
    param_2 = param_2 * 2 + (uint)bVar10;
  }
  iVar8 = 0;
  uVar4 = 0;
  iVar9 = 0;
  while( true ) {
    uVar3 = param_1 - param_3;
    uVar5 = param_2 - (param_4 + (param_3 > param_1));
    iVar9 = iVar9 * 2 + (uint)CARRY4(uVar4,uVar4);
    for (iVar8 = iVar8 - (uint)(param_2 <= param_4 &&
                               (uint)(param_3 <= param_1) <= param_2 - param_4); uVar4 = uVar4 * 2,
        iVar8 < 0;
        iVar8 = iVar8 * 2 + (uint)(bVar10 || CARRY4(uVar2,(uint)bVar11)) +
                (uint)(CARRY4(uVar6,param_4) || CARRY4(uVar6 + param_4,(uint)CARRY4(uVar1,param_3)))
        ) {
      iVar7 = iVar7 + -1;
      if (iVar7 == 0) goto LAB_0238e810;
      bVar11 = CARRY4(uVar3,uVar3);
      uVar1 = uVar3 * 2;
      uVar2 = uVar5 * 2;
      bVar10 = CARRY4(uVar5,uVar5);
      uVar6 = uVar5 * 2 + (uint)bVar11;
      uVar3 = uVar1 + param_3;
      uVar5 = uVar6 + param_4 + (uint)CARRY4(uVar1,param_3);
      iVar9 = iVar9 * 2 + (uint)CARRY4(uVar4,uVar4);
    }
    uVar4 = uVar4 | 1;
    iVar7 = iVar7 + -1;
    if (iVar7 == 0) break;
    param_1 = uVar3 * 2;
    param_2 = uVar5 * 2 + (uint)CARRY4(uVar3,uVar3);
    iVar8 = iVar8 * 2 + (uint)(CARRY4(uVar5,uVar5) || CARRY4(uVar5 * 2,(uint)CARRY4(uVar3,uVar3)));
  }
LAB_0238e810:
  return CONCAT44(iVar9,uVar4);
}



// ---- FUN_0238e8c8 @ 0238e8c8 ----

undefined8 FUN_0238e8c8(uint param_1,uint param_2)

{
  uint uVar1;
  uint uVar2;
  bool bVar3;
  bool bVar4;
  undefined8 uVar5;
  
  uVar2 = (param_1 ^ param_2) & 0x80000000;
  bVar3 = (int)param_1 < 0;
  if (bVar3) {
    param_1 = -param_1;
    uVar2 = uVar2 + 1;
  }
  bVar4 = param_2 != 0;
  if ((int)param_2 < 0) {
    param_2 = -param_2;
  }
  uVar1 = param_1;
  if (bVar4) {
    if (param_2 <= param_1) {
      uVar1 = 0x1c;
      uVar2 = param_1 >> 4;
      if ((int)param_2 <= (int)(param_1 >> 0x10)) {
        uVar1 = 0xc;
        uVar2 = param_1 >> 0x14;
      }
      if ((int)param_2 <= (int)(uVar2 >> 4)) {
        uVar1 = uVar1 - 8;
        uVar2 = uVar2 >> 8;
      }
      if ((int)param_2 <= (int)uVar2) {
        uVar1 = uVar1 - 4;
        uVar2 = uVar2 >> 4;
      }
                    /* WARNING: Could not recover jumptable at 0x0238e934. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      uVar5 = (*(code *)(&LAB_0238e93c + uVar1 * 0xc))
                        ((param_1 << (uVar1 & 0xff)) * 2,-param_2,uVar1 * 3,uVar2);
      return uVar5;
    }
    uVar1 = 0;
    param_2 = param_1;
  }
  if ((uVar2 & 0x80000000) != 0) {
    uVar1 = -uVar1;
  }
  if (bVar3) {
    param_2 = -param_2;
  }
  return CONCAT44(param_2,uVar1);
}



// ---- FUN_0238eadc @ 0238eadc ----

void FUN_0238eadc(uint param_1,uint param_2)

{
  uint uVar1;
  uint uVar2;
  
  if (param_2 <= param_1) {
    uVar1 = 0x1c;
    uVar2 = param_1 >> 4;
    if ((int)param_2 <= (int)(param_1 >> 0x10)) {
      uVar1 = 0xc;
      uVar2 = param_1 >> 0x14;
    }
    if ((int)param_2 <= (int)(uVar2 >> 4)) {
      uVar1 = uVar1 - 8;
      uVar2 = uVar2 >> 8;
    }
    if ((int)param_2 <= (int)uVar2) {
      uVar1 = uVar1 - 4;
      uVar2 = uVar2 >> 4;
    }
                    /* WARNING: Could not recover jumptable at 0x0238eb28. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (*(code *)(&LAB_0238eb30 + uVar1 * 0xc))
              ((param_1 << (uVar1 & 0xff)) * 2,-param_2,uVar1 * 3,uVar2);
    return;
  }
  return;
}



// ---- FUN_0238efc0 @ 0238efc0 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0238efc0(void)

{
  ushort *puVar1;
  ushort *puVar2;
  
  _DAT_04000208 = 0x4000000;
  *DAT_0238f028 = 0;
  puVar1 = DAT_0238f02c;
  *DAT_0238f02c = 0x100;
  puVar2 = DAT_0238f02c;
  do {
  } while ((*puVar1 & 0xf) != 1);
  *DAT_0238f02c = 0;
  do {
  } while (*puVar2 == 1);
                    /* WARNING: Could not recover jumptable at 0x0238f024. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(DAT_0238f030 + 0x34))(0,0,0,0);
  return;
}



// ---- FUN_0238f0d4 @ 0238f0d4 ----

uint FUN_0238f0d4(uint param_1)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  int iVar6;
  
  uVar2 = param_1 & DAT_0238f1dc & 0xffff;
  if (uVar2 == 0) {
    uVar2 = 0;
  }
  else {
    for (uVar4 = 0; ((int)uVar4 < 0x10 && ((uVar2 & 1 << (uVar4 & 0xff)) == 0)); uVar4 = uVar4 + 1)
    {
    }
    for (uVar3 = 0xf; (uVar3 != 0 && ((uVar2 & 1 << (uVar3 & 0xff)) == 0)); uVar3 = uVar3 - 1) {
    }
    if ((int)(uVar3 - uVar4) < 5) {
      uVar2 = 1 << (uVar4 & 0xff) & 0xffff;
    }
    else {
      uVar5 = (int)(uVar3 + uVar4) / 2;
      for (iVar6 = 0; iVar6 < (int)(uVar3 - uVar4); iVar6 = iVar6 + 1) {
        iVar1 = iVar6 >> 0x1f;
        uVar5 = iVar6 * ((((uint)(iVar6 * -0x80000000 + iVar1) >> 0x1f | iVar1 << 1) - iVar1) * 2 +
                        -1) + uVar5;
        if ((uVar2 & 1 << (uVar5 & 0xff)) != 0) break;
      }
      iVar6 = uVar3 - uVar5;
      if (4 < iVar6) {
        iVar6 = uVar5 - uVar4;
      }
      if (iVar6 < 5) {
        uVar2 = (1 << (uVar3 & 0xff) | 1 << (uVar4 & 0xff)) & 0xffff;
      }
      else {
        uVar2 = (1 << (uVar5 & 0xff) | 1 << (uVar3 & 0xff) | 1 << (uVar4 & 0xff)) & 0xffff;
      }
    }
  }
  return uVar2;
}



// ---- FUN_0238f4d4 @ 0238f4d4 ----

int FUN_0238f4d4(undefined4 param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  undefined2 *puVar1;
  int local_8 [2];
  
  local_8[0] = param_4;
  func_0x033ab91c(DAT_0238f544,param_1,1);
  func_0x033ab9a8(DAT_0238f548,local_8,1);
  if (*(short *)(local_8[0] + (uint)*(ushort *)(local_8[0] + 0xe) * 2 + 0x14) == 0xe) {
    puVar1 = (undefined2 *)func_0x033b61d8();
    *puVar1 = 0x80;
    puVar1[1] = 0x13;
    puVar1[2] = 0x18;
    func_0x033b618c();
    func_0x033ad89c();
    func_0x033ad0cc();
  }
  return local_8[0];
}



// ---- FUN_0238f6bc @ 0238f6bc ----

bool FUN_0238f6bc(int param_1,int param_2)

{
  short sVar1;
  undefined2 uVar2;
  undefined2 *puVar3;
  int iVar4;
  bool bVar5;
  
  iVar4 = *(int *)(DAT_0238f804 + 0x550);
  func_0x033ad310(iVar4 + 0xe0,param_2 + 0x10,6);
  *(undefined2 *)(param_2 + 0x16) = 7;
  *(undefined2 *)(param_2 + 0x18) = *(undefined2 *)(iVar4 + 500);
  *(undefined2 *)(param_2 + 0x1e) = *(undefined2 *)(iVar4 + 0x1ec);
  *(undefined2 *)(param_2 + 0x1c) = *(undefined2 *)(iVar4 + 0xe6);
  bVar5 = *(int *)(iVar4 + 0x198) != 0;
  if (bVar5) {
    *(undefined2 *)(param_2 + 0x20) = *(undefined2 *)(iVar4 + 0x196);
    *(undefined2 *)(param_2 + 0x22) = *(undefined2 *)(iVar4 + 0xc4);
    func_0x033ad310(iVar4 + 0x19c,param_2 + 0x24,0x50);
  }
  else {
    *(undefined2 *)(param_2 + 0x20) = 0;
    *(undefined2 *)(param_2 + 0x22) = 0;
    func_0x033ad1d0(0,param_2 + 0x24,0x50);
  }
  *(ushort *)(param_2 + 0x9e) = (ushort)bVar5;
  *(undefined2 *)(param_2 + 0x74) = 1;
  *(undefined2 *)(param_2 + 0x76) = 1;
  if (*(short *)(iVar4 + 0xe6) == 1) {
    uVar2 = 0;
  }
  else {
    uVar2 = 0x10;
  }
  *(undefined2 *)(param_2 + 0x78) = uVar2;
  *(undefined2 *)(param_2 + 0x7a) = 10;
  if (param_1 == 0x26) {
    func_0x033ad1d0(0,param_2 + 0x7c,0x20);
  }
  else {
    func_0x033ad1d0(0,param_2 + 0x7c,8);
    func_0x033ad1d0(DAT_0238f808,param_2 + 0x84,0x18);
  }
  *(undefined2 *)(param_2 + 0x9c) = *(undefined2 *)(iVar4 + 0x1ee);
  iVar4 = FUN_023916e0(param_2);
  sVar1 = *(short *)(iVar4 + 4);
  if (sVar1 != 0) {
    puVar3 = (undefined2 *)func_0x033b61d8(iVar4);
    *puVar3 = (short)param_1;
    puVar3[1] = 1;
    puVar3[2] = 0x200;
    puVar3[3] = sVar1;
    func_0x033b618c();
  }
  return sVar1 == 0;
}



// ---- FUN_0238f850 @ 0238f850 ----

void FUN_0238f850(undefined1 param_1)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar1 = DAT_0238f880;
  iVar3 = 0;
  do {
    iVar2 = iVar1 + iVar3;
    iVar3 = iVar3 + 1;
    *(undefined1 *)(iVar2 + 0x1554) = param_1;
  } while (iVar3 < 0x20);
  *(undefined4 *)(DAT_0238f884 + 0x574) = 0;
  return;
}



// ---- FUN_0238f8c4 @ 0238f8c4 ----

undefined4 FUN_0238f8c4(uint param_1)

{
  undefined4 uVar1;
  
  if (*(char *)(*(int *)(DAT_0238f928 + 0x54c) + 0x53) != '\b') {
    if (param_1 < 8) {
      return 0;
    }
    if (0xd < param_1) {
      if (param_1 < 0x14) {
        uVar1 = 2;
      }
      else {
        uVar1 = 3;
      }
      return uVar1;
    }
    return 1;
  }
  if (param_1 < 0x16) {
    return 0;
  }
  if (0x1b < param_1) {
    if (param_1 < 0x22) {
      uVar1 = 2;
    }
    else {
      uVar1 = 3;
    }
    return uVar1;
  }
  return 1;
}



// ---- FUN_0238f92c @ 0238f92c ----

void FUN_0238f92c(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = func_0x033acf5c();
  func_0x033ab7b8();
  func_0x033ab620(DAT_0238f984,*(undefined4 *)(DAT_0238f980 + 0x58c));
  uVar2 = FUN_02397d0c();
  func_0x033ab620(uVar2,*(undefined4 *)(DAT_0238f980 + 0x588));
  func_0x033ab620(DAT_0238f988,*(undefined4 *)(DAT_0238f980 + 0x584));
  func_0x033ab7f0();
  func_0x033acf70(uVar1);
  return;
}



// ---- FUN_0238f98c @ 0238f98c ----

void FUN_0238f98c(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = func_0x033acf5c();
  func_0x033ab7b8();
  func_0x033ab620(DAT_0238f9e4,*(undefined4 *)(DAT_0238f9e0 + 0x578));
  uVar2 = FUN_02397d0c();
  func_0x033ab620(uVar2,*(undefined4 *)(DAT_0238f9e0 + 0x57c));
  func_0x033ab620(DAT_0238f9e8,*(undefined4 *)(DAT_0238f9e0 + 0x580));
  func_0x033ab7f0();
  func_0x033acf70(uVar1);
  return;
}



// ---- FUN_0238f9ec @ 0238f9ec ----

int FUN_0238f9ec(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar3 = 0;
  func_0x033acf5c();
  iVar1 = *(int *)(DAT_0238fa54 + 0x54c);
  if (iVar1 != 0) {
    for (iVar2 = 0; iVar2 < 0x20; iVar2 = iVar2 + 1) {
      if ((*(uint *)(iVar1 + iVar2 * 0x10 + 0xd0) & 0x8000) != 0) {
        iVar1 = iVar1 + 0xd0;
        iVar3 = iVar1 + iVar2 * 0x10;
        *(uint *)(iVar1 + iVar2 * 0x10) = *(uint *)(iVar1 + iVar2 * 0x10) & 0xffff7fff;
        break;
      }
    }
  }
  func_0x033acf70();
  return iVar3;
}



// ---- FUN_0238fa58 @ 0238fa58 ----

void FUN_0238fa58(void)

{
  int iVar1;
  
  iVar1 = *(int *)(DAT_0238fa88 + 0x550);
  *(undefined2 *)(iVar1 + 0x38) = 0;
  *(undefined2 *)(iVar1 + 0x3a) = 0;
  *(undefined2 *)(iVar1 + 0x30) = 0;
  *(undefined2 *)(iVar1 + 0x32) = 0;
  *(undefined2 *)(iVar1 + 0x3c) = 0;
  *(undefined2 *)(iVar1 + 0x3e) = 0;
  *(undefined2 *)(iVar1 + 0x34) = 0;
  *(undefined2 *)(iVar1 + 0x36) = 0;
  return;
}



// ---- FUN_0238fa8c @ 0238fa8c ----

void FUN_0238fa8c(short param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(DAT_0238fad0 + 0x550);
  *(short *)(iVar1 + 0x30) = param_1;
  *(short *)(iVar1 + 0x34) = param_1;
  param_1 = param_1 + 4;
  if (*(short *)(iVar1 + 0x188) == 0) {
    *(short *)(iVar1 + 0x3c) = param_1;
    *(short *)(iVar1 + 0x38) = param_1;
  }
  else {
    *(short *)(iVar1 + 0x3e) = param_1;
    *(short *)(iVar1 + 0x3a) = param_1;
  }
  return;
}



// ---- FUN_0238fad4 @ 0238fad4 ----

void FUN_0238fad4(short param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(DAT_0238fb18 + 0x550);
  *(short *)(iVar1 + 0x36) = param_1;
  *(short *)(iVar1 + 0x32) = param_1;
  param_1 = param_1 + 2;
  if (*(short *)(iVar1 + 0x188) == 0) {
    *(short *)(iVar1 + 0x3e) = param_1;
    *(short *)(iVar1 + 0x3a) = param_1;
  }
  else {
    *(short *)(iVar1 + 0x3c) = param_1;
    *(short *)(iVar1 + 0x38) = param_1;
  }
  return;
}



// ---- FUN_0238fb1c @ 0238fb1c ----

void FUN_0238fb1c(short param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(DAT_0238fb44 + 0x550);
  *(short *)(iVar1 + 0x30) = param_1;
  if (*(short *)(iVar1 + 0x188) == 0) {
    *(short *)(iVar1 + 0x38) = param_1 + 4;
  }
  else {
    *(short *)(iVar1 + 0x3a) = param_1 + 4;
  }
  return;
}



// ---- FUN_0238fb48 @ 0238fb48 ----

void FUN_0238fb48(short param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(DAT_0238fb70 + 0x550);
  *(short *)(iVar1 + 0x32) = param_1;
  if (*(short *)(iVar1 + 0x188) == 0) {
    *(short *)(iVar1 + 0x3a) = param_1 + 2;
  }
  else {
    *(short *)(iVar1 + 0x38) = param_1 + 2;
  }
  return;
}



// ---- FUN_02390d30 @ 02390d30 ----

void FUN_02390d30(void)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  int iVar3;
  undefined2 *puVar4;
  int iVar5;
  
  iVar5 = *(int *)(DAT_02390da8 + 0x550);
  puVar2 = (undefined4 *)FUN_0238f9ec();
  if (puVar2 == (undefined4 *)0x0) {
    iVar3 = 0;
  }
  else {
    *puVar2 = 0x2d;
    uVar1 = DAT_02390dac;
    puVar2[1] = (uint)*(ushort *)(iVar5 + 0x68);
    iVar3 = func_0x033ab91c(uVar1,puVar2,0);
  }
  if (iVar3 == 0) {
    puVar4 = (undefined2 *)func_0x033b61d8();
    *puVar4 = 0x80;
    puVar4[1] = 8;
    puVar4[2] = 0x16;
    puVar4[3] = 0x2d;
    func_0x033b618c();
  }
  else {
    *(undefined2 *)(iVar5 + 0x66) = 1;
  }
  return;
}



// ---- FUN_02390f78 @ 02390f78 ----

void FUN_02390f78(void)

{
  func_0x033ac5e8(DAT_02390f94);
  func_0x033ac5e8(DAT_02390f98);
  return;
}



// ---- FUN_02391044 @ 02391044 ----

undefined2 * FUN_02391044(undefined2 *param_1,undefined2 param_2)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 1;
  param_1[8] = param_2;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391098 @ 02391098 ----

undefined2 *
FUN_02391098(undefined2 *param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 1;
  param_1[7] = 3;
  param_1[8] = param_2;
  param_1[9] = param_3;
  param_1[10] = param_4;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_023910f8 @ 023910f8 ----

undefined2 *
FUN_023910f8(undefined2 *param_1,uint param_2,undefined4 param_3,undefined4 param_4,
            undefined4 param_5,undefined2 param_6,undefined4 param_7,undefined2 param_8)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 2;
  param_1[7] = 0x1f;
  func_0x033ad1e8(param_3,param_1 + 8,6,param_4,param_4);
  param_1[0xb] = (short)param_4;
  func_0x033ad1e8(param_5,param_1 + 0xc,0x20);
  param_1[0x1c] = param_6;
  func_0x033ad1e8(param_7,param_1 + 0x1d,0x10);
  param_1[0x25] = param_8;
  param_1[0x26] = 0;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = (short)(param_2 >> 1) + -0x2c;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_023911b0 @ 023911b0 ----

undefined2 *
FUN_023911b0(undefined2 *param_1,undefined2 param_2,undefined4 param_3,undefined4 param_4)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 3;
  param_1[7] = 0x22;
  param_1[8] = param_2;
  param_1[9] = 0;
  func_0x033ad1e8(param_3,param_1 + 10,0x44,0,param_4);
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 5;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391228 @ 02391228 ----

undefined2 *
FUN_02391228(undefined2 *param_1,undefined4 param_2,undefined2 param_3,undefined2 param_4)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 4;
  param_1[7] = 5;
  func_0x033ad1e8(param_2,param_1 + 8,6);
  param_1[0xb] = param_3;
  param_1[0xc] = param_4;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 6;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_023912a8 @ 023912a8 ----

undefined2 *
FUN_023912a8(undefined2 *param_1,undefined4 param_2,undefined2 param_3,undefined4 param_4)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 5;
  param_1[7] = 4;
  func_0x033ad1e8(param_2,param_1 + 8,6,4,param_4);
  param_1[0xb] = param_3;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 4;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391320 @ 02391320 ----

undefined2 *
FUN_02391320(undefined2 *param_1,undefined4 param_2,undefined2 param_3,undefined2 param_4)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 6;
  param_1[7] = 5;
  func_0x033ad1e8(param_2,param_1 + 8);
  param_1[0xb] = param_3;
  param_1[0xc] = param_4;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 3;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_0239139c @ 0239139c ----

undefined2 *
FUN_0239139c(undefined2 *param_1,undefined2 param_2,undefined4 param_3,undefined4 param_4,
            undefined2 param_5,undefined2 param_6,undefined2 param_7,undefined2 param_8,
            ushort param_9,undefined4 param_10)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 9;
  param_1[7] = (short)((param_9 + 1) / 2) + 0x17;
  param_1[8] = param_2;
  func_0x033ad1e8(param_3,param_1 + 9,0x20,param_4,param_4);
  param_1[0x19] = (short)param_4;
  param_1[0x1a] = param_5;
  param_1[0x1b] = param_6;
  param_1[0x1c] = param_7;
  param_1[0x1d] = param_8;
  param_1[0x1e] = param_9;
  func_0x033ad1e8(param_10,param_1 + 0x1f);
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_0239145c @ 0239145c ----

undefined2 *
FUN_0239145c(undefined2 *param_1,undefined2 param_2,undefined2 param_3,undefined4 param_4,
            undefined4 param_5)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 10;
  param_1[7] = 0xc;
  param_1[8] = 0;
  param_1[9] = param_2;
  param_1[10] = param_3;
  param_1[0xb] = (short)param_4;
  func_0x033ad1e8(param_5,param_1 + 0xc,0x10,param_4,param_4);
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 0x12;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_023914dc @ 023914dc ----

undefined2 * FUN_023914dc(undefined2 *param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  ushort uVar1;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 0x100;
  param_1[7] = 0x18;
  func_0x033ad1e8(param_2,param_1 + 8,0x30,param_4,param_4);
  *(undefined2 *)(param_2 + 2) = 0;
  *(undefined2 *)(param_2 + 4) = 0;
  *(undefined2 *)(param_2 + 8) = 0;
  *(undefined2 *)(param_2 + 10) = 0;
  *(undefined2 *)(param_2 + 0xc) = 0;
  *(undefined2 *)(param_2 + 0x10) = 0;
  *(undefined2 *)(param_2 + 0x12) = 0;
  *(undefined2 *)(param_2 + 0x14) = 0;
  *(undefined2 *)(param_2 + 0x16) = 0;
  *(undefined2 *)(param_2 + 0x24) = 0;
  *(undefined2 *)(param_2 + 0x26) = 0;
  *(undefined2 *)(param_2 + 0x28) = 0;
  *(undefined2 *)(param_2 + 0x2a) = 0;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 2;
  FUN_0238f4d4(param_1);
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391588 @ 02391588 ----

undefined2 *
FUN_02391588(undefined2 *param_1,undefined2 param_2,undefined2 param_3,undefined4 param_4)

{
  ushort uVar1;
  undefined4 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  uVar2 = DAT_023915ec;
  param_1[5] = 0;
  param_1[6] = (short)uVar2;
  param_1[7] = 4;
  param_1[8] = param_2;
  param_1[9] = param_3;
  *(undefined4 *)(param_1 + 10) = param_4;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_023916e0 @ 023916e0 ----

undefined2 * FUN_023916e0(undefined2 *param_1)

{
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 0x200;
  param_1[7] = 0x48;
  param_1[0x50] = param_1[6];
  param_1[0x51] = 1;
  FUN_0238f4d4();
  return param_1 + 0x50;
}



// ---- FUN_02391734 @ 02391734 ----

undefined2 * FUN_02391734(undefined2 *param_1,undefined2 param_2)

{
  ushort uVar1;
  undefined4 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  uVar2 = DAT_0239178c;
  param_1[5] = 0;
  param_1[6] = (short)uVar2;
  param_1[7] = 1;
  param_1[8] = param_2;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391790 @ 02391790 ----

undefined2 * FUN_02391790(undefined2 *param_1,undefined2 param_2)

{
  ushort uVar1;
  undefined4 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  uVar2 = DAT_023917e8;
  param_1[5] = 0;
  param_1[6] = (short)uVar2;
  param_1[7] = 1;
  param_1[8] = param_2;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391860 @ 02391860 ----

undefined2 * FUN_02391860(undefined2 *param_1,undefined2 param_2)

{
  ushort uVar1;
  undefined4 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  uVar2 = DAT_023918b8;
  param_1[5] = 0;
  param_1[6] = (short)uVar2;
  param_1[7] = 1;
  param_1[8] = param_2;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_023918bc @ 023918bc ----

undefined2 *
FUN_023918bc(undefined2 *param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4)

{
  ushort uVar1;
  undefined4 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  uVar2 = DAT_02391920;
  param_1[5] = 0;
  param_1[6] = (short)uVar2;
  param_1[7] = 3;
  param_1[8] = param_2;
  param_1[9] = param_3;
  param_1[10] = param_4;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391980 @ 02391980 ----

undefined2 * FUN_02391980(undefined2 *param_1,undefined2 param_2)

{
  ushort uVar1;
  undefined4 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  uVar2 = DAT_023919d8;
  param_1[5] = 0;
  param_1[6] = (short)uVar2;
  param_1[7] = 1;
  param_1[8] = param_2;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_023919dc @ 023919dc ----

undefined2 * FUN_023919dc(undefined2 *param_1,undefined2 param_2)

{
  ushort uVar1;
  undefined4 uVar2;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  uVar2 = DAT_02391a34;
  param_1[5] = 0;
  param_1[6] = (short)uVar2;
  param_1[7] = 1;
  param_1[8] = param_2;
  uVar1 = param_1[7];
  param_1[uVar1 + 8] = param_1[6];
  param_1[uVar1 + 9] = 1;
  FUN_0238f4d4();
  return param_1 + uVar1 + 8;
}



// ---- FUN_02391b18 @ 02391b18 ----

void FUN_02391b18(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391b24. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391b28)(param_1,DAT_02391b2c,4);
  return;
}



// ---- FUN_02391b30 @ 02391b30 ----

void FUN_02391b30(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391b3c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391b40)(param_1,DAT_02391b44,3);
  return;
}



// ---- FUN_02391b5c @ 02391b5c ----

void FUN_02391b5c(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391b68. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391b6c)(param_1,DAT_02391b70,1);
  return;
}



// ---- FUN_02391b74 @ 02391b74 ----

void FUN_02391b74(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391b80. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391b84)(param_1,DAT_02391b88,1);
  return;
}



// ---- FUN_02391b8c @ 02391b8c ----

void FUN_02391b8c(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391b98. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391b9c)(param_1,DAT_02391ba0,1);
  return;
}



// ---- FUN_02391ba4 @ 02391ba4 ----

void FUN_02391ba4(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391bb0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391bb4)(param_1,0x304,1);
  return;
}



// ---- FUN_02391bb8 @ 02391bb8 ----

void FUN_02391bb8(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391bc4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391bc8)(param_1,DAT_02391bcc,1);
  return;
}



// ---- FUN_02391bd0 @ 02391bd0 ----

void FUN_02391bd0(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391bdc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391be0)(param_1,DAT_02391be4,9);
  return;
}



// ---- FUN_02391be8 @ 02391be8 ----

void FUN_02391be8(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391bf4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391bf8)(param_1,DAT_02391bfc,0x5c);
  return;
}



// ---- FUN_02391c00 @ 02391c00 ----

void FUN_02391c00(undefined4 param_1)

{
                    /* WARNING: Could not recover jumptable at 0x02391c0c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02391c10)(param_1,0x308,2);
  return;
}



// ---- FUN_02391ccc @ 02391ccc ----

void FUN_02391ccc(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined2 *puVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  undefined2 local_10;
  undefined2 local_e;
  undefined4 local_c;
  
  iVar1 = DAT_02391d78;
  puVar4 = *(undefined4 **)(param_1 + 4);
  *(undefined4 **)(DAT_02391d78 + 0x54c) = puVar4;
  uVar3 = *(undefined4 *)(param_1 + 8);
  *(undefined4 *)(iVar1 + 0x550) = uVar3;
  *puVar4 = uVar3;
  puVar4[2] = *(undefined4 *)(param_1 + 0xc);
  local_c = param_4;
  FUN_0239702c();
  func_0x033b42b4(0xf);
  *(undefined2 *)*puVar4 = 1;
  iVar1 = FUN_0239728c(&local_e,&local_10);
  if (iVar1 == 0) {
    puVar2 = (undefined2 *)func_0x033b61d8();
    *puVar2 = 0;
    puVar2[1] = 1;
    puVar2[2] = local_e;
    puVar2[3] = local_10;
    func_0x033b618c();
  }
  else {
    *(undefined2 *)*puVar4 = 2;
    puVar2 = (undefined2 *)func_0x033b61d8();
    *puVar2 = 0;
    puVar2[1] = 0;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_0239218c @ 0239218c ----

void FUN_0239218c(void)

{
  short sVar1;
  undefined2 *puVar2;
  int iVar3;
  undefined4 in_r3;
  short *psVar4;
  undefined1 auStack_210 [512];
  undefined4 local_10;
  
  psVar4 = *(short **)(DAT_02392238 + 0x550);
  local_10 = in_r3;
  if (*psVar4 == 2) {
    iVar3 = FUN_02391b5c(auStack_210);
    sVar1 = *(short *)(iVar3 + 4);
    if (sVar1 == 0) {
      *psVar4 = 1;
      func_0x033b42b4();
      *psVar4 = 0;
      puVar2 = (undefined2 *)func_0x033b61d8();
      *puVar2 = 2;
      puVar2[1] = 0;
      func_0x033b618c();
    }
    else {
      puVar2 = (undefined2 *)func_0x033b61d8();
      *puVar2 = 2;
      puVar2[1] = 1;
      puVar2[2] = 0x301;
      puVar2[3] = sVar1;
      func_0x033b618c();
    }
  }
  else {
    puVar2 = (undefined2 *)func_0x033b61d8();
    *puVar2 = 2;
    puVar2[1] = 3;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_023925b8 @ 023925b8 ----

void FUN_023925b8(void)

{
  short sVar1;
  ushort uVar2;
  undefined2 *puVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  short *psVar7;
  undefined1 auStack_228 [8];
  undefined1 auStack_220 [512];
  
  psVar7 = *(short **)(DAT_02392774 + 0x550);
  if (*psVar7 == 7) {
    psVar7[0x7b] = 0;
    uVar5 = 1;
    do {
      if (((uint)(ushort)psVar7[0xc1] & 1 << (uVar5 & 0xff)) != 0) {
        func_0x033ad310(psVar7 + (uVar5 - 1) * 3 + 0x94,auStack_228);
        for (iVar6 = 0; iVar6 < 2; iVar6 = iVar6 + 1) {
          iVar4 = FUN_023912a8(auStack_220,auStack_228,3);
          sVar1 = *(short *)(iVar4 + 4);
          if ((sVar1 == 0) || (sVar1 != 7 && sVar1 != 0xc)) break;
        }
        func_0x033acf5c();
        if (((uint)(ushort)psVar7[0xc1] & 1 << (uVar5 & 0xff)) == 0) {
          func_0x033acf70();
        }
        else {
          uVar2 = ~(ushort)(1 << (uVar5 & 0xff));
          psVar7[0xc1] = psVar7[0xc1] & uVar2;
          psVar7[0x43] = psVar7[0x43] & uVar2;
          (psVar7 + uVar5 * 4 + 0x39c)[0] = 0;
          (psVar7 + uVar5 * 4 + 0x39c)[1] = 0;
          (psVar7 + uVar5 * 4 + 0x39e)[0] = 0;
          (psVar7 + uVar5 * 4 + 0x39e)[1] = 0;
          func_0x033acf70();
          FUN_02393d70(1,uVar5 & 0xffff,auStack_228);
        }
      }
      uVar5 = uVar5 + 1;
    } while ((int)uVar5 < 0x10);
    iVar6 = FUN_02391044(auStack_220,1);
    if (*(short *)(iVar6 + 4) == 0) {
      psVar7[0x61] = 0;
      *psVar7 = 3;
      iVar6 = FUN_02391b74(auStack_220);
      if (*(short *)(iVar6 + 4) == 0) {
        *psVar7 = 2;
        psVar7[0xcc] = 0;
        psVar7[0xcd] = 0;
        psVar7[0xcb] = 0;
        func_0x033ad27c(psVar7 + 0xce,0,0x50);
        FUN_0238fa58();
        puVar3 = (undefined2 *)func_0x033b61d8();
        *puVar3 = 9;
        puVar3[1] = 0;
        func_0x033b618c();
      }
      else {
        FUN_0239277c(DAT_02392778);
      }
    }
    else {
      FUN_0239277c();
    }
  }
  else {
    puVar3 = (undefined2 *)func_0x033b61d8();
    *puVar3 = 9;
    puVar3[1] = 3;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_0239277c @ 0239277c ----

void FUN_0239277c(undefined2 param_1,undefined2 param_2)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 9;
  puVar1[1] = 1;
  puVar1[2] = param_1;
  puVar1[3] = param_2;
  func_0x033b618c();
  return;
}



// ---- FUN_023927b0 @ 023927b0 ----

void FUN_023927b0(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  short sVar1;
  ushort uVar2;
  ushort uVar3;
  uint uVar4;
  undefined2 uVar5;
  undefined2 *puVar6;
  int iVar7;
  undefined4 uVar8;
  short *psVar9;
  ushort local_250 [3];
  undefined1 local_24a;
  undefined1 auStack_249 [15];
  undefined1 auStack_23a [34];
  undefined1 auStack_218 [512];
  undefined4 local_18;
  
  psVar9 = *(short **)(DAT_02392b00 + 0x550);
  sVar1 = *psVar9;
  local_18 = param_4;
  if ((sVar1 == 2 || sVar1 == 3) || sVar1 == 5) {
    *(undefined4 *)(psVar9 + 0xc2) = *(undefined4 *)(param_1 + 4);
    uVar2 = *(ushort *)(param_1 + 2);
    psVar9[200] = uVar2;
    uVar5 = *(undefined2 *)(param_1 + 8);
    func_0x033ad310(param_1 + 10,local_250,6);
    if ((local_250[0] != DAT_02392b04) && ((local_250[0] & 1) != 0)) {
      local_250[0] = local_250[0] & 0xfffe;
    }
    if (uVar2 == 0) {
      puVar6 = (undefined2 *)func_0x033b61d8();
      *puVar6 = 10;
      puVar6[1] = 6;
      puVar6[4] = 4;
      func_0x033b618c();
    }
    else if (((uint)(ushort)psVar9[0xfa] & 1 << (uVar2 & 0xff)) == 0) {
      puVar6 = (undefined2 *)func_0x033b61d8();
      *puVar6 = 10;
      puVar6[1] = 6;
      puVar6[4] = 4;
      func_0x033b618c();
    }
    else {
      psVar9[0x73] = 2;
      iVar7 = FUN_02391c00(auStack_218);
      if (*(short *)(iVar7 + 4) == 0) {
        if (*(short *)(iVar7 + 6) == 0x10) {
          iVar7 = FUN_0238f6bc(10,auStack_218);
          if (iVar7 == 0) {
            return;
          }
          iVar7 = FUN_02391b8c(auStack_218);
          if (*(short *)(iVar7 + 4) != 0) {
            FUN_02393068(DAT_02392b08);
            return;
          }
          *psVar9 = 3;
          iVar7 = FUN_02391098(auStack_218,1,0,1);
          if (*(short *)(iVar7 + 4) != 0) {
            FUN_02393068(1,*(short *)(iVar7 + 4),0);
            return;
          }
          psVar9[99] = 1;
        }
        uVar4 = DAT_02392b04;
        *psVar9 = 5;
        func_0x033ad1d0(uVar4,auStack_23a,0x20);
        local_24a = (undefined1)uVar2;
        func_0x033ad27c(auStack_249,0,0xf);
        iVar7 = FUN_023910f8(auStack_218,DAT_02392b0c,local_250,0,auStack_23a,1,&local_24a,uVar5);
        if (*(short *)(iVar7 + 4) == 0) {
          puVar6 = (undefined2 *)func_0x033b61d8();
          if (*(short *)(iVar7 + 8) == 0) {
            *puVar6 = 10;
            puVar6[1] = 0;
            puVar6[4] = 4;
            puVar6[8] = uVar2;
            puVar6[9] = 0;
          }
          else {
            func_0x033ad1d0(0,*(int *)(psVar9 + 0xc2) + 0x40,0x80);
            func_0x033ad310(iVar7 + 10,*(undefined4 *)(psVar9 + 0xc2),
                            (uint)*(ushort *)(iVar7 + 10) << 1);
            *puVar6 = 10;
            puVar6[1] = 0;
            puVar6[4] = 5;
            puVar6[8] = *(undefined2 *)(iVar7 + 0x40);
            uVar8 = FUN_02392b10(*(ushort *)(iVar7 + 0xc) & 0xff);
            uVar5 = FUN_0238f8c4();
            puVar6[9] = uVar5;
            FUN_02392b24(uVar8);
            puVar6[10] = *(undefined2 *)(iVar7 + 0x14);
            func_0x033ad310(iVar7 + 0xe,puVar6 + 5,6);
            func_0x033ad1e8(iVar7 + 0x16,puVar6 + 0xb,0x20);
            uVar3 = *(ushort *)(iVar7 + 0x46);
            puVar6[0x1b] = uVar3;
            if (uVar3 < 0x81) {
              func_0x033ad1d0(0,puVar6 + 0x1c,0x80);
              func_0x033ad1e8(iVar7 + 0x4a,puVar6 + 0x1c,(ushort)puVar6[0x1b] + 1 & 0xfffffffe);
            }
            else {
              *puVar6 = 10;
              puVar6[1] = 0;
              puVar6[4] = 4;
              puVar6[8] = uVar2;
              puVar6[9] = 0;
            }
          }
          func_0x033b618c(puVar6);
        }
        else {
          FUN_02393068(2,*(short *)(iVar7 + 4),0);
        }
      }
      else {
        FUN_02393068(0x308,*(short *)(iVar7 + 4),0);
      }
    }
  }
  else {
    puVar6 = (undefined2 *)func_0x033b61d8();
    *puVar6 = 10;
    puVar6[1] = 3;
    puVar6[4] = 4;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_02392b10 @ 02392b10 ----

uint FUN_02392b10(uint param_1)

{
  uint uVar1;
  
  uVar1 = (int)param_1 >> 2;
  if ((param_1 & 2) == 0) {
    uVar1 = uVar1 + 0x19;
  }
  return uVar1 & 0xff;
}



// ---- FUN_02392b24 @ 02392b24 ----

void FUN_02392b24(uint param_1)

{
  param_1 = param_1 ^ (uint)*DAT_02392b3c << 1;
  *DAT_02392b3c = (ushort)param_1 ^ (ushort)(param_1 >> 0x10);
  return;
}



// ---- FUN_02393068 @ 02393068 ----

void FUN_02393068(undefined2 param_1,undefined2 param_2,int param_3)

{
  undefined2 *puVar1;
  undefined2 uVar2;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  if (param_3 == 0) {
    uVar2 = 10;
  }
  else {
    uVar2 = 0x26;
  }
  *puVar1 = uVar2;
  puVar1[1] = 1;
  puVar1[4] = 4;
  puVar1[2] = param_1;
  puVar1[3] = param_2;
  func_0x033b618c();
  return;
}



// ---- FUN_023930b0 @ 023930b0 ----

void FUN_023930b0(void)

{
  undefined2 *puVar1;
  int iVar2;
  undefined4 in_r3;
  short *psVar3;
  undefined1 auStack_210 [512];
  undefined4 local_10;
  
  psVar3 = *(short **)(DAT_02393178 + 0x550);
  local_10 = in_r3;
  if (*psVar3 == 5) {
    iVar2 = FUN_02391b74(auStack_210);
    if (*(short *)(iVar2 + 4) == 0) {
      *psVar3 = 2;
      if (psVar3[0xf7] == 0) {
        iVar2 = FUN_02391860(auStack_210,1);
        if (*(short *)(iVar2 + 4) != 0) {
          FUN_02393184(DAT_02393180);
          return;
        }
        psVar3[0xf7] = 1;
      }
      puVar1 = (undefined2 *)func_0x033b61d8();
      *puVar1 = 0xb;
      puVar1[1] = 0;
      func_0x033b618c();
    }
    else {
      FUN_02393184(DAT_0239317c);
    }
  }
  else {
    puVar1 = (undefined2 *)func_0x033b61d8();
    *puVar1 = 0xb;
    puVar1[1] = 3;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_02393184 @ 02393184 ----

void FUN_02393184(undefined2 param_1,undefined2 param_2)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 0xb;
  puVar1[1] = 1;
  puVar1[2] = param_1;
  puVar1[3] = param_2;
  func_0x033b618c();
  return;
}



// ---- FUN_023931b8 @ 023931b8 ----

void FUN_023931b8(int param_1)

{
  short sVar1;
  ushort uVar2;
  undefined2 *puVar3;
  int iVar4;
  uint uVar5;
  undefined4 uVar6;
  int extraout_r1;
  undefined1 *puVar7;
  uint uVar8;
  int iVar9;
  short *psVar10;
  bool bVar11;
  undefined8 uVar12;
  undefined1 auStack_268 [6];
  undefined1 auStack_262 [6];
  undefined1 auStack_25c [10];
  undefined2 local_252;
  undefined2 local_250;
  undefined2 local_24e;
  undefined2 local_24c;
  undefined2 local_24a;
  undefined1 auStack_248 [48];
  undefined1 auStack_218 [512];
  
  psVar10 = *(short **)(DAT_0239373c + 0x550);
  iVar9 = *(int *)(DAT_0239373c + 0x54c);
  if (*psVar10 == 2) {
    func_0x033ad310(*(undefined4 *)(param_1 + 4),iVar9 + 0x10,0xc0);
    if ((*(ushort *)(iVar9 + 0x4c) < 0x10) || ((*(byte *)(iVar9 + 0x5b) & 1) != 0)) {
      uVar8 = 1 << (*(ushort *)(iVar9 + 0x46) & 0xff);
      if (((uVar8 & (ushort)psVar10[0xfa]) == 0) || (((int)uVar8 >> 1 & 0x1fffU) == 0)) {
        puVar3 = (undefined2 *)func_0x033b61d8();
        *puVar3 = 0xc;
        puVar3[1] = 6;
        puVar3[4] = 6;
        func_0x033b618c();
      }
      else {
        puVar3 = (undefined2 *)func_0x033b61d8();
        *puVar3 = 0xc;
        puVar3[1] = 0;
        puVar3[4] = 6;
        func_0x033b618c();
        if (psVar10[0xf6] == 1) {
          bVar11 = (*(ushort *)(iVar9 + 0x3e) & 1) == 0;
          if (bVar11) {
            sVar1 = 2;
          }
          else {
            sVar1 = 1;
            psVar10[0xf6] = 1;
          }
        }
        else {
          bVar11 = (*(ushort *)(iVar9 + 0x3e) & 2) == 0;
          if (bVar11) {
            sVar1 = 1;
          }
          else {
            sVar1 = 2;
            psVar10[0xf6] = 2;
          }
        }
        if (bVar11) {
          psVar10[0xf6] = sVar1;
        }
        psVar10[0xf7] = (ushort)((*(ushort *)(iVar9 + 0x3c) & 0x20) != 0);
        if (*(short *)(iVar9 + 0x4c) == 0) {
          sVar1 = 3;
        }
        else {
          sVar1 = 2;
        }
        psVar10[0x73] = sVar1;
        iVar4 = FUN_0238f6bc(0xc,auStack_218);
        if (iVar4 != 0) {
          iVar4 = FUN_023919dc(auStack_218,0);
          if (*(short *)(iVar4 + 4) == 0) {
            if (*(ushort *)(iVar9 + 0x4c) < 0x10) {
              if (*(short *)(iVar9 + 0x42) == 0) {
                uVar2 = 1;
              }
              else {
                sVar1 = func_0x033b5a20(DAT_02393744);
                uVar2 = sVar1 + 1;
              }
              if (0xff < uVar2) {
                uVar2 = 0xff;
              }
              iVar4 = FUN_02391790(auStack_218,uVar2);
              if (*(short *)(iVar4 + 4) != 0) {
                FUN_02393750(DAT_02393748,*(short *)(iVar4 + 4),0);
                return;
              }
            }
            iVar4 = FUN_02391b8c(auStack_218);
            if (*(short *)(iVar4 + 4) == 0) {
              *psVar10 = 3;
              bVar11 = *(int *)(param_1 + 0x20) != 0;
              iVar4 = FUN_02391098(auStack_218,bVar11,0,1);
              if (*(short *)(iVar4 + 4) == 0) {
                psVar10[99] = (ushort)bVar11;
                func_0x033ad310(iVar9 + 0x10,auStack_25c,0x40);
                if (psVar10[0x73] == 2) {
                  local_252 = 0x20;
                  local_250 = (undefined2)*(undefined4 *)(iVar9 + 0x54);
                  local_24e = (undefined2)((uint)*(undefined4 *)(iVar9 + 0x54) >> 0x10);
                  local_24c = *(undefined2 *)(iVar9 + 0x58);
                  local_24a = 0;
                  func_0x033ad310(param_1 + 8,auStack_248,0x18);
                }
                puVar7 = auStack_25c;
                iVar4 = FUN_023911b0(auStack_218,2000);
                sVar1 = *(short *)(iVar4 + 4);
                if (sVar1 == 0) {
                  puVar7 = (undefined1 *)(uint)*(ushort *)(iVar4 + 6);
                }
                if (sVar1 == 0 && puVar7 == (undefined1 *)0x0) {
                  func_0x033ad310(iVar4 + 8,psVar10 + 0xc5,6);
                  func_0x033ad310(psVar10 + 0xc5,auStack_262,6);
                  uVar8 = (uint)*(ushort *)(param_1 + 0x26);
                  iVar4 = FUN_02391228(auStack_218,auStack_262,uVar8,2000);
                  sVar1 = *(short *)(iVar4 + 4);
                  if (sVar1 == 0xc) {
                    uVar8 = (uint)*(ushort *)(iVar4 + 6);
                  }
                  if (sVar1 != 0xc || uVar8 != 0x13) {
                    if (sVar1 == 0) {
                      uVar8 = (uint)*(ushort *)(iVar4 + 6);
                    }
                    if (sVar1 == 0 && uVar8 == 0) {
                      func_0x033ad310(psVar10 + 0xc5,auStack_268,6);
                      iVar4 = FUN_02391320(auStack_218,auStack_268,1,2000);
                      uVar12 = func_0x033acf5c();
                      uVar8 = (uint)((ulonglong)uVar12 >> 0x20);
                      uVar5 = (uint)uVar12;
                      sVar1 = *(short *)(iVar4 + 4);
                      if (sVar1 == 0xc) {
                        uVar8 = (uint)*(ushort *)(iVar4 + 6);
                      }
                      if (sVar1 != 0xc || uVar8 != 0x13) {
                        uVar8 = uVar5;
                        if (sVar1 == 0) {
                          uVar8 = (uint)*(ushort *)(iVar4 + 6);
                        }
                        if (sVar1 == 0 && uVar8 == 0) {
                          psVar10[0xc4] = *(short *)(iVar4 + 8);
                          psVar10[0x5d] = *(short *)(iVar9 + 0x58);
                          func_0x033ad1d0(1,psVar10 + 0xfc,0x10);
                          iVar4 = (int)(*(ushort *)(iVar9 + 0x12) & 0xff) >> 2;
                          if ((*(ushort *)(iVar9 + 0x12) & 2) == 0) {
                            iVar4 = iVar4 + 0x19;
                          }
                          sVar1 = FUN_0238f8c4(iVar4);
                          psVar10[0x5e] = sVar1;
                          FUN_0238f850(iVar4);
                          uVar6 = func_0x033acf5c();
                          psVar10[0xc1] = 1;
                          psVar10[0x43] = 1;
                          iVar4 = *(int *)(psVar10 + 0x3de);
                          if (iVar4 != 0 || *(int *)(psVar10 + 0x3dc) != 0) {
                            uVar12 = func_0x033ac464();
                            iVar4 = (int)((ulonglong)uVar12 >> 0x20);
                            *(uint *)(psVar10 + 0x39c) = (uint)uVar12 | 1;
                            *(int *)(psVar10 + 0x39e) = iVar4;
                          }
                          *psVar10 = 8;
                          bVar11 = (*(byte *)(iVar9 + 0x5b) & 4) != 0;
                          if (bVar11) {
                            iVar4 = 0x2a;
                          }
                          if (!bVar11) {
                            iVar4 = 0;
                          }
                          FUN_0238fa8c((uint)*(ushort *)(iVar9 + 0x5c) + iVar4 & 0xffff);
                          bVar11 = (*(byte *)(iVar9 + 0x5b) & 4) != 0;
                          iVar4 = extraout_r1;
                          if (bVar11) {
                            iVar4 = 6;
                          }
                          if (!bVar11) {
                            iVar4 = 0;
                          }
                          FUN_0238fad4((uint)*(ushort *)(iVar9 + 0x5e) + iVar4 & 0xffff);
                          func_0x033acf70(uVar6);
                          psVar10[0x61] = 1;
                          puVar3 = (undefined2 *)func_0x033b61d8();
                          *puVar3 = 0xc;
                          puVar3[1] = 0;
                          puVar3[4] = 7;
                          puVar3[5] = psVar10[0xc4];
                          func_0x033ad310(psVar10 + 0xc5,puVar3 + 8,6);
                          puVar3[0xb] = psVar10[0x18];
                          puVar3[0xc] = psVar10[0x19];
                          func_0x033b618c(puVar3);
                          func_0x033acf70(uVar5);
                        }
                        else {
                          func_0x033acf70(uVar5);
                          FUN_02393750(6,*(undefined2 *)(iVar4 + 4),*(undefined2 *)(iVar4 + 6));
                        }
                      }
                      else {
                        func_0x033acf70();
                        puVar3 = (undefined2 *)func_0x033b61d8();
                        *puVar3 = 0xc;
                        puVar3[1] = 0xc;
                        puVar3[4] = 6;
                        func_0x033b618c();
                      }
                    }
                    else {
                      FUN_02393750(4,sVar1,*(undefined2 *)(iVar4 + 6));
                    }
                  }
                  else {
                    puVar3 = (undefined2 *)func_0x033b61d8();
                    *puVar3 = 0xc;
                    puVar3[1] = 0xc;
                    puVar3[4] = 6;
                    func_0x033b618c();
                  }
                }
                else {
                  FUN_02393750(3,sVar1,*(undefined2 *)(iVar4 + 6));
                }
              }
              else {
                FUN_02393750(1,*(short *)(iVar4 + 4),0);
              }
            }
            else {
              FUN_02393750(DAT_0239374c);
            }
          }
          else {
            FUN_02393750(DAT_02393740,*(short *)(iVar4 + 4),0);
          }
        }
      }
    }
    else {
      puVar3 = (undefined2 *)func_0x033b61d8();
      *puVar3 = 0xc;
      puVar3[1] = 0xb;
      puVar3[4] = 6;
      func_0x033b618c();
    }
  }
  else {
    puVar3 = (undefined2 *)func_0x033b61d8();
    *puVar3 = 0xc;
    puVar3[1] = 3;
    puVar3[4] = 6;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_02393750 @ 02393750 ----

void FUN_02393750(undefined2 param_1,undefined2 param_2,undefined2 param_3)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 0xc;
  puVar1[1] = 1;
  puVar1[2] = param_1;
  puVar1[3] = param_2;
  puVar1[7] = param_3;
  func_0x033b618c();
  return;
}



// ---- FUN_0239378c @ 0239378c ----

void FUN_0239378c(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined2 *puVar2;
  undefined4 uVar3;
  undefined2 local_10 [2];
  undefined4 local_c;
  
  uVar3 = *(undefined4 *)(param_1 + 4);
  local_c = param_4;
  iVar1 = FUN_023937e4(param_1,0,local_10);
  if (iVar1 == 1) {
    puVar2 = (undefined2 *)func_0x033b61d8();
    *puVar2 = 0xd;
    puVar2[1] = 0;
    puVar2[4] = (short)uVar3;
    puVar2[5] = local_10[0];
    func_0x033b618c();
  }
  return;
}



// ---- FUN_023937e4 @ 023937e4 ----

undefined4 FUN_023937e4(int param_1,int param_2,undefined2 *param_3,undefined4 param_4)

{
  uint uVar1;
  uint uVar2;
  short sVar3;
  ushort uVar4;
  undefined2 uVar5;
  int iVar6;
  undefined2 *puVar7;
  undefined4 uVar8;
  uint uVar9;
  short *psVar10;
  int iVar11;
  undefined2 uVar12;
  uint uVar13;
  bool bVar14;
  undefined1 auStack_234 [6];
  undefined1 auStack_22e [6];
  undefined1 auStack_228 [512];
  undefined4 local_28;
  
  if (param_2 == 0) {
    uVar5 = 0;
  }
  else {
    uVar5 = (undefined2)*(undefined4 *)(param_1 + 8);
  }
  uVar13 = 0;
  psVar10 = *(short **)(DAT_02393d68 + 0x550);
  uVar1 = *(uint *)(param_1 + 4) & 0xffff;
  sVar3 = *psVar10;
  bVar14 = false;
  local_28 = param_4;
  if (sVar3 == 9 || sVar3 == 7) {
    bVar14 = *(int *)(psVar10 + 6) == 1;
  }
  else {
    uVar12 = (undefined2)*(uint *)(param_1 + 4);
    if (sVar3 != 10 && sVar3 != 8) {
      if (param_2 == 0) {
        puVar7 = (undefined2 *)func_0x033b61d8();
        *puVar7 = 0xd;
        puVar7[1] = 3;
        puVar7[2] = 0;
        puVar7[3] = 0;
        puVar7[4] = uVar12;
        puVar7[5] = 0;
        func_0x033b618c();
      }
      return 0;
    }
    uVar8 = func_0x033acf5c();
    if (psVar10[0xc1] == 0) {
      func_0x033acf70();
      if (param_2 == 0) {
        puVar7 = (undefined2 *)func_0x033b61d8();
        *puVar7 = 0xd;
        puVar7[1] = 3;
        puVar7[2] = 0;
        puVar7[3] = 0;
        puVar7[4] = uVar12;
        puVar7[5] = 0;
        func_0x033b618c();
      }
      return 0;
    }
    if (*(int *)(psVar10 + 6) == 1) {
      psVar10[6] = 0;
      psVar10[7] = 0;
      bVar14 = true;
      FUN_02394d88();
      FUN_0238f92c();
      if (*psVar10 == 10) {
        *psVar10 = 8;
      }
    }
    psVar10[0xc1] = 0;
    psVar10[0x43] = 0;
    psVar10[10] = 0;
    psVar10[0xb] = 0;
    psVar10[8] = 0;
    psVar10[9] = 0;
    psVar10[0xe] = 0;
    psVar10[0xf] = 0;
    func_0x033acf70(uVar8);
  }
  if (*psVar10 == 10 || *psVar10 == 8) {
    func_0x033ad310(psVar10 + 0xc5,auStack_22e,6);
    for (iVar11 = 0; iVar11 < 2; iVar11 = iVar11 + 1) {
      iVar6 = FUN_023912a8(auStack_228,auStack_22e,3);
      uVar4 = *(ushort *)(iVar6 + 4);
      if (uVar4 < 8) {
        if (uVar4 < 7) {
          if ((1 < uVar4) || (1 < uVar4)) {
LAB_023939bc:
            if (param_2 == 0) {
              FUN_02393e34(5,uVar4,uVar1,0);
            }
            else {
              FUN_02393e78();
            }
            if (bVar14) {
              FUN_023969ec(1);
            }
            return 0;
          }
          break;
        }
      }
      else if (uVar4 != 0xc) goto LAB_023939bc;
    }
    psVar10[0x61] = 0;
    uVar12 = 1;
    *psVar10 = 3;
    iVar11 = FUN_02391044(auStack_228,1);
    if (*(short *)(iVar11 + 4) != 0) {
      if (param_2 == 0) {
        FUN_02393e34(0,*(short *)(iVar11 + 4),uVar1,1);
      }
      else {
        FUN_02393e78();
      }
      if (bVar14) {
        FUN_023969ec(1);
      }
      return 0;
    }
    iVar11 = FUN_02391b74(auStack_228);
    if (*(short *)(iVar11 + 4) != 0) {
      if (param_2 == 0) {
        FUN_02393e34(DAT_02393d6c,*(short *)(iVar11 + 4),uVar1,1);
      }
      else {
        FUN_02393e78();
      }
      if (bVar14) {
        FUN_023969ec(1);
      }
      return 0;
    }
    *psVar10 = 2;
    psVar10[0xcc] = 0;
    psVar10[0xcd] = 0;
    psVar10[0xcb] = 0;
    func_0x033ad27c(psVar10 + 0xce,0,0x50);
    FUN_0238fa58();
    if (param_2 == 1) {
      puVar7 = (undefined2 *)func_0x033b61d8();
      *puVar7 = 0xc;
      puVar7[1] = 0;
      puVar7[4] = 9;
      puVar7[6] = uVar5;
      puVar7[5] = psVar10[0xc4];
      func_0x033ad310(auStack_22e,puVar7 + 8,6);
      puVar7[0xb] = psVar10[0x18];
      puVar7[0xc] = psVar10[0x19];
      func_0x033b618c(puVar7);
    }
    else {
      FUN_02393d70(0,0,auStack_22e);
    }
    if (bVar14) {
      FUN_023969ec(1);
    }
  }
  else {
    for (uVar9 = 1; uVar12 = (undefined2)uVar13, (int)uVar9 < 0x10; uVar9 = uVar9 + 1) {
      uVar2 = 1 << (uVar9 & 0xff);
      if ((uVar2 & (ushort)psVar10[0xc1] & uVar1) != 0) {
        func_0x033ad310(psVar10 + (uVar9 - 1) * 3 + 0x94,auStack_234);
        for (iVar11 = 0; iVar11 < 2; iVar11 = iVar11 + 1) {
          iVar6 = FUN_023912a8(auStack_228,auStack_234,3);
          sVar3 = *(short *)(iVar6 + 4);
          if (sVar3 == 0) break;
          if (sVar3 != 7 && sVar3 != 0xc) {
            if (param_2 == 0) {
              FUN_02393e34(5,sVar3,uVar1,uVar13);
            }
            else {
              FUN_02393e78();
            }
            if (bVar14) {
              FUN_023969ec(1);
            }
            return 0;
          }
        }
        uVar8 = func_0x033acf5c();
        if (((ushort)psVar10[0xc1] & uVar2) == 0) {
          func_0x033acf70();
        }
        else {
          uVar13 = uVar13 | 1 << (uVar9 & 0xff) & 0xffffU;
          psVar10[0xc1] = psVar10[0xc1] & ~(ushort)uVar2;
          psVar10[0x43] = psVar10[0x43] & ~(ushort)uVar2;
          (psVar10 + (uVar9 & 0xffff) * 4 + 0x39c)[0] = 0;
          (psVar10 + (uVar9 & 0xffff) * 4 + 0x39c)[1] = 0;
          (psVar10 + (uVar9 & 0xffff) * 4 + 0x39e)[0] = 0;
          (psVar10 + (uVar9 & 0xffff) * 4 + 0x39e)[1] = 0;
          func_0x033ad27c(psVar10 + (uVar9 - 1) * 3 + 0x94,0,6);
          func_0x033acf70(uVar8);
          if (param_2 == 1) {
            puVar7 = (undefined2 *)func_0x033b61d8();
            *puVar7 = 8;
            puVar7[1] = 0;
            puVar7[4] = 9;
            puVar7[9] = uVar5;
            puVar7[8] = (short)uVar9;
            func_0x033ad310(auStack_234,puVar7 + 5,6);
            puVar7[0x16] = psVar10[0x18];
            puVar7[0x17] = psVar10[0x19];
            func_0x033b618c(puVar7);
          }
          else {
            FUN_02393d70(1,uVar9 & 0xffff,auStack_234);
          }
          if (bVar14) {
            FUN_023969ec(uVar2 & 0xffff);
          }
        }
      }
    }
  }
  if (param_3 != (undefined2 *)0x0) {
    *param_3 = uVar12;
  }
  return 1;
}



// ---- FUN_02393d70 @ 02393d70 ----

void FUN_02393d70(int param_1,undefined2 param_2,undefined4 param_3)

{
  undefined4 uVar1;
  undefined2 *puVar2;
  int iVar3;
  
  iVar3 = *(int *)(DAT_02393e2c + 0x550);
  puVar2 = (undefined2 *)func_0x033b61d8();
  puVar2[1] = 0;
  if (param_1 == 0) {
    *puVar2 = 0xc;
    uVar1 = DAT_02393e30;
    puVar2[4] = 0x1a;
    puVar2[6] = (short)uVar1;
    puVar2[5] = *(undefined2 *)(iVar3 + 0x188);
    func_0x033ad310(param_3,puVar2 + 8,6);
    puVar2[0xb] = *(undefined2 *)(iVar3 + 0x30);
    puVar2[0xc] = *(undefined2 *)(iVar3 + 0x32);
  }
  else {
    *puVar2 = 8;
    puVar2[4] = 0x1a;
    puVar2[9] = (short)DAT_02393e30;
    puVar2[8] = param_2;
    func_0x033ad310(param_3,puVar2 + 5,6);
    puVar2[0x16] = *(undefined2 *)(iVar3 + 0x30);
    puVar2[0x17] = *(undefined2 *)(iVar3 + 0x32);
  }
  func_0x033b618c(puVar2);
  return;
}



// ---- FUN_02393e34 @ 02393e34 ----

void FUN_02393e34(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 0xd;
  puVar1[1] = 1;
  puVar1[2] = param_1;
  puVar1[3] = param_2;
  puVar1[4] = param_3;
  puVar1[5] = param_4;
  func_0x033b618c();
  return;
}



// ---- FUN_02393e78 @ 02393e78 ----

void FUN_02393e78(undefined2 param_1,undefined2 param_2,undefined2 param_3,undefined2 param_4)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 0x25;
  puVar1[1] = 1;
  puVar1[2] = param_1;
  puVar1[3] = param_2;
  puVar1[4] = param_3;
  puVar1[5] = param_4;
  func_0x033b618c();
  return;
}



// ---- FUN_02393ebc @ 02393ebc ----

void FUN_02393ebc(int param_1)

{
  undefined2 *puVar1;
  undefined4 uVar2;
  uint uVar3;
  int iVar4;
  short sVar5;
  int iVar6;
  uint uVar7;
  undefined4 uVar8;
  uint uVar9;
  short *psVar10;
  undefined8 uVar11;
  undefined1 auStack_220 [512];
  
  psVar10 = *(short **)(DAT_02394158 + 0x550);
  iVar6 = *(int *)(param_1 + 4);
  uVar7 = *(uint *)(param_1 + 8);
  uVar8 = *(undefined4 *)(param_1 + 0xc);
  uVar9 = *(uint *)(param_1 + 0x10);
  sVar5 = 0;
  if (psVar10[0x4e] == 0) {
    if (uVar9 < ((ushort)psVar10[0x1e] + 0x1f & 0xffffffe0)) {
      sVar5 = 6;
    }
    if (psVar10[0xc4] == 0) {
      uVar3 = ((ushort)psVar10[0x1f] + 0xc) * (uint)(ushort)psVar10[0x7c] + 0x29;
    }
    else {
      uVar3 = (ushort)psVar10[0x1f] + 0x51;
    }
    if (uVar7 < (uVar3 & 0xffffffe0)) {
      sVar5 = 6;
    }
  }
  if ((psVar10[0x73] == 2) &&
     (((uint)(ushort)psVar10[0xfb] &
      (1 << (*(ushort *)(*(int *)(DAT_0239415c + 0x154c) + 0x46) & 0xff)) >> 1) == 0)) {
    sVar5 = 6;
  }
  if (sVar5 == 0) {
    if (*(int *)(psVar10 + 6) != 0) {
      psVar10[6] = 0;
      psVar10[7] = 0;
      FUN_023969ec(DAT_02394160);
    }
    FUN_02395560();
    FUN_023975a4(param_1 + 0x14,0);
    uVar2 = func_0x033acf5c();
    if ((ushort)(*psVar10 - 7U) < 2) {
      psVar10[0x42] = 0;
      psVar10[0x2f] = 0;
      psVar10[0x30] = 1;
      psVar10[0x44] = 0;
      psVar10[0x4f] = 0;
      psVar10[0x50] = 0x3c;
      psVar10[0x39a] = 0;
      psVar10[0x39b] = 0;
      psVar10[0x45] = 0;
      psVar10[0x46] = 0;
      psVar10[0x47] = 0;
      psVar10[0x48] = 0;
      psVar10[0x33] = 0;
      *(int *)(psVar10 + 0x3a) = iVar6;
      psVar10[0x39] = (short)uVar7;
      *(uint *)(psVar10 + 0x3c) = iVar6 + uVar7;
      psVar10[0x38] = 0;
      *(undefined4 *)(psVar10 + 0x3e) = uVar8;
      psVar10[0x40] = (short)uVar9;
      psVar10[0x31] = 0;
      psVar10[0x32] = 0;
      psVar10[0x34] = 0;
      psVar10[0x35] = 0;
      psVar10[0x5f] = -1;
      psVar10[0x60] = 1;
      uVar11 = func_0x033ac464();
      iVar6 = 0;
      do {
        *(uint *)(psVar10 + iVar6 * 4 + 0x39c) = (uint)uVar11 | 1;
        iVar4 = iVar6 + 1;
        *(int *)(psVar10 + iVar6 * 4 + 0x39e) = (int)((ulonglong)uVar11 >> 0x20);
        iVar6 = iVar4;
      } while (iVar4 < 0x10);
      FUN_0238f98c();
      psVar10[0x67] = 0;
      FUN_02394d9c();
      if (*psVar10 == 8) {
        *psVar10 = 10;
      }
      else if (*psVar10 == 7) {
        *psVar10 = 9;
      }
      puVar1 = (undefined2 *)func_0x033b61d8();
      *puVar1 = 0xe;
      puVar1[1] = 0;
      puVar1[2] = 10;
      func_0x033b618c();
      psVar10[6] = 1;
      psVar10[7] = 0;
      func_0x033acf70(uVar2);
      iVar6 = FUN_023919dc(auStack_220,1);
      if (*(short *)(iVar6 + 4) != 0) {
        puVar1 = (undefined2 *)func_0x033b61d8();
        *puVar1 = 0xe;
        puVar1[1] = 1;
        puVar1[2] = 0x216;
        puVar1[3] = *(undefined2 *)(iVar6 + 4);
        func_0x033b618c();
      }
    }
    else {
      func_0x033acf70();
      puVar1 = (undefined2 *)func_0x033b61d8();
      *puVar1 = 0xe;
      puVar1[1] = 3;
      puVar1[2] = 10;
      func_0x033b618c();
    }
  }
  else {
    puVar1 = (undefined2 *)func_0x033b61d8();
    *puVar1 = 0xe;
    puVar1[1] = sVar5;
    puVar1[2] = 10;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_023943f0 @ 023943f0 ----

void FUN_023943f0(int param_1)

{
  undefined4 uVar1;
  undefined2 *puVar2;
  uint uVar3;
  undefined2 *puVar4;
  int iVar5;
  
  uVar3 = *(uint *)(param_1 + 8);
  puVar4 = *(undefined2 **)(DAT_02394478 + 0x550);
  iVar5 = *(int *)(param_1 + 4);
  uVar1 = func_0x033acf5c();
  *(int *)(puVar4 + 0x58) = iVar5;
  puVar4[0x5c] = (short)uVar3;
  *(uint *)(puVar4 + 0x5a) = iVar5 + (uVar3 & 0xffff);
  puVar4[0x57] = 0;
  *(undefined4 *)(puVar4 + 0x54) = 0;
  puVar4[0x56] = 0;
  *(undefined4 *)(puVar4 + 0xc) = 0;
  *puVar4 = 0xb;
  puVar2 = (undefined2 *)func_0x033b61d8();
  *puVar2 = 0x11;
  puVar2[1] = 0;
  puVar2[2] = 0xe;
  func_0x033b618c();
  *(undefined4 *)(puVar4 + 8) = 1;
  func_0x033acf70(uVar1);
  return;
}



// ---- FUN_02394938 @ 02394938 ----

void FUN_02394938(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 0x1a;
  puVar1[1] = 4;
  func_0x033b618c();
  return;
}



// ---- FUN_0239495c @ 0239495c ----

void FUN_0239495c(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 0x1b;
  puVar1[1] = 4;
  func_0x033b618c();
  return;
}



// ---- FUN_02394980 @ 02394980 ----

void FUN_02394980(int param_1)

{
  short sVar1;
  longlong lVar2;
  int iVar3;
  undefined2 *puVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;
  int iVar8;
  undefined8 uVar9;
  undefined1 auStack_210 [512];
  
  uVar5 = *(uint *)(param_1 + 0x10) & 0xffff;
  iVar8 = *(int *)(DAT_02394aa0 + 0x550);
  iVar3 = FUN_023918bc(auStack_210,*(uint *)(param_1 + 4) & 0xffff,*(uint *)(param_1 + 8) & 0xffff,
                       *(uint *)(param_1 + 0xc) & 0xffff);
  sVar1 = *(short *)(iVar3 + 4);
  if (sVar1 == 0) {
    if (uVar5 == DAT_02394aa4) {
      *(undefined4 *)(iVar8 + 0x7b8) = 0;
      *(undefined4 *)(iVar8 + 0x7bc) = 0;
    }
    else {
      if (uVar5 == 0) {
        uVar7 = 1;
        uVar5 = 0;
      }
      else {
        lVar2 = (ulonglong)DAT_02394aa8 * (ulonglong)(uVar5 * 100);
        uVar7 = (uint)((ulonglong)lVar2 >> 0x20);
        uVar5 = uVar7 >> 6;
        uVar7 = (uint)lVar2 >> 6 | uVar7 * 0x4000000;
      }
      *(uint *)(iVar8 + 0x7b8) = uVar7;
      *(uint *)(iVar8 + 0x7bc) = uVar5;
    }
    uVar9 = func_0x033ac464();
    iVar3 = 0;
    do {
      iVar6 = iVar8 + iVar3 * 8;
      *(uint *)(iVar6 + 0x738) = (uint)uVar9 | 1;
      iVar3 = iVar3 + 1;
      *(int *)(iVar6 + 0x73c) = (int)((ulonglong)uVar9 >> 0x20);
    } while (iVar3 < 0x10);
    puVar4 = (undefined2 *)func_0x033b61d8();
    *puVar4 = 0x1d;
    puVar4[1] = 0;
    func_0x033b618c();
  }
  else {
    puVar4 = (undefined2 *)func_0x033b61d8();
    *puVar4 = 0x1d;
    puVar4[1] = 1;
    puVar4[2] = 0x211;
    puVar4[3] = sVar1;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_02394c88 @ 02394c88 ----

void FUN_02394c88(void)

{
  short sVar1;
  int iVar2;
  undefined2 *puVar3;
  undefined1 auStack_208 [512];
  
  iVar2 = FUN_02391bb8(auStack_208);
  sVar1 = *(short *)(iVar2 + 4);
  if (sVar1 == 0) {
    puVar3 = (undefined2 *)func_0x033b61d8();
    *puVar3 = 0x1f;
    puVar3[1] = 0;
    func_0x033b618c();
  }
  else {
    puVar3 = (undefined2 *)func_0x033b61d8();
    *puVar3 = 0x1f;
    puVar3[1] = 1;
    puVar3[2] = 0x305;
    puVar3[3] = sVar1;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_02394cf0 @ 02394cf0 ----

void FUN_02394cf0(void)

{
  short sVar1;
  int iVar2;
  undefined2 *puVar3;
  undefined4 in_r3;
  undefined1 auStack_210 [512];
  undefined4 local_10;
  
  local_10 = in_r3;
  iVar2 = FUN_02391be8(auStack_210);
  sVar1 = *(short *)(iVar2 + 4);
  if (sVar1 == 0) {
    puVar3 = (undefined2 *)func_0x033b61d8();
    *puVar3 = 0x20;
    puVar3[1] = 0;
    func_0x033ad1e8(iVar2 + 8,puVar3 + 4,0xb4);
    func_0x033b618c(puVar3);
  }
  else {
    puVar3 = (undefined2 *)func_0x033b61d8();
    *puVar3 = 0x20;
    puVar3[1] = 1;
    puVar3[2] = 0x307;
    puVar3[3] = sVar1;
    func_0x033b618c();
  }
  return;
}



// ---- FUN_02394d74 @ 02394d74 ----

void FUN_02394d74(void)

{
                    /* WARNING: Could not recover jumptable at 0x02394d7c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02394d80)(DAT_02394d84);
  return;
}



// ---- FUN_02394d88 @ 02394d88 ----

void FUN_02394d88(void)

{
                    /* WARNING: Could not recover jumptable at 0x02394d90. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02394d94)(DAT_02394d98);
  return;
}



// ---- FUN_02394d9c @ 02394d9c ----

void FUN_02394d9c(void)

{
  int *piVar1;
  undefined4 in_r3;
  int iVar2;
  
  piVar1 = DAT_02394e40;
  iVar2 = *(int *)(DAT_02394e3c + 0x550);
  if (*(short *)(iVar2 + 0xe6) == 1) {
    if (*DAT_02394e40 != 0) {
      func_0x033acc94();
    }
    func_0x033acaf4(DAT_02394e40,0xd1,0x107,DAT_02394e44,3,in_r3);
  }
  else if (*(short *)(iVar2 + 0xe6) == 2) {
    *(undefined4 *)(iVar2 + 0x1c) = 0;
    if (*piVar1 != 0) {
      func_0x033acc94();
    }
    func_0x033acaf4(DAT_02394e40,200,0x107,DAT_02394e48,1,in_r3);
    *(undefined4 *)(iVar2 + 0xd8) = 0;
  }
  return;
}



// ---- FUN_02395560 @ 02395560 ----

void FUN_02395560(void)

{
  undefined2 uVar1;
  undefined2 uVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  
  iVar6 = *(int *)(DAT_02395610 + 0x550);
  func_0x033abad0(iVar6 + 0x71c);
  func_0x033ad1d0(0,iVar6 + 0x2f8,0x400);
  uVar5 = 0;
  do {
    uVar3 = uVar5 + 1;
    iVar4 = uVar5 * 0x20;
    uVar5 = uVar3 & 0xffff;
    uVar1 = (undefined2)(uVar3 * 0x10000 >> 0x10);
    *(undefined2 *)(iVar6 + iVar4 + 0x2f8) = uVar1;
  } while (uVar5 < 0x1f);
  uVar2 = (undefined2)DAT_02395614;
  *(undefined2 *)(iVar6 + uVar5 * 0x20 + 0x2f8) = uVar2;
  uVar5 = 0;
  *(undefined2 *)(iVar6 + 0x6f8) = 0;
  *(undefined2 *)(iVar6 + 0x6fa) = uVar1;
  do {
    iVar4 = iVar6 + uVar5 * 4;
    *(undefined2 *)(iVar4 + 0x70c) = uVar2;
    *(undefined2 *)(iVar4 + 0x70e) = uVar2;
    *(undefined2 *)(iVar4 + 0x6fc) = uVar2;
    uVar5 = uVar5 + 1 & 0xffff;
    *(undefined2 *)(iVar4 + 0x6fe) = uVar2;
  } while (uVar5 < 4);
  func_0x033abb54(iVar6 + 0x71c);
  return;
}



// ---- FUN_023969ec @ 023969ec ----

void FUN_023969ec(ushort param_1)

{
  undefined2 uVar1;
  undefined2 *puVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  int iVar5;
  int iVar6;
  ushort *puVar7;
  ushort *puVar8;
  int iVar9;
  uint uVar10;
  uint uVar11;
  ushort uVar12;
  uint local_38;
  ushort *local_34;
  int local_2c;
  
  iVar9 = *(int *)(DAT_02396bd8 + 0x550);
  iVar5 = iVar9 + 0x2f8;
  uVar12 = ~param_1 & *(ushort *)(iVar9 + 0x182);
  func_0x033abad0(iVar9 + 0x71c);
  local_2c = 0;
  do {
    iVar6 = 0;
    do {
      puVar7 = (ushort *)(iVar9 + 0x70c + iVar6 * 4);
      uVar10 = (uint)*(ushort *)(iVar9 + 0x70c + iVar6 * 4);
      local_38 = DAT_02396bdc;
      local_34 = puVar7;
      while (uVar10 != DAT_02396bdc) {
        puVar8 = (ushort *)(iVar5 + uVar10 * 0x20);
        puVar8[3] = puVar8[3] & uVar12;
        puVar8[5] = puVar8[5] & uVar12;
        uVar11 = uVar10;
        if (puVar8[3] == 0) {
          puVar2 = (undefined2 *)func_0x033b61d8();
          *puVar2 = 0x81;
          puVar2[1] = 0;
          puVar2[4] = 0x14;
          puVar2[5] = puVar8[1];
          puVar2[6] = puVar8[2];
          puVar2[7] = puVar8[3];
          puVar2[8] = puVar8[4];
          puVar2[0xc] = puVar8[7];
          *(undefined4 *)(puVar2 + 10) = *(undefined4 *)(puVar8 + 10);
          *(undefined4 *)(puVar2 + 0xe) = *(undefined4 *)(puVar8 + 0xc);
          *(undefined4 *)(puVar2 + 0x10) = *(undefined4 *)(puVar8 + 0xe);
          puVar2[0xd] = puVar8[8];
          uVar1 = *(undefined2 *)(iVar9 + 0x30);
          uVar3 = *(undefined2 *)(iVar9 + 0x32);
          uVar4 = uVar1;
          if (*(short *)(iVar9 + 0x188) != 0) {
            uVar4 = uVar3;
          }
          puVar2[0x12] = uVar4;
          if (*(short *)(iVar9 + 0x188) != 0) {
            uVar3 = uVar1;
          }
          puVar2[0x13] = uVar3;
          func_0x033b618c();
          if (*puVar8 == DAT_02396bdc) {
            puVar7[1] = (ushort)local_38;
          }
          *local_34 = *puVar8;
          uVar11 = DAT_02396bdc;
          *puVar8 = (ushort)DAT_02396bdc;
          uVar1 = (undefined2)uVar10;
          if (*(ushort *)(iVar9 + 0x6fa) == uVar11) {
            *(undefined2 *)(iVar9 + 0x6f8) = uVar1;
          }
          else {
            *(undefined2 *)(iVar5 + (uint)*(ushort *)(iVar9 + 0x6fa) * 0x20) = uVar1;
          }
          *(undefined2 *)(iVar9 + 0x6fa) = uVar1;
          uVar11 = local_38;
        }
        local_38 = uVar11;
        if (uVar11 == DAT_02396bdc) {
          uVar10 = (uint)*puVar7;
          local_34 = puVar7;
        }
        else {
          uVar10 = (uint)*(ushort *)(iVar5 + uVar11 * 0x20);
          local_34 = (ushort *)(iVar5 + uVar11 * 0x20);
        }
      }
      iVar6 = iVar6 + 1;
    } while (iVar6 < 4);
    local_2c = local_2c + 1;
  } while (local_2c < 2);
  func_0x033abb54(iVar9 + 0x71c);
  return;
}



// ---- FUN_02396fcc @ 02396fcc ----

void FUN_02396fcc(int param_1)

{
  int iVar1;
  undefined2 *puVar2;
  undefined4 uVar3;
  undefined4 *puVar4;
  
  iVar1 = DAT_02397028;
  puVar4 = *(undefined4 **)(param_1 + 4);
  *(undefined4 **)(DAT_02397028 + 0x54c) = puVar4;
  uVar3 = *(undefined4 *)(param_1 + 8);
  *(undefined4 *)(iVar1 + 0x550) = uVar3;
  *puVar4 = uVar3;
  puVar4[2] = *(undefined4 *)(param_1 + 0xc);
  FUN_0239702c();
  func_0x033b42b4(0xf);
  *(undefined2 *)*puVar4 = 1;
  puVar2 = (undefined2 *)func_0x033b61d8();
  *puVar2 = 3;
  puVar2[1] = 0;
  func_0x033b618c();
  return;
}



// ---- FUN_0239702c @ 0239702c ----

void FUN_0239702c(void)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  bool bVar7;
  
  iVar6 = *(int *)(DAT_02397170 + 0x550);
  iVar5 = *(int *)(DAT_02397170 + 0x54c);
  uVar3 = func_0x033acf5c();
  bVar7 = *(int *)(iVar6 + 0xc) == 1;
  if (bVar7) {
    *(undefined4 *)(iVar6 + 0xc) = 0;
    FUN_02394d88();
    FUN_0238f92c();
  }
  *(undefined2 *)(iVar6 + 0x182) = 0;
  *(undefined2 *)(iVar6 + 0x86) = 0;
  *(undefined4 *)(iVar6 + 0x14) = 0;
  *(undefined4 *)(iVar6 + 0x10) = 0;
  *(undefined4 *)(iVar6 + 0x1c) = 0;
  *(undefined2 *)(iVar6 + 0xce) = 0;
  *(undefined2 *)(iVar6 + 0xc2) = 0;
  *(undefined2 *)(iVar6 + 0x58) = 1;
  *(undefined2 *)(iVar6 + 0x5a) = 1;
  *(undefined2 *)(iVar6 + 0x5c) = 6;
  *(undefined2 *)(iVar6 + 0x98) = 0;
  *(undefined2 *)(iVar6 + 0x92) = 0;
  *(undefined2 *)(iVar6 + 0x94) = 0;
  *(undefined2 *)(iVar6 + 0x9a) = 0;
  *(undefined2 *)(iVar6 + 0x9c) = 0;
  *(undefined4 *)(iVar6 + 0x198) = 0;
  *(undefined2 *)(iVar6 + 0x196) = 0;
  func_0x033ad27c(iVar6 + 0x19c,0,0x50);
  FUN_0238fa58();
  *(undefined2 *)(iVar6 + 0x40) = 0x104;
  *(undefined2 *)(iVar6 + 0x42) = 0xf0;
  *(undefined2 *)(iVar6 + 0x44) = 1000;
  uVar2 = DAT_02397174;
  *(undefined2 *)(iVar6 + 0x46) = 0;
  *(undefined4 *)(iVar6 + 0x48) = uVar2;
  *(undefined4 *)(iVar6 + 0x4c) = 0;
  *(undefined4 *)(iVar6 + 0x50) = 0;
  *(undefined4 *)(iVar6 + 0x54) = 0;
  *(undefined2 *)(iVar6 + 0xc6) = 0;
  *(undefined2 *)(iVar6 + 0x1ee) = 1;
  func_0x033acf70(uVar3);
  if (bVar7) {
    FUN_023969ec(DAT_02397178);
  }
  iVar4 = 0;
  do {
    iVar1 = iVar4 * 0x10;
    iVar4 = iVar4 + 1;
    *(undefined4 *)(iVar5 + iVar1 + 0xd0) = 0x8000;
  } while (iVar4 < 0x20);
  func_0x033ad1d0(1,iVar6 + 0x1f8,0x100);
  FUN_02390f78();
  func_0x033abab8(iVar6 + 0x71c);
  FUN_02394d74();
  return;
}



// ---- FUN_0239728c @ 0239728c ----

undefined4
FUN_0239728c(undefined2 *param_1,undefined2 *param_2,undefined4 param_3,undefined4 param_4)

{
  ushort uVar1;
  undefined2 *puVar2;
  undefined2 uVar3;
  int iVar4;
  undefined4 uVar5;
  int iVar6;
  undefined1 auStack_218 [512];
  undefined4 local_18;
  
  iVar6 = *(int *)(DAT_02397474 + 0x550);
  local_18 = param_4;
  iVar4 = FUN_02391ba4(auStack_218);
  if (*(short *)(iVar4 + 4) == 0) {
    iVar4 = FUN_02391b74(auStack_218);
    puVar2 = DAT_0239747c;
    if (*(short *)(iVar4 + 4) == 0) {
      *DAT_0239747c = 200;
      puVar2[2] = 2000;
      puVar2[0x16] = (short)DAT_02397480;
      iVar4 = FUN_02391b30(auStack_218);
      if (*(short *)(iVar4 + 4) == 0) {
        uVar1 = *(ushort *)(iVar4 + 6);
        *(ushort *)(iVar6 + 500) = uVar1;
        uVar3 = func_0x033b622c(uVar1 >> 1);
        *(undefined2 *)(iVar6 + 0x1f6) = uVar3;
        FUN_023918bc(auStack_218,DAT_02397488,0x28,5);
        *(undefined4 *)(iVar6 + 0x7b8) = DAT_0239748c;
        *(undefined4 *)(iVar6 + 0x7bc) = 0;
        *(undefined2 *)(iVar6 + 0x1ec) = 2;
        *(undefined2 *)(iVar6 + 0x1ee) = 1;
        iVar4 = FUN_02391bd0(auStack_218);
        if (*(short *)(iVar4 + 4) == 0) {
          func_0x033ad1e8(iVar4 + 6,iVar6 + 0x20,8);
          *(undefined2 *)(iVar6 + 0x28) = *(undefined2 *)(iVar4 + 0xe);
          *(undefined2 *)(iVar6 + 0x2c) = *(undefined2 *)(iVar4 + 0x10);
          *(undefined2 *)(iVar6 + 0x2e) = *(undefined2 *)(iVar4 + 0x12);
          *(undefined2 *)(iVar6 + 0x2a) = *(undefined2 *)(iVar4 + 0x14);
          iVar4 = FUN_02391b18(auStack_218);
          if (*(short *)(iVar4 + 4) == 0) {
            func_0x033ad310(iVar4 + 6,iVar6 + 0xe0,6);
            iVar4 = FUN_02391980(auStack_218,1);
            if (*(short *)(iVar4 + 4) == 0) {
              uVar5 = 1;
            }
            else {
              *param_1 = (short)DAT_02397498;
              uVar5 = 0;
              *param_2 = *(undefined2 *)(iVar4 + 4);
            }
          }
          else {
            *param_1 = (short)DAT_02397494;
            uVar5 = 0;
            *param_2 = *(undefined2 *)(iVar4 + 4);
          }
        }
        else {
          uVar5 = 0;
          *param_1 = (short)DAT_02397490;
          *param_2 = *(undefined2 *)(iVar4 + 4);
        }
      }
      else {
        *param_1 = (short)DAT_02397484;
        uVar5 = 0;
        *param_2 = *(undefined2 *)(iVar4 + 4);
      }
    }
    else {
      *param_1 = (short)DAT_02397478;
      uVar5 = 0;
      *param_2 = *(undefined2 *)(iVar4 + 4);
    }
  }
  else {
    *param_1 = 0x304;
    uVar5 = 0;
    *param_2 = *(undefined2 *)(iVar4 + 4);
  }
  return uVar5;
}



// ---- FUN_023975a4 @ 023975a4 ----

undefined4 FUN_023975a4(uint *param_1,undefined4 *param_2)

{
  ushort uVar1;
  longlong lVar2;
  short sVar3;
  undefined4 uVar4;
  uint uVar5;
  undefined4 uVar6;
  uint uVar7;
  short *psVar8;
  
  psVar8 = *(short **)(DAT_02397888 + 0x550);
  uVar7 = *param_1;
  uVar6 = 0;
  if (((ushort)(*psVar8 - 9U) < 2) && ((uVar7 & 0x2c00) != 0)) {
    uVar7 = uVar7 & 0xffffd3ff;
    uVar6 = 3;
  }
  uVar4 = func_0x033acf5c();
  if (param_2 != (undefined4 *)0x0) {
    *param_2 = DAT_0239788c;
    *(short *)(param_2 + 1) = psVar8[0x2d];
    *(short *)((int)param_2 + 6) = psVar8[0x2d];
    *(short *)(param_2 + 2) = psVar8[0x2d];
    *(short *)((int)param_2 + 10) = psVar8[0x18];
    *(short *)(param_2 + 3) = psVar8[0x19];
    *(short *)((int)param_2 + 0xe) = psVar8[0x22];
    *(short *)(param_2 + 4) = psVar8[0x23];
    *(short *)((int)param_2 + 0x12) = psVar8[0x20];
    *(short *)(param_2 + 5) = psVar8[0x21];
    *(short *)((int)param_2 + 0x16) = psVar8[0x4c];
    *(char *)(param_2 + 6) = (char)psVar8[0x49];
    *(char *)((int)param_2 + 0x19) = (char)psVar8[0x4a];
    *(char *)((int)param_2 + 0x1a) = (char)psVar8[0x4d];
    *(char *)((int)param_2 + 0x1b) = (char)psVar8[0x4e];
  }
  if ((uVar7 & 1) != 0) {
    sVar3 = (short)param_1[1];
    if (sVar3 == 0) {
      sVar3 = 0x10;
    }
    psVar8[0x2c] = sVar3;
  }
  if ((uVar7 & 2) != 0) {
    uVar5 = (uint)*(ushort *)((int)param_1 + 6);
    if (uVar5 == 0) {
      uVar5 = 0x10;
    }
    psVar8[0x2d] = (short)uVar5;
    if ((int)uVar5 < (int)psVar8[0x31]) {
      psVar8[0x31] = (short)uVar5;
    }
  }
  if ((uVar7 & 4) != 0) {
    uVar5 = (uint)(ushort)param_1[2];
    if (uVar5 == 0) {
      uVar5 = 0x10;
    }
    psVar8[0x2e] = (short)uVar5;
    if ((int)uVar5 < (int)psVar8[0x31]) {
      psVar8[0x31] = (short)uVar5;
    }
  }
  if ((uVar7 & 8) != 0) {
    if ((ushort)psVar8[0x1a] < (*(short *)((int)param_1 + 10) + 1U & 0xfffe)) {
      uVar6 = 6;
    }
    else {
      FUN_0238fb1c();
    }
  }
  if ((uVar7 & 0x10) != 0) {
    if ((ushort)psVar8[0x1b] < ((short)param_1[3] + 1U & 0xfffe)) {
      uVar6 = 6;
    }
    else {
      FUN_0238fb48();
    }
  }
  if ((uVar7 & 0x20) != 0) {
    uVar1 = *(ushort *)((int)param_1 + 0xe);
    if (DAT_02397890 < uVar1) {
      uVar6 = 6;
    }
    else {
      lVar2 = (ulonglong)DAT_02397894 * (ulonglong)(uint)uVar1;
      uVar5 = (uint)((ulonglong)lVar2 >> 0x20);
      psVar8[0x22] = uVar1;
      *(uint *)(psVar8 + 0x24) = ((uint)lVar2 >> 6 | uVar5 * 0x4000000) >> 10 | (uVar5 >> 6) << 0x16
      ;
      psVar8[0x26] = 0;
      psVar8[0x27] = 0;
    }
  }
  if ((uVar7 & 0x40) != 0) {
    uVar1 = (ushort)param_1[4];
    if (DAT_02397890 < uVar1) {
      uVar6 = 6;
    }
    else {
      lVar2 = (ulonglong)DAT_02397894 * (ulonglong)(uint)uVar1;
      uVar5 = (uint)((ulonglong)lVar2 >> 0x20);
      psVar8[0x23] = uVar1;
      *(uint *)(psVar8 + 0x28) = ((uint)lVar2 >> 6 | uVar5 * 0x4000000) >> 10 | (uVar5 >> 6) << 0x16
      ;
      psVar8[0x2a] = 0;
      psVar8[0x2b] = 0;
    }
  }
  if ((uVar7 & 0x80) != 0) {
    uVar5 = (uint)*(ushort *)((int)param_1 + 0x12);
    if ((uVar5 < 0xbf) || ((0xdb < uVar5 && (uVar5 <= DAT_02397898)))) {
      psVar8[0x20] = *(ushort *)((int)param_1 + 0x12);
    }
    else {
      uVar6 = 6;
    }
  }
  if ((uVar7 & 0x100) != 0) {
    uVar5 = (uint)(ushort)param_1[5];
    if ((uVar5 < 0xbf) || ((0xdb < uVar5 && (uVar5 <= DAT_02397898)))) {
      psVar8[0x21] = (ushort)param_1[5];
    }
    else {
      uVar6 = 6;
    }
  }
  if ((uVar7 & 0x200) != 0) {
    psVar8[0x4c] = *(short *)((int)param_1 + 0x16);
  }
  if ((uVar7 & 0x400) != 0) {
    psVar8[0x49] = (ushort)(byte)param_1[6];
  }
  if ((uVar7 & 0x800) != 0) {
    psVar8[0x4a] = (ushort)*(byte *)((int)param_1 + 0x19);
  }
  if ((uVar7 & 0x1000) != 0) {
    psVar8[0x4d] = (ushort)*(byte *)((int)param_1 + 0x1a);
  }
  if ((uVar7 & 0x2000) != 0) {
    psVar8[0x4e] = (ushort)*(byte *)((int)param_1 + 0x1b);
  }
  func_0x033acf70(uVar4);
  return uVar6;
}



// ---- FUN_02397acc @ 02397acc ----

void FUN_02397acc(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)func_0x033b61d8();
  *puVar1 = 0x2a;
  puVar1[1] = 4;
  func_0x033b618c();
  return;
}



// ---- FUN_02397af0 @ 02397af0 ----

void FUN_02397af0(void)

{
  FUN_02399d3c();
  FUN_02398e50();
  FUN_0239987c();
  FUN_02397ea0();
  FUN_02397d20();
  FUN_02397f38(*(undefined4 *)(*DAT_02397b38 + 0x31c),*(undefined2 *)(*DAT_02397b38 + 800));
  FUN_0239b840();
  FUN_0239d20c();
  FUN_0239b5d0();
  FUN_0239890c();
  return;
}



// ---- FUN_02397d0c @ 02397d0c ----

int FUN_02397d0c(void)

{
  return *DAT_02397d1c + 0x18;
}



// ---- FUN_02397d20 @ 02397d20 ----

void FUN_02397d20(void)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 uVar4;
  uint uVar5;
  int iVar6;
  
  uVar4 = DAT_02397da4;
  uVar5 = 0;
  iVar6 = *DAT_02397da0;
  *(undefined2 *)(iVar6 + 0x10) = 0;
  *(undefined2 *)(iVar6 + 0x12) = 0;
  do {
    iVar3 = iVar6 + uVar5 * 2;
    *(short *)(iVar3 + 8) = (short)uVar4;
    iVar1 = uVar5 * 2;
    uVar5 = uVar5 + 1;
    *(undefined2 *)(iVar6 + iVar1) = *(undefined2 *)(iVar3 + 8);
    iVar1 = DAT_02397da8;
    uVar2 = DAT_02397da4;
  } while (uVar5 < 4);
  uVar5 = 0;
  do {
    iVar3 = iVar6 + uVar5 * 8;
    *(short *)(iVar3 + 0xbc) = (short)uVar2;
    uVar4 = *(undefined4 *)(iVar1 + uVar5 * 4);
    *(undefined2 *)(iVar3 + 0xbe) = 0;
    uVar5 = uVar5 + 1;
    *(undefined4 *)(iVar3 + 0xc0) = uVar4;
  } while (uVar5 < 0x18);
  func_0x033a78a0(3,0xc);
  return;
}



// ---- FUN_02397dac @ 02397dac ----

void FUN_02397dac(undefined4 *param_1,undefined2 param_2)

{
  *param_1 = 0xffffffff;
  param_1[1] = 0xffffffff;
  *(undefined2 *)(param_1 + 2) = 0;
  *(undefined2 *)((int)param_1 + 10) = param_2;
  return;
}



// ---- FUN_02397dc8 @ 02397dc8 ----

void FUN_02397dc8(undefined4 *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 uVar2;
  int iVar3;
  
  iVar3 = *DAT_02397e9c;
  *(undefined4 *)(iVar3 + 0x17c) = *param_1;
  *(undefined4 *)(iVar3 + 0x180) = param_1[1];
  uVar2 = param_1[2];
  *(undefined4 *)(iVar3 + 0x184) = uVar2;
  FUN_02397dac(iVar3 + 0x188,2,uVar2,param_4,param_4);
  FUN_02397dac(iVar3 + 0x194,3);
  FUN_02397dac(iVar3 + 0x1a0,4);
  FUN_02397dac(iVar3 + 0x1ac,5);
  FUN_02397dac(iVar3 + 0x1b8,6);
  FUN_02397dac(iVar3 + 0x1c4,7);
  FUN_02397dac(iVar3 + 0x1d0,8);
  FUN_02397dac(iVar3 + 0x1dc,9);
  FUN_02397dac(iVar3 + 0x1e8,10);
  FUN_02397dac(iVar3 + 500,0xb);
  FUN_02397dac(iVar3 + 0x200,0xc);
  iVar1 = func_0x033a7b74(iVar3 + 0x188,0x81);
  *(int *)(iVar3 + 0x3e0) = iVar1 + 0xc;
  *(undefined2 *)(iVar3 + 0x3e4) = 0;
  *(undefined2 *)(iVar3 + 1000) = 0;
  return;
}



// ---- FUN_02397ea0 @ 02397ea0 ----

void FUN_02397ea0(void)

{
  int iVar1;
  
  iVar1 = *DAT_02397ef4;
  FUN_02397ef8(iVar1 + 0x194);
  FUN_02397ef8(iVar1 + 0x1a0);
  FUN_02397ef8(iVar1 + 0x1ac);
  FUN_02397ef8(iVar1 + 0x1b8);
  FUN_02397ef8(iVar1 + 0x1c4);
  FUN_02397ef8(iVar1 + 0x1d0);
  FUN_02397ef8(iVar1 + 0x1dc);
  FUN_02397ef8(iVar1 + 0x1e8);
  return;
}



// ---- FUN_02397ef8 @ 02397ef8 ----

void FUN_02397ef8(int *param_1)

{
  int iVar1;
  
  iVar1 = *param_1;
  if ((short)param_1[2] != 0) {
    while (iVar1 != -1) {
      iVar1 = *(int *)(iVar1 + 4);
      func_0x033a7c10(param_1);
    }
  }
  return;
}



// ---- FUN_02397f38 @ 02397f38 ----

void FUN_02397f38(undefined4 param_1,undefined2 param_2)

{
  int *piVar1;
  undefined4 uVar2;
  
  uVar2 = *(undefined4 *)(*DAT_02397fb4 + 0x3e0);
  func_0x033ad1d0(0,*DAT_02397fb4 + 0x31c,0x28);
  func_0x033ad1d0(0,*DAT_02397fb4 + 0x344,0xc0);
  piVar1 = DAT_02397fb4;
  *(undefined4 *)(*DAT_02397fb4 + 0x31c) = param_1;
  *(undefined2 *)(*piVar1 + 800) = param_2;
  *(undefined2 *)(*piVar1 + 0x322) = param_2;
  *(undefined4 *)(*piVar1 + 0x3e0) = uVar2;
  return;
}



// ---- FUN_02397fb8 @ 02397fb8 ----

undefined4 FUN_02397fb8(ushort *param_1)

{
  undefined4 uVar1;
  
  if ((*param_1 & 1) == 0) {
    FUN_0239923c(*DAT_02398010 + 0x324,param_1);
    FUN_0239923c(DAT_02398014,param_1);
    uVar1 = 0;
    *(uint *)(*DAT_02398010 + 0x340) = *(uint *)(*DAT_02398010 + 0x340) | 2;
  }
  else {
    uVar1 = 5;
  }
  return uVar1;
}



// ---- FUN_02398018 @ 02398018 ----

undefined4 FUN_02398018(uint param_1)

{
  undefined2 *puVar1;
  
  puVar1 = DAT_02398048;
  if (param_1 < 0x100) {
    *(short *)(*DAT_02398044 + 0x32a) = (short)param_1;
    *puVar1 = (short)param_1;
    return 0;
  }
  return 5;
}



// ---- FUN_0239804c @ 0239804c ----

undefined4 FUN_0239804c(uint param_1)

{
  int *piVar1;
  
  piVar1 = DAT_02398088;
  if ((param_1 & DAT_02398084) != 0) {
    *(short *)(*DAT_02398088 + 0x32c) = (short)param_1;
    *(uint *)(*piVar1 + 0x340) = *(uint *)(*piVar1 + 0x340) | 4;
    return 0;
  }
  return 5;
}



// ---- FUN_0239808c @ 0239808c ----

undefined4 FUN_0239808c(uint param_1)

{
  ushort uVar1;
  int *piVar2;
  ushort *puVar3;
  undefined4 uVar4;
  
  uVar4 = DAT_02398108;
  puVar3 = DAT_02398104;
  piVar2 = DAT_02398100;
  if (param_1 < 4) {
    uVar1 = (ushort)param_1;
    *(ushort *)(*DAT_02398100 + 0x32e) = uVar1;
    *(ushort *)(*piVar2 + 0x350) = uVar1;
    *puVar3 = *puVar3 & (ushort)uVar4 | uVar1;
    FUN_02398da8(*(undefined2 *)(*piVar2 + 0x352));
    uVar4 = 0;
    *(uint *)(*DAT_02398100 + 0x340) = *(uint *)(*DAT_02398100 + 0x340) | 8;
  }
  else {
    uVar4 = 5;
  }
  return uVar4;
}



// ---- FUN_0239810c @ 0239810c ----

undefined4 FUN_0239810c(uint param_1)

{
  undefined4 uVar1;
  
  if (param_1 < 3) {
    *(short *)(*DAT_0239813c + 0x330) = (short)param_1;
    FUN_02398d28();
    uVar1 = 0;
  }
  else {
    uVar1 = 5;
  }
  return uVar1;
}



// ---- FUN_02398140 @ 02398140 ----

undefined4 FUN_02398140(uint param_1)

{
  ushort *puVar1;
  ushort uVar2;
  int iVar3;
  
  iVar3 = *DAT_023981d4;
  if (3 < param_1) {
    return 5;
  }
  *(short *)(iVar3 + 0x334) = (short)param_1;
  puVar1 = DAT_023981d8;
  if (param_1 == 0) {
    *(ushort *)(iVar3 + 0x3c0) = *(ushort *)(iVar3 + 0x3c0) & 0xffef;
    uVar2 = *(ushort *)(iVar3 + 0x3ce) & 0xbfff;
    puVar1 = DAT_023981d8;
  }
  else {
    *(ushort *)(iVar3 + 0x3c0) = *(ushort *)(iVar3 + 0x3c0) | 0x10;
    uVar2 = *(ushort *)(iVar3 + 0x3ce) | 0x4000;
  }
  *(ushort *)(iVar3 + 0x3ce) = uVar2;
  if (*(short *)(iVar3 + 0x34c) == 0x40 && param_1 == 1) {
    *(undefined2 *)(*(int *)(*DAT_023981d4 + 0x4ac) + 0x2e) = *(undefined2 *)(iVar3 + 0x3c0);
  }
  if (param_1 == 0) {
    param_1 = 1;
  }
  *puVar1 = *puVar1 & (ushort)DAT_023981dc | (ushort)(param_1 << 3);
  return 0;
}



// ---- FUN_023981e0 @ 023981e0 ----

undefined4 FUN_023981e0(uint param_1)

{
  undefined4 uVar1;
  
  if (param_1 < 4) {
    *(short *)(*DAT_02398200 + 0x336) = (short)param_1;
    uVar1 = 0;
  }
  else {
    uVar1 = 5;
  }
  return uVar1;
}



// ---- FUN_02398204 @ 02398204 ----

undefined4 FUN_02398204(int param_1)

{
  func_0x033ad1e8(param_1,DAT_02398254,0x14);
  func_0x033ad1e8(param_1 + 0x14,DAT_02398258,0x14);
  func_0x033ad1e8(param_1 + 0x28,DAT_0239825c,0x14);
  func_0x033ad1e8(param_1 + 0x3c,DAT_02398260,0x14);
  return 0;
}



// ---- FUN_02398264 @ 02398264 ----

undefined4 FUN_02398264(uint param_1)

{
  if (param_1 < 2) {
    *(ushort *)(*DAT_02398298 + 0x33a) =
         *(ushort *)(*DAT_02398298 + 0x33a) & 0xfffe | (ushort)param_1 & 1;
    return 0;
  }
  return 5;
}



// ---- FUN_0239829c @ 0239829c ----

undefined4 FUN_0239829c(uint param_1)

{
  if (param_1 < 2) {
    *(ushort *)(*DAT_023982d0 + 0x33a) =
         *(ushort *)(*DAT_023982d0 + 0x33a) & 0xfffd | (ushort)((param_1 << 0x1f) >> 0x1e);
    return 0;
  }
  return 5;
}



// ---- FUN_023982d4 @ 023982d4 ----

undefined4 FUN_023982d4(uint param_1)

{
  int *piVar1;
  
  piVar1 = DAT_02398308;
  if (param_1 < 0x100) {
    *(undefined2 *)(*DAT_02398308 + 0x3c4) = 0;
    *(short *)(*piVar1 + 0x3c2) = (short)param_1;
    return 0;
  }
  return 5;
}



// ---- FUN_0239830c @ 0239830c ----

undefined4 FUN_0239830c(uint param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  if (param_1 < 10) {
    uVar1 = 5;
  }
  else {
    *(short *)(*DAT_023983b4 + 0x33c) = (short)param_1;
    if (param_2 != 0) {
      *DAT_023983b8 = (short)param_1;
    }
    iVar2 = *DAT_023983b4;
    if (*(short *)(iVar2 + 0x4a4) != 0) {
      iVar3 = *(int *)(iVar2 + 0x4ac) + 0x24;
      iVar4 = iVar3 + (uint)*(ushort *)(iVar2 + 0x3da);
      if (*(short *)(iVar2 + 0x352) == 1) {
        FUN_02399e80(iVar4 + 6,param_1 & 0xff,iVar3,param_4,param_4);
        FUN_02399e80(iVar4 + 7,(int)param_1 >> 8 & 0xff);
      }
      else {
        FUN_02399e80(iVar4 + 6,0xff,iVar3,param_4,param_4);
        FUN_02399e80(iVar4 + 7,0xff);
      }
    }
    uVar1 = 0;
  }
  return uVar1;
}



// ---- FUN_023983bc @ 023983bc ----

undefined4 FUN_023983bc(undefined2 *param_1)

{
  uint uVar1;
  undefined2 *puVar2;
  
  uVar1 = 0;
  puVar2 = (undefined2 *)(*DAT_023983e8 + 900);
  do {
    uVar1 = uVar1 + 1;
    *puVar2 = *param_1;
    param_1 = param_1 + 1;
    puVar2 = puVar2 + 1;
  } while (uVar1 < 0x10);
  return 0;
}



// ---- FUN_023983ec @ 023983ec ----

undefined4 FUN_023983ec(uint param_1)

{
  short sVar1;
  undefined4 uVar2;
  ushort uVar3;
  uint uVar4;
  uint uVar5;
  bool bVar6;
  
  uVar4 = *DAT_0239848c;
  if (param_1 < 2) {
    uVar5 = *(ushort *)(uVar4 + 0x33a) & 0xfffffffb | (param_1 & 1) << 2;
    *(short *)(uVar4 + 0x33a) = (short)uVar5;
    if (param_1 == 0) {
      uVar3 = *(ushort *)(uVar4 + 0x3c0) & 0xffdf;
    }
    else {
      uVar3 = *(ushort *)(uVar4 + 0x3c0) | 0x20;
    }
    *(ushort *)(uVar4 + 0x3c0) = uVar3;
    sVar1 = *(short *)(uVar4 + 0x34c);
    bVar6 = sVar1 == 0x40;
    if (bVar6) {
      uVar5 = *DAT_0239848c;
      sVar1 = *(short *)(uVar5 + 0x32e);
    }
    if (bVar6 && sVar1 == 1) {
      *(undefined2 *)(*(int *)(uVar5 + 0x4ac) + 0x2e) = *(undefined2 *)(uVar4 + 0x3c0);
    }
    if (param_1 == 0) {
      *DAT_02398490 = *DAT_02398490 & 0xfff9;
    }
    else {
      *DAT_02398490 = *DAT_02398490 | 6;
    }
    FUN_02398d28();
    uVar2 = 0;
  }
  else {
    uVar2 = 5;
  }
  return uVar2;
}



// ---- FUN_02398494 @ 02398494 ----

undefined4 FUN_02398494(uint param_1)

{
  undefined4 uVar1;
  
  if (param_1 < 2) {
    *(short *)(*DAT_023984b4 + 0x332) = (short)param_1;
    uVar1 = 0;
  }
  else {
    uVar1 = 5;
  }
  return uVar1;
}



// ---- FUN_023984b8 @ 023984b8 ----

undefined4 FUN_023984b8(uint param_1,uint param_2)

{
  undefined4 uVar1;
  
  if (param_1 < 4) {
    if (param_2 < 0x40) {
      FUN_0239974c(0x13,param_1);
      FUN_0239974c(0x35,param_2);
      uVar1 = 0;
    }
    else {
      uVar1 = 5;
    }
  }
  else {
    uVar1 = 5;
  }
  return uVar1;
}



// ---- FUN_023984fc @ 023984fc ----

undefined4 FUN_023984fc(uint param_1)

{
  int *piVar1;
  
  piVar1 = DAT_0239855c;
  if (param_1 < 2) {
    *(ushort *)(*DAT_0239855c + 0x33a) =
         *(ushort *)(*DAT_0239855c + 0x33a) & 0xfff7 | (ushort)((param_1 << 0x1f) >> 0x1c);
    *DAT_02398560 =
         (ushort)((ushort)(((uint)*(ushort *)(*piVar1 + 0x33a) << 0x1c) >> 0x10) ^
                 (ushort)(((uint)*(ushort *)(*piVar1 + 0x33a) << 0x1a) >> 0x10)) >> 0xf;
    return 0;
  }
  return 5;
}



// ---- FUN_02398564 @ 02398564 ----

undefined4 FUN_02398564(uint param_1,uint param_2)

{
  uint uVar1;
  int *piVar2;
  int iVar3;
  
  uVar1 = param_1;
  if (param_1 < 2) {
    uVar1 = param_2;
  }
  if (1 < uVar1) {
    return 5;
  }
  if (param_1 == 0) {
    *(ushort *)(*DAT_02398630 + 0x33a) =
         *(ushort *)(*DAT_02398630 + 0x33a) & 0xffdf | (ushort)((param_2 << 0x1f) >> 0x1a);
  }
  else if (param_1 == 1) {
    iVar3 = *DAT_02398630;
    if (*(short *)(iVar3 + 0x32e) != 1) {
      return 0xb;
    }
    *(ushort *)(iVar3 + 0x33a) = *(ushort *)(iVar3 + 0x33a) & 0xffdf;
  }
  piVar2 = DAT_02398630;
  *(ushort *)(*DAT_02398630 + 0x33a) =
       *(ushort *)(*DAT_02398630 + 0x33a) & 0xffef | (ushort)((param_1 << 0x1f) >> 0x1b);
  *DAT_02398634 =
       (ushort)((ushort)(((uint)*(ushort *)(*piVar2 + 0x33a) << 0x1c) >> 0x10) ^
               (ushort)(((uint)*(ushort *)(*piVar2 + 0x33a) << 0x1a) >> 0x10)) >> 0xf;
  return 0;
}



// ---- FUN_02398638 @ 02398638 ----

undefined4 FUN_02398638(uint param_1)

{
  if (param_1 < 2) {
    *(ushort *)(*DAT_02398674 + 0x33a) =
         *(ushort *)(*DAT_02398674 + 0x33a) & 0xffbf | (ushort)((param_1 << 0x1f) >> 0x19);
    return 0;
  }
  return 5;
}



// ---- FUN_02398678 @ 02398678 ----

undefined4 FUN_02398678(uint param_1)

{
  if (param_1 < 2) {
    *(ushort *)(*DAT_023986c0 + 0x33a) =
         *(ushort *)(*DAT_023986c0 + 0x33a) & 0xff7f | (ushort)(byte)((param_1 << 0x1f) >> 0x18);
    if (param_1 == 1) {
      DAT_023986c4[-1] = *DAT_023986c4;
    }
    return 0;
  }
  return 5;
}



// ---- FUN_0239883c @ 0239883c ----

undefined4 FUN_0239883c(uint param_1)

{
  int *piVar1;
  undefined2 *puVar2;
  undefined4 uVar3;
  
  puVar2 = DAT_02398890;
  piVar1 = DAT_0239888c;
  if ((param_1 < 10) || (1000 < param_1)) {
    uVar3 = 5;
  }
  else {
    *(short *)(*DAT_0239888c + 0x3b2) = (short)param_1;
    *puVar2 = (short)param_1;
    FUN_02398f8c(*(undefined2 *)(*piVar1 + 0x338));
    uVar3 = 0;
  }
  return uVar3;
}



// ---- FUN_0239890c @ 0239890c ----

void FUN_0239890c(void)

{
  undefined4 in_r3;
  ushort local_10;
  undefined1 auStack_e [6];
  undefined4 local_8;
  
  local_8 = in_r3;
  FUN_023a3f6c(0x36,6,auStack_e);
  FUN_023a3f6c(0x3c,2,&local_10);
  FUN_02397fb8(auStack_e);
  FUN_02398018(7);
  FUN_0239804c(local_10 & DAT_02398a40);
  FUN_0239808c(2);
  FUN_0239810c(0);
  FUN_02398140(0);
  FUN_023981e0(0);
  FUN_02398204(DAT_02398a44);
  FUN_0239883c(500);
  FUN_02398264(0);
  FUN_0239829c(0);
  FUN_023982d4(0x10);
  FUN_0239830c(DAT_02398a48,0);
  FUN_023983bc(DAT_02398a4c);
  FUN_023983ec(1);
  FUN_02398494(0);
  FUN_02398ce8(DAT_02398a50);
  FUN_023984b8(0,0x1f);
  FUN_02398f8c(5);
  FUN_02398564(0,0);
  FUN_023984fc(0);
  FUN_02398638(0);
  FUN_02398678(0);
  FUN_02399ec8((uint)*DAT_02398a54 + (uint)*DAT_02398a54 * 0x100,*DAT_02398a54);
  *(undefined2 *)(*DAT_02398a58 + 0x358) = 1;
  return;
}



// ---- FUN_02398ce8 @ 02398ce8 ----

undefined4 FUN_02398ce8(ushort *param_1)

{
  int iVar1;
  
  iVar1 = *DAT_02398d24;
  *(ushort *)(iVar1 + 0x3a4) = *param_1;
  *(ushort *)(iVar1 + 0x3a6) = param_1[1] | *param_1;
  FUN_02398d28();
  return 0;
}



// ---- FUN_02398d28 @ 02398d28 ----

void FUN_02398d28(void)

{
  int iVar1;
  int iVar2;
  int local_8 [2];
  
  local_8[0] = DAT_02398d9c;
  FUN_023a3f6c(0x58,2,local_8);
  local_8[0] = local_8[0] + 0x202;
  iVar2 = FUN_023996d4();
  iVar1 = local_8[0];
  if ((iVar2 == 0x14) && (iVar1 = local_8[0] + -0x6161, (*DAT_02398da0 & 2) != 0)) {
    iVar1 = local_8[0] + -0xc1c1;
  }
  local_8[0] = iVar1;
  *DAT_02398da4 = (short)local_8[0];
  return;
}



// ---- FUN_02398da8 @ 02398da8 ----

undefined4 FUN_02398da8(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  short sVar1;
  ushort *puVar2;
  int iVar3;
  
  iVar3 = *DAT_02398e08;
  *(short *)(iVar3 + 0x352) = (short)param_1;
  puVar2 = DAT_02398e0c;
  sVar1 = 0;
  if (param_1 != 0) {
    sVar1 = *(short *)(iVar3 + 0x32e);
  }
  if (param_1 != 0 && sVar1 != 1) {
    *DAT_02398e0c = *DAT_02398e0c | 0x40;
  }
  else {
    *DAT_02398e0c = *DAT_02398e0c & 0xffbf;
    FUN_0239830c(*(undefined2 *)(iVar3 + 0x33c),0,puVar2,iVar3 + 0x31c,param_4);
  }
  return 0;
}



// ---- FUN_02398e10 @ 02398e10 ----

undefined4 FUN_02398e10(uint param_1)

{
  undefined2 *puVar1;
  
  puVar1 = DAT_02398e38;
  *(short *)(*DAT_02398e34 + 0x354) = (short)(param_1 >> 1);
  *puVar1 = (short)param_1;
  return 0;
}



// ---- FUN_02398e3c @ 02398e3c ----

undefined4 FUN_02398e3c(undefined2 param_1)

{
  *DAT_02398e4c = param_1;
  return 0;
}



// ---- FUN_02398e50 @ 02398e50 ----

void FUN_02398e50(void)

{
  undefined2 *puVar1;
  
  if (*(short *)(*DAT_02398eb8 + 0x5f8) == 2) {
    FUN_0239977c(DAT_02398ebc);
  }
  *DAT_02398ec4 = (short)DAT_02398ec0;
  func_0x033aa728();
  FUN_0239974c(0x1e,*DAT_02398ec8 | 0x3f);
  puVar1 = DAT_02398ed4;
  *DAT_02398ed0 = (short)DAT_02398ecc;
  *puVar1 = 1;
  return;
}



// ---- FUN_02398f8c @ 02398f8c ----

undefined4 FUN_02398f8c(int param_1)

{
  undefined2 uVar1;
  uint uVar2;
  int iVar3;
  
  iVar3 = *DAT_02398fe8;
  uVar1 = (undefined2)DAT_02398fec;
  if (param_1 == DAT_02398fec) {
    *(undefined2 *)(iVar3 + 0x338) = uVar1;
    *(undefined2 *)(iVar3 + 0x3d0) = uVar1;
  }
  else {
    uVar2 = func_0x033b5c2c(param_1 * (uint)*(ushort *)(iVar3 + 0x3b2),100);
    if (0x10000 < uVar2) {
      return 5;
    }
    *(short *)(iVar3 + 0x338) = (short)param_1;
    *(short *)(iVar3 + 0x3d0) = (short)uVar2;
  }
  return 0;
}



// ---- FUN_02398ff0 @ 02398ff0 ----

void FUN_02398ff0(void)

{
  int *piVar1;
  ushort *puVar2;
  
  piVar1 = DAT_02399034;
  *(undefined2 *)(*DAT_02399034 + 0x3ea) = 1;
  puVar2 = DAT_02399038;
  if (*(short *)(*piVar1 + 0x468) != 0) {
    return;
  }
  *DAT_02399038 = *DAT_02399038 & 0xfffd;
  puVar2[8] = 0;
  return;
}



// ---- FUN_0239923c @ 0239923c ----

void FUN_0239923c(undefined2 *param_1,undefined2 *param_2)

{
  *param_1 = *param_2;
  param_1[1] = param_2[1];
  param_1[2] = param_2[2];
  return;
}



// ---- FUN_023992d8 @ 023992d8 ----

void FUN_023992d8(void)

{
  FUN_02399308();
  func_0x033ad204(0,*DAT_02399304 + 0x53c,0xb4);
  return;
}



// ---- FUN_02399308 @ 02399308 ----

void FUN_02399308(void)

{
  ushort uVar1;
  ushort *puVar2;
  int iVar3;
  
  puVar2 = DAT_023994fc;
  iVar3 = *DAT_023994f8;
  *(uint *)(iVar3 + 0x58c) = *(int *)(iVar3 + 0x58c) + (*DAT_023994fc & 0xff);
  uVar1 = puVar2[1];
  *(int *)(iVar3 + 0x588) = *(int *)(iVar3 + 0x588) + ((int)(uint)uVar1 >> 8);
  *(uint *)(iVar3 + 0x598) = *(int *)(iVar3 + 0x598) + (uVar1 & 0xff);
  uVar1 = puVar2[2];
  *(int *)(iVar3 + 0x594) = *(int *)(iVar3 + 0x594) + ((int)(uint)uVar1 >> 8);
  *(uint *)(iVar3 + 0x590) = *(int *)(iVar3 + 0x590) + (uVar1 & 0xff);
  uVar1 = puVar2[3];
  *(int *)(iVar3 + 0x59c) = *(int *)(iVar3 + 0x59c) + ((int)(uint)uVar1 >> 8);
  *(uint *)(iVar3 + 0x574) = *(int *)(iVar3 + 0x574) + (uVar1 & 0xff);
  *(uint *)(iVar3 + 0x584) = *(int *)(iVar3 + 0x584) + (puVar2[4] & 0xff);
  *(uint *)(iVar3 + 0x55c) = *(int *)(iVar3 + 0x55c) + (puVar2[5] & 0xff);
  uVar1 = puVar2[6];
  *(int *)(iVar3 + 0x56c) = *(int *)(iVar3 + 0x56c) + ((int)(uint)uVar1 >> 8);
  *(uint *)(iVar3 + 0x580) = *(int *)(iVar3 + 0x580) + (uVar1 & 0xff);
  uVar1 = puVar2[7];
  *(uint *)(iVar3 + 0x578) = *(int *)(iVar3 + 0x578) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x57c) = *(int *)(iVar3 + 0x57c) + ((int)(uint)uVar1 >> 8);
  *(uint *)(iVar3 + 0x548) = *(int *)(iVar3 + 0x548) + (puVar2[8] & 0xff);
  *(int *)(iVar3 + 0x5b4) = *(int *)(iVar3 + 0x5b4) + ((int)(uint)puVar2[0x10] >> 8);
  uVar1 = puVar2[0x11];
  *(uint *)(iVar3 + 0x5b8) = *(int *)(iVar3 + 0x5b8) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x5bc) = *(int *)(iVar3 + 0x5bc) + ((int)(uint)uVar1 >> 8);
  uVar1 = puVar2[0x12];
  *(uint *)(iVar3 + 0x5c0) = *(int *)(iVar3 + 0x5c0) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x5c4) = *(int *)(iVar3 + 0x5c4) + ((int)(uint)uVar1 >> 8);
  uVar1 = puVar2[0x13];
  *(uint *)(iVar3 + 0x5c8) = *(int *)(iVar3 + 0x5c8) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x5cc) = *(int *)(iVar3 + 0x5cc) + ((int)(uint)uVar1 >> 8);
  uVar1 = puVar2[0x14];
  *(uint *)(iVar3 + 0x5d0) = *(int *)(iVar3 + 0x5d0) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x5d4) = *(int *)(iVar3 + 0x5d4) + ((int)(uint)uVar1 >> 8);
  uVar1 = puVar2[0x15];
  *(uint *)(iVar3 + 0x5d8) = *(int *)(iVar3 + 0x5d8) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x5dc) = *(int *)(iVar3 + 0x5dc) + ((int)(uint)uVar1 >> 8);
  uVar1 = puVar2[0x16];
  *(uint *)(iVar3 + 0x5e0) = *(int *)(iVar3 + 0x5e0) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x5e4) = *(int *)(iVar3 + 0x5e4) + ((int)(uint)uVar1 >> 8);
  uVar1 = puVar2[0x17];
  *(uint *)(iVar3 + 0x5e8) = *(int *)(iVar3 + 0x5e8) + (uVar1 & 0xff);
  *(int *)(iVar3 + 0x5ec) = *(int *)(iVar3 + 0x5ec) + ((int)(uint)uVar1 >> 8);
  return;
}



// ---- FUN_023995d0 @ 023995d0 ----

bool FUN_023995d0(short *param_1,short *param_2)

{
  short sVar1;
  short sVar2;
  bool bVar3;
  bool bVar4;
  
  sVar1 = param_1[2];
  sVar2 = param_2[2];
  bVar3 = sVar1 == sVar2;
  if (bVar3) {
    sVar1 = param_1[1];
    sVar2 = param_2[1];
  }
  bVar4 = bVar3 && sVar1 == sVar2;
  if (bVar3 && sVar1 == sVar2) {
    bVar4 = *param_1 == *param_2;
  }
  return bVar4;
}



// ---- FUN_023996d4 @ 023996d4 ----

undefined4 FUN_023996d4(void)

{
  short sVar1;
  
  sVar1 = *(short *)(*DAT_0239971c + 0x330);
  if (sVar1 == 0) {
    if ((*(ushort *)(*DAT_0239971c + 0x3a4) & 1) != 0) {
      return 10;
    }
  }
  else if (sVar1 == 1) {
    return 10;
  }
  return 0x14;
}



// ---- FUN_0239974c @ 0239974c ----

undefined4 FUN_0239974c(ushort param_1,undefined2 param_2)

{
  undefined2 *puVar1;
  int iVar2;
  undefined4 uVar3;
  
  puVar1 = DAT_02399778;
  *DAT_02399778 = param_2;
  puVar1[-1] = param_1 | 0x5000;
  iVar2 = func_0x033aa728();
  if (iVar2 == 0) {
    uVar3 = 0;
  }
  else {
    uVar3 = 0xffffffff;
  }
  return uVar3;
}



// ---- FUN_0239977c @ 0239977c ----

void FUN_0239977c(undefined4 param_1)

{
  undefined2 *puVar1;
  code *UNRECOVERED_JUMPTABLE;
  
  UNRECOVERED_JUMPTABLE = DAT_02399798;
  puVar1 = DAT_02399794;
  *DAT_02399794 = (short)param_1;
  puVar1[-1] = (short)((uint)param_1 >> 0x10);
                    /* WARNING: Could not recover jumptable at 0x02399790. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)();
  return;
}



// ---- FUN_0239980c @ 0239980c ----

void FUN_0239980c(void)

{
  int iVar1;
  
  iVar1 = *DAT_02399878;
  func_0x033ad1d0(0,iVar1 + 0x5f8,0x10);
  FUN_023a3f6c(0x40,1,iVar1 + 0x5f8);
  FUN_023a3f6c(0x41,1,iVar1 + 0x5fa);
  FUN_023a3f6c(0x42,1,iVar1 + 0x5fc);
  FUN_023a3f6c(0x43,1,iVar1 + 0x5fe);
  return;
}



// ---- FUN_0239987c @ 0239987c ----

void FUN_0239987c(void)

{
  int iVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  
  iVar3 = DAT_023998b0;
  uVar4 = 0;
  do {
    iVar1 = uVar4 * 4;
    iVar2 = uVar4 * 4;
    uVar4 = uVar4 + 1;
    *(undefined2 *)(*(ushort *)(iVar3 + iVar1) + 0x4808000) = *(undefined2 *)(iVar3 + iVar2 + 2);
  } while (uVar4 < 0x19);
  return;
}



// ---- FUN_02399d3c @ 02399d3c ----

void FUN_02399d3c(void)

{
                    /* WARNING: Could not recover jumptable at 0x02399d50. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02399d58)(*DAT_02399d54 + 0x634);
  return;
}



// ---- FUN_02399dd8 @ 02399dd8 ----

void FUN_02399dd8(undefined4 param_1,undefined4 param_2,int param_3)

{
                    /* WARNING: Could not recover jumptable at 0x02399df0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_02399df4)(param_2,param_1,param_3 + 1U & 0xfffffffe);
  return;
}



// ---- FUN_02399df8 @ 02399df8 ----

void FUN_02399df8(int param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  func_0x033ad1e8(param_2,param_1,0x24);
  if (param_4 != 0) {
    func_0x033ad1e8(param_3,param_1 + 0x24,param_4 + 1U & 0xfffffffe);
  }
  return;
}



// ---- FUN_02399e3c @ 02399e3c ----

void FUN_02399e3c(int param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  func_0x033ad1e8(param_2,param_1,0x24);
  if (param_4 != 0) {
    func_0x033ad1e8(param_3,param_1 + 0x28,param_4 + 1U & 0xfffffffe);
  }
  return;
}



// ---- FUN_02399e80 @ 02399e80 ----

void FUN_02399e80(ushort *param_1,ushort param_2)

{
  if (((uint)param_1 & 1) == 0) {
    *param_1 = *param_1 & 0xff00 | param_2 & 0xff;
  }
  else {
    *(ushort *)((int)param_1 + -1) = *(ushort *)((int)param_1 + -1) & 0xff | param_2 << 8;
  }
  return;
}



// ---- FUN_02399eac @ 02399eac ----

uint FUN_02399eac(ushort *param_1)

{
  uint uVar1;
  
  if (((uint)param_1 & 1) == 0) {
    uVar1 = (uint)*param_1;
  }
  else {
    uVar1 = (int)(uint)*(ushort *)((int)param_1 + -1) >> 8;
  }
  return uVar1 & 0xff;
}



// ---- FUN_02399ec8 @ 02399ec8 ----

void FUN_02399ec8(ushort param_1,ushort param_2)

{
  int iVar1;
  
  iVar1 = *DAT_02399ef4;
  *(ushort *)(iVar1 + 0x5f0) = (param_1 & (ushort)DAT_02399ef8) + 5;
  *(ushort *)(iVar1 + 0x5f2) = param_2 | 1;
  return;
}



// ---- FUN_0239aa5c @ 0239aa5c ----

uint FUN_0239aa5c(ushort *param_1)

{
  short *psVar1;
  int *piVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  
  piVar2 = DAT_0239ab00;
  if ((*param_1 & 1) == 0) {
    iVar4 = *DAT_0239ab00;
    if (1 < *(ushort *)(iVar4 + 0x52c)) {
      uVar5 = 0;
      psVar1 = *(short **)(iVar4 + 0x31c);
      for (uVar3 = 1; uVar3 < *(ushort *)(iVar4 + 0x322); uVar3 = uVar3 + 1) {
        if (psVar1[0xe] != 0) {
          iVar4 = FUN_023995d0(psVar1 + 0x10,param_1);
          if (iVar4 != 0) {
            return uVar3;
          }
          iVar4 = *piVar2;
          uVar5 = uVar5 + 1;
          if (*(ushort *)(iVar4 + 0x52c) <= uVar5) break;
        }
        psVar1 = psVar1 + 0xe;
      }
    }
    uVar3 = 0xff;
  }
  else {
    uVar3 = 0;
  }
  return uVar3;
}



// ---- FUN_0239aca0 @ 0239aca0 ----

void FUN_0239aca0(int param_1)

{
  short sVar1;
  undefined4 uVar2;
  uint uVar3;
  int iVar4;
  bool bVar5;
  
  uVar3 = (uint)*(ushort *)(param_1 + 2);
  iVar4 = uVar3 * 0x1c + *(int *)(*DAT_0239ad2c + 0x31c);
  uVar2 = func_0x033aabf8(0x1000000);
  sVar1 = *(short *)(*DAT_0239ad2c + 0x350);
  bVar5 = sVar1 == 1;
  if (bVar5) {
    sVar1 = *(short *)(iVar4 + 0x16);
  }
  if (bVar5 && sVar1 == 0) {
    FUN_0239b268(uVar3);
  }
  *(short *)(iVar4 + 0x16) = *(short *)(iVar4 + 0x16) + 1;
  func_0x033aabc0(uVar2);
  if (((uint)*(ushort *)(*DAT_0239ad2c + 0x534) & 1 << (uVar3 & 0xff)) == 0) {
    *(undefined2 *)(iVar4 + 0x18) = *(undefined2 *)(iVar4 + 0x1a);
  }
  return;
}



// ---- FUN_0239ad30 @ 0239ad30 ----

void FUN_0239ad30(int param_1)

{
  ushort uVar1;
  short sVar2;
  undefined4 uVar3;
  int iVar4;
  bool bVar5;
  
  uVar1 = *(ushort *)(param_1 + 2);
  iVar4 = (uint)uVar1 * 0x1c + *(int *)(*DAT_0239ad9c + 0x31c);
  uVar3 = func_0x033aabf8(0x1000000);
  sVar2 = *(short *)(*DAT_0239ad9c + 0x350);
  bVar5 = sVar2 == 1;
  if (bVar5) {
    sVar2 = *(short *)(iVar4 + 0x16);
  }
  if (bVar5 && sVar2 == 1) {
    FUN_0239b324((uint)uVar1);
  }
  *(short *)(iVar4 + 0x16) = *(short *)(iVar4 + 0x16) + -1;
  func_0x033aabc0(uVar3);
  return;
}



// ---- FUN_0239ada0 @ 0239ada0 ----

void FUN_0239ada0(uint param_1,uint param_2)

{
  int *piVar1;
  undefined4 uVar2;
  int iVar3;
  
  uVar2 = func_0x033aabf8(0x1000000);
  piVar1 = DAT_0239ae84;
  if (param_2 < 0x40) {
    *(ushort *)(*DAT_0239ae84 + 0x530) =
         *(ushort *)(*DAT_0239ae84 + 0x530) | (ushort)(1 << (param_1 & 0xff));
    *(ushort *)(*piVar1 + 0x532) = *(ushort *)(*piVar1 + 0x532) | (ushort)(1 << (param_1 & 0xff));
    if ((*(short *)(*piVar1 + 0x350) == 1) && (iVar3 = FUN_0239b228(param_1), iVar3 != 0)) {
      FUN_0239b0bc(param_1);
    }
  }
  else {
    *(ushort *)(*DAT_0239ae84 + 0x532) =
         *(ushort *)(*DAT_0239ae84 + 0x532) & ~(ushort)(1 << (param_1 & 0xff));
    if (((int)(uint)*(ushort *)(*piVar1 + 0x52e) >> (param_1 & 0xff) & 1U) != 0) {
      FUN_0239af04(param_1);
    }
  }
  *(short *)(*(int *)(*DAT_0239ae84 + 0x31c) + param_1 * 0x1c) = (short)param_2;
  func_0x033aabc0(uVar2);
  return;
}



// ---- FUN_0239aea8 @ 0239aea8 ----

void FUN_0239aea8(uint param_1,int param_2)

{
  int iVar1;
  
  iVar1 = *DAT_0239aef8;
  *(ushort *)(iVar1 + 0x52e) =
       *(ushort *)(iVar1 + 0x52e) & ~(ushort)(1 << (param_1 & 0xff)) |
       (ushort)(param_2 << (param_1 & 0xff));
  if ((*(ushort *)(iVar1 + 0x52e) & ~*(ushort *)(iVar1 + 0x532)) == 0) {
    *DAT_0239af00 = 8;
  }
  else {
    *DAT_0239aefc = 8;
  }
  return;
}



// ---- FUN_0239af04 @ 0239af04 ----

void FUN_0239af04(uint param_1)

{
  int iVar1;
  
  iVar1 = FUN_0239b13c();
  if (iVar1 == 0x40) {
    *(ushort *)(*DAT_0239af40 + 0x530) =
         *(ushort *)(*DAT_0239af40 + 0x530) & ~(ushort)(1 << (param_1 & 0xff));
  }
  return;
}



// ---- FUN_0239b0bc @ 0239b0bc ----

void FUN_0239b0bc(int param_1)

{
  uint uVar1;
  int iVar2;
  
  iVar2 = *DAT_0239b138;
  FUN_0239b324();
  uVar1 = FUN_0239b228(param_1);
  if (uVar1 != 0) {
    *(undefined2 *)(param_1 * 0x1c + *(int *)(*DAT_0239b138 + 0x31c) + 2) = 0;
    *(ushort *)(iVar2 + 0x53a) = *(ushort *)(iVar2 + 0x53a) & ~(ushort)(1 << (uVar1 & 0xff));
    *(short *)(iVar2 + 0x538) = *(short *)(iVar2 + 0x538) + -1;
    if (*(short *)(iVar2 + 0x538) == 0) {
      FUN_02398ff0();
    }
  }
  return;
}



// ---- FUN_0239b13c @ 0239b13c ----

undefined2 FUN_0239b13c(int param_1)

{
  return *(undefined2 *)(*(int *)(*DAT_0239b158 + 0x31c) + param_1 * 0x1c);
}



// ---- FUN_0239b15c @ 0239b15c ----

uint FUN_0239b15c(uint param_1)

{
  return (int)(uint)*(ushort *)(*DAT_0239b178 + 0x530) >> (param_1 & 0xff) & 1;
}



// ---- FUN_0239b228 @ 0239b228 ----

undefined2 FUN_0239b228(int param_1)

{
  return *(undefined2 *)(param_1 * 0x1c + *(int *)(*DAT_0239b244 + 0x31c) + 2);
}



// ---- FUN_0239b248 @ 0239b248 ----

undefined2 FUN_0239b248(int param_1)

{
  return *(undefined2 *)(param_1 * 0x1c + *(int *)(*DAT_0239b264 + 0x31c) + 0x16);
}



// ---- FUN_0239b268 @ 0239b268 ----

void FUN_0239b268(uint param_1)

{
  byte bVar1;
  int iVar2;
  undefined4 uVar3;
  uint uVar4;
  uint uVar5;
  
  iVar2 = FUN_0239b13c();
  if ((iVar2 == 0x40) && (((uint)*(ushort *)(*DAT_0239b31c + 0x534) & 1 << (param_1 & 0xff)) == 0))
  {
    iVar2 = (uint)*(ushort *)(*DAT_0239b31c + 0x3d8) + DAT_0239b320;
    uVar3 = func_0x033aabf8(0x1000000);
    if (param_1 == 0) {
      bVar1 = FUN_02399eac(iVar2 + 4);
      FUN_02399e80(iVar2 + 4,bVar1 | 1);
    }
    else {
      uVar4 = FUN_0239b228(param_1);
      iVar2 = iVar2 + 5 + (uVar4 >> 3);
      uVar5 = FUN_02399eac(iVar2);
      FUN_02399e80(iVar2,(uVar5 | 1 << (uVar4 & 7)) & 0xff);
    }
    func_0x033aabc0(uVar3);
  }
  return;
}



// ---- FUN_0239b324 @ 0239b324 ----

void FUN_0239b324(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  uint uVar3;
  uint uVar4;
  
  iVar1 = FUN_0239b13c();
  if (iVar1 == 0x40) {
    iVar1 = (uint)*(ushort *)(*DAT_0239b3c8 + 0x3d8) + DAT_0239b3cc;
    uVar2 = func_0x033aabf8(0x1000000);
    if (param_1 == 0) {
      uVar3 = FUN_02399eac(iVar1 + 4);
      FUN_02399e80(iVar1 + 4,uVar3 & 0xfe);
    }
    else {
      uVar3 = FUN_0239b228(param_1);
      iVar1 = iVar1 + 5 + (uVar3 >> 3);
      uVar4 = FUN_02399eac(iVar1);
      FUN_02399e80(iVar1,~(1 << (uVar3 & 7)) & uVar4 & 0xff);
    }
    func_0x033aabc0(uVar2);
  }
  return;
}



// ---- FUN_0239b5d0 @ 0239b5d0 ----

void FUN_0239b5d0(void)

{
  ushort uVar1;
  undefined2 uVar2;
  undefined4 in_r3;
  int iVar3;
  uint uVar4;
  int iVar5;
  
  iVar3 = *DAT_0239b660;
  uVar1 = *(ushort *)(iVar3 + 0x322);
  iVar5 = *(int *)(iVar3 + 0x31c);
  func_0x033ad1d0(0,iVar5,(uint)uVar1 * 0x1c,iVar3,in_r3);
  func_0x033ad1d0(0,*DAT_0239b660 + 0x52c,0x10);
  uVar2 = (undefined2)DAT_0239b664;
  *(undefined2 *)(iVar5 + 0x1a) = uVar2;
  for (uVar4 = 1; uVar4 < uVar1; uVar4 = uVar4 + 1) {
    *(undefined2 *)(uVar4 * 0x1c + iVar5 + 0x1a) = uVar2;
  }
  FUN_0239b6f4(0,DAT_0239b668);
  FUN_0239ada0(0,0x40);
  return;
}



// ---- FUN_0239b6f4 @ 0239b6f4 ----

void FUN_0239b6f4(uint param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  iVar3 = *DAT_0239b7d0;
  iVar2 = *(int *)(iVar3 + 0x31c);
  iVar4 = iVar2 + param_1 * 0x1c;
  if (*(short *)(iVar2 + param_1 * 0x1c) == 0) {
    *(short *)(iVar3 + 0x52c) = *(short *)(iVar3 + 0x52c) + 1;
  }
  func_0x033ad1d0(0,iVar4,0x1a,iVar2,param_4);
  *(ushort *)(*DAT_0239b7d0 + 0x534) =
       *(ushort *)(*DAT_0239b7d0 + 0x534) & ~(ushort)(1 << (param_1 & 0xff));
  FUN_0239aea8(param_1 & 0xffff,0);
  *(ushort *)(*DAT_0239b7d0 + 0x530) =
       *(ushort *)(*DAT_0239b7d0 + 0x530) | (ushort)(1 << (param_1 & 0xff));
  FUN_0239923c(iVar4 + 4,param_2);
  piVar1 = DAT_0239b7d0;
  *(short *)(iVar4 + 0x14) = (short)DAT_0239b7d4;
  *(undefined2 *)(iVar4 + 0x10) = *(undefined2 *)(*piVar1 + 0x3a6);
  *(undefined2 *)(iVar4 + 0x18) = *(undefined2 *)(iVar4 + 0x1a);
  FUN_0239ada0(param_1 & 0xffff,0x20);
  return;
}



// ---- FUN_0239b7e0 @ 0239b7e0 ----

void FUN_0239b7e0(void)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  
  piVar1 = DAT_0239b83c;
  iVar2 = *DAT_0239b83c;
  iVar3 = *(int *)(iVar2 + 500);
  while ((iVar3 != -1 &&
         (iVar2 = func_0x033ab91c(*(undefined4 *)(iVar2 + 0x304),iVar3,0), iVar2 != 0))) {
    func_0x033a7ab4(*piVar1 + 500,iVar3);
    iVar2 = *piVar1;
    iVar3 = *(int *)(iVar2 + 500);
  }
  return;
}



// ---- FUN_0239b840 @ 0239b840 ----

void FUN_0239b840(void)

{
  *(undefined2 *)(*DAT_0239b858 + 0x428) = 0;
  return;
}



// ---- FUN_0239b89c @ 0239b89c ----

undefined4 FUN_0239b89c(int param_1,int param_2)

{
  undefined4 uVar1;
  
  *(undefined2 *)(param_2 + 2) = 9;
  if (*(ushort *)(param_1 + 0x10) < 2) {
    if (*(ushort *)(param_1 + 0x12) < 2) {
      if (*(ushort *)(param_1 + 0x14) < 2) {
        FUN_02398da8(*(ushort *)(param_1 + 0x10));
        if (*(short *)(param_1 + 0x10) == 1) {
          if (*(short *)(param_1 + 0x12) == 1) {
            FUN_02398e3c(DAT_0239b940);
          }
          else {
            FUN_02398e3c(0);
          }
          *(undefined2 *)(*DAT_0239b944 + 0x358) = *(undefined2 *)(param_1 + 0x14);
        }
        else {
          FUN_02398e3c(0x8000);
          FUN_02398e10(2);
        }
        uVar1 = 0;
      }
      else {
        uVar1 = 5;
      }
    }
    else {
      uVar1 = 5;
    }
  }
  else {
    uVar1 = 5;
  }
  return uVar1;
}



// ---- FUN_0239d20c @ 0239d20c ----

void FUN_0239d20c(void)

{
                    /* WARNING: Could not recover jumptable at 0x0239d228. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*DAT_0239d230)(0,*DAT_0239d22c + 0x404,0x20);
  return;
}



// ---- FUN_0239d588 @ 0239d588 ----

undefined4 FUN_0239d588(int param_1,int param_2)

{
  int *piVar1;
  int *piVar2;
  undefined4 uVar3;
  int iVar4;
  uint uVar5;
  int iVar6;
  
  piVar1 = DAT_0239d688;
  iVar4 = *(int *)(*DAT_0239d688 + 0x31c);
  *(undefined2 *)(param_2 + 2) = 1;
  piVar2 = DAT_0239d688;
  uVar5 = (uint)*(ushort *)(param_1 + 0x10);
  if ((uVar5 < *(ushort *)(*piVar1 + 0x322)) || (uVar5 == 0xffff)) {
    if ((*(ushort *)(param_1 + 0x14) < 0x40) || (*(ushort *)(param_1 + 0x14) == DAT_0239d68c)) {
      if (uVar5 == DAT_0239d68c) {
        uVar5 = 1;
        while (uVar5 < *(ushort *)(*piVar2 + 0x322)) {
          iVar6 = uVar5 * 0x1c + iVar4;
          uVar5 = uVar5 + 1;
          *(undefined2 *)(iVar6 + 0x1a) = *(undefined2 *)(param_1 + 0x12);
          if (*(short *)(iVar6 + 0x18) != 0) {
            *(undefined2 *)(iVar6 + 0x18) = *(undefined2 *)(param_1 + 0x12);
          }
        }
      }
      else if (uVar5 != 0) {
        *(undefined2 *)(uVar5 * 0x1c + iVar4 + 0x1a) = *(undefined2 *)(param_1 + 0x12);
        iVar6 = (uint)*(ushort *)(param_1 + 0x10) * 0x1c;
        if (*(short *)(iVar4 + 0x18 + iVar6) != 0) {
          *(undefined2 *)(iVar4 + 0x18 + iVar6) = *(undefined2 *)(param_1 + 0x12);
        }
      }
      if (*(short *)(param_1 + 0x14) != 0) {
        FUN_02398f8c();
      }
      uVar3 = 0;
    }
    else {
      uVar3 = 5;
    }
  }
  else {
    uVar3 = 5;
  }
  return uVar3;
}



// ---- FUN_0239f018 @ 0239f018 ----

void FUN_0239f018(undefined4 param_1,int param_2)

{
  int iVar1;
  
  iVar1 = param_2 + (uint)*(ushort *)(param_2 + 0xe) * 2;
  *(undefined2 *)(param_2 + 0xc) = *(undefined2 *)(iVar1 + 0x10);
  *(undefined2 *)(iVar1 + 0x12) = 2;
  *(undefined2 *)(iVar1 + 0x14) = 0;
  *(undefined2 *)(iVar1 + 0x16) = *(undefined2 *)(param_2 + 0x18);
  func_0x033a8060();
  return;
}



// ---- FUN_0239f050 @ 0239f050 ----

void FUN_0239f050(int param_1)

{
  undefined2 uVar1;
  ushort uVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  ushort *puVar8;
  uint uVar9;
  short *psVar10;
  int iVar11;
  int iVar12;
  int *piVar13;
  
  iVar7 = *DAT_0239f264;
  piVar13 = (int *)(param_1 * 0xc + iVar7 + 0x194);
  psVar10 = (short *)(param_1 * 0x14 + iVar7 + 0x42c);
  if ((short)piVar13[2] != 0) {
    uVar3 = func_0x033aabf8(0x1000000);
    if (*psVar10 == 0) {
      iVar4 = *piVar13;
      while (iVar11 = iVar4, iVar11 != -1) {
        iVar4 = func_0x033a7d88(iVar11);
        iVar12 = iVar11 + 0x10;
        uVar1 = *(undefined2 *)(iVar11 + 0x12);
        iVar5 = FUN_0239f3d8(iVar12);
        if (iVar5 == 0) {
          if ((param_1 != 0) && ((param_1 != 1 || (iVar5 = FUN_0239b13c(uVar1), iVar5 != 0x40))))
          goto LAB_0239f198;
          iVar5 = FUN_0239b15c(uVar1);
          if (iVar5 != 0) {
            iVar5 = FUN_0239b13c(uVar1);
            if (iVar5 == 0x40) {
LAB_0239f198:
              *psVar10 = 1;
              psVar10[1] = psVar10[1] + 1;
              *(int *)(psVar10 + 6) = iVar12;
              uVar9 = *(uint *)(psVar10 + 4);
              if (*(short *)(iVar7 + 0x354) == 0) {
                FUN_02398e10(2);
              }
              FUN_0239f270(uVar9,iVar11);
              if ((*(short *)(iVar7 + 0x350) == 1) && (uVar6 = FUN_0239b248(uVar1), 1 < uVar6)) {
                *(ushort *)(uVar9 + 0xc) = *(ushort *)(uVar9 + 0xc) | 0x2000;
              }
              puVar8 = (ushort *)(DAT_0239f26c + param_1 * 4);
              uVar2 = (ushort)((uVar9 & DAT_0239f268) >> 1);
              if ((*(ushort *)(iVar11 + 0x24) & 0xc) == 4) {
                *puVar8 = uVar2 | 0xa000;
              }
              else if ((*(ushort *)(iVar11 + 0x24) & 0xfc) == 0x50) {
                *puVar8 = uVar2 | 0x9000;
              }
              else {
                *puVar8 = uVar2 | 0x8000;
              }
              func_0x033aabc0(uVar3);
              return;
            }
            *(undefined2 *)(iVar11 + 0x18) = 2;
            FUN_0239f018(piVar13,iVar11);
            FUN_0239ad30(iVar12);
          }
        }
        else {
          *(short *)(iVar7 + 0x4da) = *(short *)(iVar7 + 0x4da) + 1;
          *(undefined2 *)(iVar11 + 0x18) = 2;
          psVar10[2] = psVar10[2] + 1;
          (**(code **)(psVar10 + 8))(iVar12,0);
        }
      }
      func_0x033aabc0(uVar3);
    }
    else {
      func_0x033aabc0();
    }
  }
  return;
}



// ---- FUN_0239f270 @ 0239f270 ----

void FUN_0239f270(int param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  int *piVar1;
  ushort *puVar2;
  undefined4 uVar3;
  undefined2 *puVar4;
  
  if ((*(ushort *)(param_2 + 0x24) & 0x4000) == 0) {
    if (*(ushort *)(param_2 + 0xc) == DAT_0239f3c8) {
      FUN_02399dd8(param_1,param_2 + 0x18,*(ushort *)(param_2 + 0x16) + 0x24);
    }
    else {
      FUN_02399df8(param_1,param_2 + 0x18,*(undefined4 *)(param_2 + 0x3c),
                   *(undefined2 *)(param_2 + 0x16),param_4);
    }
  }
  else {
    if (*(short *)(*DAT_0239f3c4 + 0x350) == 3) {
      FUN_02399308();
    }
    if (*(ushort *)(param_2 + 0xc) == DAT_0239f3c8) {
      FUN_02399e3c(param_1,param_2 + 0x18,param_2 + 0x3c,*(undefined2 *)(param_2 + 0x16));
    }
    else {
      FUN_02399e3c(param_1,param_2 + 0x18,*(undefined4 *)(param_2 + 0x3c),
                   *(undefined2 *)(param_2 + 0x16));
    }
    puVar2 = DAT_0239f3cc;
    piVar1 = DAT_0239f3c4;
    *(ushort *)(param_1 + 0x24) = *DAT_0239f3cc + *DAT_0239f3cc * 0x100;
    *(ushort *)(param_1 + 0x26) = *puVar2 & 0xff | *(short *)(*piVar1 + 0x336) << 0xe;
    if ((*(ushort *)(*piVar1 + 0x690) & 8) != 0) {
      puVar4 = (undefined2 *)(param_1 + (uint)*(ushort *)(param_2 + 0x22) + 5 & 0xfffffffe);
      *puVar4 = 0;
      puVar4[1] = 0;
    }
  }
  uVar3 = DAT_0239f3d4;
  if ((*(ushort *)(*DAT_0239f3c4 + 0x690) & 4) != 0) {
    puVar4 = (undefined2 *)(param_1 + (uint)*(ushort *)(param_2 + 0x22) + 0xb & 0xfffffffc);
    *puVar4 = (short)DAT_0239f3d0;
    puVar4[1] = (short)uVar3;
  }
  return;
}



// ---- FUN_0239f3d8 @ 0239f3d8 ----

bool FUN_0239f3d8(int param_1)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  uint uVar4;
  
  iVar3 = *DAT_0239f454;
  uVar2 = *(ushort *)(iVar3 + 0x3d0) & 0x1fff;
  uVar4 = uVar2 << 3;
  if ((*(ushort *)(param_1 + 0x14) & 0xf) >> 2 == 0) {
    if ((*(short *)(iVar3 + 0x350) == 1) &&
       (uVar1 = (*(ushort *)(param_1 + 0x14) & 0xff) >> 4,
       (uVar1 == 1 || uVar1 == 3) || uVar1 == 0xb)) {
      uVar4 = uVar2;
    }
  }
  else {
    uVar4 = *(ushort *)(iVar3 + 0x3d0) & 0x1fff;
  }
  return uVar4 < (*(int *)(iVar3 + 0x3ec) - (uint)*(ushort *)(param_1 + 4) & 0xffff);
}



// ---- FUN_023a01f0 @ 023a01f0 ----

void FUN_023a01f0(int param_1)

{
  undefined2 uVar1;
  
  uVar1 = FUN_0239aa5c(param_1 + 0x18);
  *(undefined2 *)(param_1 + 2) = uVar1;
  if (*(short *)(param_1 + 2) == 0xff) {
    *(undefined2 *)(param_1 + 2) = 0;
  }
  *(short *)(param_1 + 4) = (short)*(undefined4 *)(*DAT_023a0260 + 0x3ec);
  if ((*(ushort *)(param_1 + 0x14) & 0x4000) != 0) {
    *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) + 8;
  }
  FUN_0239aca0(param_1);
  func_0x033a7c90(*DAT_023a0260 + 0x188,*DAT_023a0260 + 0x1a0,param_1 + -0x10);
  return;
}



// ---- FUN_023a3f6c @ 023a3f6c ----

void FUN_023a3f6c(int param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  int iVar2;
  
  if (*(int *)(*DAT_023a3fc8 + 0x318) != 0) {
    iVar2 = *(int *)(*DAT_023a3fc8 + 0x318) + param_1 + -0x2a;
    for (; param_2 != 0; param_2 = param_2 + -1) {
      uVar1 = FUN_02399eac(iVar2);
      iVar2 = iVar2 + 1;
      FUN_02399e80(param_3,uVar1);
      param_3 = param_3 + 1;
    }
  }
  return;
}



// ---- FUN_023a45ac @ 023a45ac ----

bool FUN_023a45ac(void)

{
  uint in_r3;
  uint local_8 [2];
  
  local_8[0] = in_r3;
  FUN_023a46a4(local_8);
  return (local_8[0] & 1) == 0;
}



// ---- FUN_023a45d0 @ 023a45d0 ----

undefined4 FUN_023a45d0(void)

{
  undefined4 uVar1;
  uint in_r3;
  uint local_8 [2];
  
  local_8[0] = in_r3;
  FUN_023a46a4(local_8);
  if ((local_8[0] & 1) == 0) {
    if ((local_8[0] & 2) == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = 1;
    }
  }
  else {
    uVar1 = 0;
  }
  return uVar1;
}



// ---- FUN_023a46a4 @ 023a46a4 ----

void FUN_023a46a4(undefined1 *param_1)

{
  undefined2 *puVar1;
  undefined2 *puVar2;
  ushort *puVar3;
  
  puVar1 = DAT_023a4710;
  do {
  } while ((*DAT_023a470c & 0x80) != 0);
  *DAT_023a470c = 0x8900;
  *puVar1 = 5;
  puVar2 = DAT_023a4710;
  puVar3 = puVar1 + -1;
  do {
  } while ((*puVar3 & 0x80) != 0);
  *puVar3 = 0x8100;
  *puVar2 = 0;
  do {
  } while ((puVar2[-1] & 0x80) != 0);
  *param_1 = (char)*DAT_023a4710;
  return;
}



// ---- FUN_023a51c4 @ 023a51c4 ----

void FUN_023a51c4(uint param_1,uint param_2)

{
  int iVar1;
  
  do {
    iVar1 = func_0x033ad5a4(5,(param_1 & 0x7f) << 8 | 0x8000 | param_2 & 0xff,0);
  } while (iVar1 < 0);
  return;
}



// ---- FUN_023a5204 @ 023a5204 ----

void FUN_023a5204(void)

{
  undefined2 uVar1;
  ushort *puVar2;
  int iVar3;
  int iVar4;
  undefined4 in_r3;
  undefined4 uStack_28;
  
  iVar3 = DAT_023a567c;
  puVar2 = DAT_023a5678;
  uStack_28 = in_r3;
LAB_023a5228:
  func_0x033ab9a8(DAT_023a5680,&uStack_28,1);
  uVar1 = *(undefined2 *)(DAT_023a5684 + 0xdc);
  switch(uVar1) {
  case 0:
    FUN_023a5788();
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0,0);
    goto LAB_023a5228;
  case 1:
    FUN_023a57cc((*puVar2 & 3) >> 1);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(1,0);
    goto LAB_023a5228;
  case 2:
    break;
  case 3:
    break;
  case 4:
    break;
  case 5:
    break;
  case 6:
    break;
  case 7:
    break;
  case 8:
    break;
  case 9:
    break;
  case 10:
    break;
  case 0xb:
    break;
  case 0xc:
    break;
  case 0xd:
    break;
  case 0xe:
    break;
  case 0xf:
    break;
  case 0x10:
    FUN_023a58f0(puVar2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x10,0);
    goto LAB_023a5228;
  case 0x11:
    FUN_023a5954(puVar2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x11,0);
    goto LAB_023a5228;
  case 0x12:
    FUN_023a5980(puVar2 + 2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x12,0);
    goto LAB_023a5228;
  case 0x13:
    iVar4 = FUN_023a59e4(puVar2 + 2);
    if (iVar4 == 0) {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x13,2);
    }
    else {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x13,0);
    }
    goto LAB_023a5228;
  case 0x14:
    iVar4 = FUN_023a5ac0(puVar2 + 2);
    if (iVar4 == 0) {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x14,2);
    }
    else {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x14,0);
    }
    goto LAB_023a5228;
  case 0x15:
    iVar4 = FUN_023a5b94(puVar2 + 2);
    if (iVar4 == 0) {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x15,2);
    }
    else {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x15,0);
    }
    goto LAB_023a5228;
  case 0x16:
    FUN_023a5c60(puVar2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x16,0);
    goto LAB_023a5228;
  case 0x17:
    FUN_023a5cc4(puVar2 + 1);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x17,0);
    goto LAB_023a5228;
  case 0x18:
    FUN_023a5d28(puVar2 + 2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x18,0);
    goto LAB_023a5228;
  case 0x19:
    FUN_023a5d8c(puVar2 + 2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x19,0);
    goto LAB_023a5228;
  case 0x1a:
    break;
  case 0x1b:
    break;
  case 0x1c:
    break;
  case 0x1d:
    break;
  case 0x1e:
    break;
  case 0x1f:
    break;
  case 0x20:
    FUN_023a591c(puVar2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x20,0);
    goto LAB_023a5228;
  case 0x21:
    FUN_023a5980(puVar2 + 2);
    FUN_023a591c(puVar2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x21,0);
    goto LAB_023a5228;
  case 0x22:
    FUN_023a59ac(puVar2 + 2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x22,0);
    goto LAB_023a5228;
  case 0x23:
    iVar4 = FUN_023a5a4c(puVar2 + 2);
    if (iVar4 == 0) {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x23,2);
    }
    else {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x23,0);
    }
    goto LAB_023a5228;
  case 0x24:
    iVar4 = FUN_023a5b24(puVar2 + 2);
    if (iVar4 == 0) {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x24,2);
    }
    else {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x24,0);
    }
    goto LAB_023a5228;
  case 0x25:
    iVar4 = FUN_023a5bf4(puVar2 + 2);
    if (iVar4 == 0) {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x25,2);
    }
    else {
      *(undefined4 *)(iVar3 + 0x1d8) = 0;
      FUN_023a51c4(0x25,0);
    }
    goto LAB_023a5228;
  case 0x26:
    FUN_023a5c8c(puVar2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x26,0);
    goto LAB_023a5228;
  case 0x27:
    FUN_023a5cf0(puVar2 + 1);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x27,0);
    goto LAB_023a5228;
  case 0x28:
    FUN_023a5d54(puVar2 + 2);
    *(undefined4 *)(iVar3 + 0x1d8) = 0;
    FUN_023a51c4(0x28,0);
    goto LAB_023a5228;
  case 0x29:
    goto LAB_023a5644;
  }
  *(undefined4 *)(iVar3 + 0x1d8) = 0;
  FUN_023a51c4(uVar1,1);
  goto LAB_023a5228;
LAB_023a5644:
  FUN_023a5db8(puVar2 + 2);
  *(undefined4 *)(iVar3 + 0x1d8) = 0;
  FUN_023a51c4(0x29,0);
  goto LAB_023a5228;
}



// ---- FUN_023a5718 @ 023a5718 ----

int FUN_023a5718(uint param_1)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  
  iVar2 = 0;
  uVar1 = 0;
  while( true ) {
    if (7 < (int)uVar1) {
      uVar1 = 0;
      iVar3 = 1;
      do {
        iVar2 = iVar3 * (param_1 >> ((uVar1 & 0x3f) << 2) & 0xf) + iVar2;
        uVar1 = uVar1 + 1;
        iVar3 = iVar3 * 10;
      } while ((int)uVar1 < 8);
      return iVar2;
    }
    if (9 < (param_1 >> ((uVar1 & 0x3f) << 2) & 0xf)) break;
    uVar1 = uVar1 + 1;
  }
  return 0;
}



// ---- FUN_023a5788 @ 023a5788 ----

void FUN_023a5788(void)

{
  uint in_r3;
  uint local_8 [2];
  
  local_8[0] = in_r3;
  func_0x033ad73c(0x8000);
  local_8[0] = local_8[0] & 0xfffffffe | 1;
  FUN_023a606c();
  FUN_023a60e0(6,0);
  FUN_023a6150(local_8,1);
  FUN_023a60ac();
  return;
}



// ---- FUN_023a57cc @ 023a57cc ----

/* WARNING: Removing unreachable block (ram,0x023a586c) */
/* WARNING: Removing unreachable block (ram,0x023a58b8) */

void FUN_023a57cc(ushort param_1)

{
  ushort local_10 [2];
  undefined1 auStack_c [4];
  
  if ((param_1 & 1) == 1) {
    func_0x033ad73c(0x8000);
    FUN_023a6010(0x86,0,local_10,1);
    if (-1 < (int)((uint)local_10[0] << 0x1e)) {
      local_10[0] = local_10[0] & 0xfffd | (param_1 & 1) << 1;
      func_0x033ad73c(0x8000);
      FUN_023a606c();
      FUN_023a60e0(6,0);
      FUN_023a6150(local_10,1);
      FUN_023a60ac();
      FUN_023a6010(0x86,0x10,auStack_c,3);
      FUN_023a5f00(auStack_c);
      FUN_023a606c();
      FUN_023a60e0(6,0x10);
      FUN_023a6150(auStack_c,3);
      FUN_023a60ac();
      FUN_023a6010(0x86,0x50,auStack_c,3);
      FUN_023a5f00(auStack_c);
      FUN_023a606c();
      FUN_023a60e0(6,0x50);
      FUN_023a6150(auStack_c,3);
      FUN_023a60ac();
    }
  }
  return;
}



// ---- FUN_023a58f0 @ 023a58f0 ----

void FUN_023a58f0(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x20,param_1,7);
  return;
}



// ---- FUN_023a591c @ 023a591c ----

void FUN_023a591c(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a606c();
  FUN_023a60e0(6,0x20);
  FUN_023a6150(param_1,7);
  FUN_023a60ac();
  return;
}



// ---- FUN_023a5954 @ 023a5954 ----

void FUN_023a5954(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x20,param_1,4);
  return;
}



// ---- FUN_023a5980 @ 023a5980 ----

void FUN_023a5980(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x60,param_1,3);
  return;
}



// ---- FUN_023a59ac @ 023a59ac ----

void FUN_023a59ac(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a606c();
  FUN_023a60e0(6,0x60);
  FUN_023a6150(param_1,3);
  FUN_023a60ac();
  return;
}



// ---- FUN_023a59e4 @ 023a59e4 ----

bool FUN_023a59e4(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  bool bVar1;
  ushort local_10 [2];
  undefined4 local_c;
  
  local_c = param_4;
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x40,local_10,1);
  bVar1 = (local_10[0] & 0xb) == 1;
  if (bVar1) {
    FUN_023a6010(0x86,0x10,param_1,1);
  }
  return bVar1;
}



// ---- FUN_023a5a4c @ 023a5a4c ----

bool FUN_023a5a4c(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  bool bVar1;
  ushort local_10 [2];
  undefined4 local_c;
  
  local_c = param_4;
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x40,local_10,1);
  bVar1 = (local_10[0] & 0xb) == 1;
  if (bVar1) {
    FUN_023a606c(1);
    FUN_023a60e0(6,0x10);
    FUN_023a6150(param_1,1);
    FUN_023a60ac();
  }
  return bVar1;
}



// ---- FUN_023a5ac0 @ 023a5ac0 ----

bool FUN_023a5ac0(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  bool bVar1;
  ushort local_10 [2];
  undefined4 local_c;
  
  local_c = param_4;
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x40,local_10,1);
  bVar1 = (local_10[0] & 0xf) == 4;
  if (bVar1) {
    FUN_023a6010(0x86,0x10,param_1,3);
  }
  return bVar1;
}



// ---- FUN_023a5b24 @ 023a5b24 ----

bool FUN_023a5b24(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  bool bVar1;
  ushort local_10 [2];
  undefined4 local_c;
  
  local_c = param_4;
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x40,local_10,1);
  bVar1 = (local_10[0] & 0xf) == 4;
  if (bVar1) {
    FUN_023a606c(4);
    FUN_023a60e0(6,0x10);
    FUN_023a6150(param_1,3);
    FUN_023a60ac();
  }
  return bVar1;
}



// ---- FUN_023a5b94 @ 023a5b94 ----

bool FUN_023a5b94(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  bool bVar1;
  ushort local_10 [2];
  undefined4 local_c;
  
  local_c = param_4;
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x40,local_10,1);
  bVar1 = (int)((uint)local_10[0] << 0x19) < 0;
  if (bVar1) {
    FUN_023a6010(0x86,0x50,param_1,3);
  }
  return bVar1;
}



// ---- FUN_023a5bf4 @ 023a5bf4 ----

bool FUN_023a5bf4(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  int iVar1;
  ushort local_10 [2];
  undefined4 local_c;
  
  local_c = param_4;
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x40,local_10,1);
  iVar1 = -((int)((uint)local_10[0] << 0x19) >> 0x1f);
  if (iVar1 != 0) {
    FUN_023a606c(iVar1);
    FUN_023a60e0(6,0x50);
    FUN_023a6150(param_1,3);
    FUN_023a60ac();
  }
  return iVar1 != 0;
}



// ---- FUN_023a5c60 @ 023a5c60 ----

void FUN_023a5c60(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0,param_1,1);
  return;
}



// ---- FUN_023a5c8c @ 023a5c8c ----

void FUN_023a5c8c(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a606c();
  FUN_023a60e0(6,0);
  FUN_023a6150(param_1,1);
  FUN_023a60ac();
  return;
}



// ---- FUN_023a5cc4 @ 023a5cc4 ----

void FUN_023a5cc4(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x40,param_1,1);
  return;
}



// ---- FUN_023a5cf0 @ 023a5cf0 ----

void FUN_023a5cf0(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a606c();
  FUN_023a60e0(6,0x40);
  FUN_023a6150(param_1,1);
  FUN_023a60ac();
  return;
}



// ---- FUN_023a5d28 @ 023a5d28 ----

void FUN_023a5d28(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x30,param_1,1);
  return;
}



// ---- FUN_023a5d54 @ 023a5d54 ----

void FUN_023a5d54(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a606c();
  FUN_023a60e0(6,0x30);
  FUN_023a6150(param_1,1);
  FUN_023a60ac();
  return;
}



// ---- FUN_023a5d8c @ 023a5d8c ----

void FUN_023a5d8c(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a6010(0x86,0x70,param_1,1);
  return;
}



// ---- FUN_023a5db8 @ 023a5db8 ----

void FUN_023a5db8(undefined4 param_1)

{
  func_0x033ad73c(0x8000);
  FUN_023a606c();
  FUN_023a60e0(6,0x70);
  FUN_023a6150(param_1,1);
  FUN_023a60ac();
  return;
}



// ---- FUN_023a5df0 @ 023a5df0 ----

void FUN_023a5df0(uint *param_1)

{
  uint uVar1;
  
  uVar1 = *param_1;
  switch((uVar1 & 0x3fff) >> 8) {
  case 0:
    goto LAB_023a5e98;
  case 1:
    goto LAB_023a5e98;
  case 2:
    goto LAB_023a5e98;
  case 3:
    goto LAB_023a5e98;
  case 4:
    goto LAB_023a5e98;
  case 5:
    goto LAB_023a5e98;
  case 6:
    goto LAB_023a5e98;
  case 7:
    goto LAB_023a5e98;
  case 8:
    goto LAB_023a5e98;
  case 9:
    goto LAB_023a5e98;
  case 10:
    break;
  case 0xb:
    break;
  case 0xc:
    break;
  case 0xd:
    break;
  case 0xe:
    break;
  case 0xf:
    break;
  case 0x10:
    goto LAB_023a5e98;
  case 0x11:
LAB_023a5e98:
    *param_1 = uVar1 & 0xffffbfff;
    return;
  case 0x12:
    goto LAB_023a5ea4;
  case 0x13:
    goto LAB_023a5ea4;
  case 0x14:
    goto LAB_023a5ea4;
  case 0x15:
    goto LAB_023a5ea4;
  case 0x16:
    goto LAB_023a5ea4;
  case 0x17:
    goto LAB_023a5ea4;
  case 0x18:
    goto LAB_023a5ea4;
  case 0x19:
    goto LAB_023a5ea4;
  case 0x1a:
    break;
  case 0x1b:
    break;
  case 0x1c:
    break;
  case 0x1d:
    break;
  case 0x1e:
    break;
  case 0x1f:
    break;
  case 0x20:
    goto LAB_023a5ec8;
  case 0x21:
LAB_023a5ec8:
    *param_1 = uVar1 & 0xffffc0ff | 0x4000 | (((uVar1 & 0x3fff) >> 8) - 0x18 & 0x3f) << 8;
    return;
  case 0x22:
    goto LAB_023a5ea4;
  case 0x23:
LAB_023a5ea4:
    *param_1 = uVar1 & 0xffffc0ff | 0x4000 | (((uVar1 & 0x3fff) >> 8) - 0x12 & 0x3f) << 8;
    return;
  }
  *param_1 = *param_1 & 0xffff80ff;
  return;
}



// ---- FUN_023a5f00 @ 023a5f00 ----

void FUN_023a5f00(uint *param_1)

{
  uint uVar1;
  uint uVar2;
  
  uVar2 = *param_1;
  uVar1 = (uVar2 & 0x3fff) >> 8;
  switch(uVar1) {
  case 0:
    goto LAB_023a5fa8;
  case 1:
    goto LAB_023a5fa8;
  case 2:
    goto LAB_023a5fa8;
  case 3:
    goto LAB_023a5fa8;
  case 4:
    goto LAB_023a5fa8;
  case 5:
    goto LAB_023a5fa8;
  case 6:
    goto LAB_023a5fa8;
  case 7:
    goto LAB_023a5fa8;
  case 8:
    goto LAB_023a5fcc;
  case 9:
LAB_023a5fcc:
    if ((int)(uVar2 << 0x11) < 0) {
      *param_1 = uVar2 & 0xffffc0ff | (uVar1 + 0x18 & 0x3f) << 8;
      return;
    }
    return;
  case 10:
    break;
  case 0xb:
    break;
  case 0xc:
    break;
  case 0xd:
    break;
  case 0xe:
    break;
  case 0xf:
    break;
  case 0x10:
    goto LAB_023a5fa8;
  case 0x11:
LAB_023a5fa8:
    if ((int)(uVar2 << 0x11) < 0) {
      *param_1 = uVar2 & 0xffffc0ff | (uVar1 + 0x12 & 0x3f) << 8;
      return;
    }
    return;
  case 0x12:
    goto LAB_023a5ff0;
  case 0x13:
    goto LAB_023a5ff0;
  case 0x14:
    goto LAB_023a5ff0;
  case 0x15:
    goto LAB_023a5ff0;
  case 0x16:
    goto LAB_023a5ff0;
  case 0x17:
    goto LAB_023a5ff0;
  case 0x18:
    goto LAB_023a5ff0;
  case 0x19:
    goto LAB_023a5ff0;
  case 0x1a:
    break;
  case 0x1b:
    break;
  case 0x1c:
    break;
  case 0x1d:
    break;
  case 0x1e:
    break;
  case 0x1f:
    break;
  case 0x20:
    goto LAB_023a5ff0;
  case 0x21:
    goto LAB_023a5ff0;
  case 0x22:
    goto LAB_023a5ff0;
  case 0x23:
LAB_023a5ff0:
    *param_1 = uVar2 | 0x4000;
    return;
  }
  *param_1 = *param_1 & 0xffff80ff;
  return;
}



// ---- FUN_023a6010 @ 023a6010 ----

void FUN_023a6010(int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  FUN_023a606c();
  FUN_023a60e0(param_1,param_2);
  if (param_1 == 6) {
    FUN_023a6150(param_3,param_4);
  }
  else if (param_1 == 0x86) {
    FUN_023a61e0(param_3,param_4);
  }
  FUN_023a60ac();
  return;
}



// ---- FUN_023a606c @ 023a606c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_023a606c(void)

{
  int iVar1;
  
  iVar1 = 2;
  do {
    iVar1 = iVar1 + -1;
  } while (iVar1 != 0);
  _DAT_04000138 = _DAT_04000138 & 0xff88 | 0x76;
  iVar1 = 2;
  do {
    iVar1 = iVar1 + -1;
  } while (iVar1 != 0);
  return;
}



// ---- FUN_023a60ac @ 023a60ac ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_023a60ac(void)

{
  int iVar1;
  
  iVar1 = 2;
  do {
    iVar1 = iVar1 + -1;
  } while (iVar1 != 0);
  _DAT_04000138 = _DAT_04000138 & 0xfffb;
  iVar1 = 2;
  do {
    iVar1 = iVar1 + -1;
  } while (iVar1 != 0);
  return;
}



// ---- FUN_023a60e0 @ 023a60e0 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_023a60e0(uint param_1,uint param_2)

{
  uint uVar1;
  int iVar2;
  
  _DAT_04000138 = _DAT_04000138 & 0xff88 | 0x74;
  uVar1 = 0;
  do {
    iVar2 = 9;
    do {
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    _DAT_04000138 =
         _DAT_04000138 & 0xfffc | (ushort)(((param_1 | param_2) >> (uVar1 & 0xff) & 1) != 0) | 2;
    iVar2 = 9;
    do {
      iVar2 = iVar2 + -1;
    } while (iVar2 != 0);
    uVar1 = uVar1 + 1;
  } while (uVar1 != 8);
  return;
}



// ---- FUN_023a6150 @ 023a6150 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_023a6150(ushort *param_1,int param_2)

{
  ushort uVar1;
  uint uVar2;
  int iVar3;
  
  do {
    if (((uint)param_1 & 1) == 0) {
      uVar1 = *param_1;
    }
    else {
      uVar1 = *(ushort *)((int)param_1 + -1) >> 8;
    }
    _DAT_04000138 = _DAT_04000138 & 0xff88 | 0x74;
    uVar2 = 0;
    do {
      iVar3 = 9;
      do {
        iVar3 = iVar3 + -1;
      } while (iVar3 != 0);
      _DAT_04000138 = _DAT_04000138 & 0xfffc | (ushort)((uVar1 >> (uVar2 & 0xff) & 1) != 0) | 2;
      iVar3 = 9;
      do {
        iVar3 = iVar3 + -1;
      } while (iVar3 != 0);
      uVar2 = uVar2 + 1;
    } while (uVar2 != 8);
    param_1 = (ushort *)((int)param_1 + 1);
    param_2 = param_2 + -1;
  } while (param_2 != 0);
  return;
}



// ---- FUN_023a61e0 @ 023a61e0 ----

/* WARNING: Removing unreachable block (ram,0x023a6224) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_023a61e0(ushort *param_1,int param_2)

{
  int iVar1;
  int iVar2;
  
  do {
    _DAT_04000138 = _DAT_04000138 & 0xff88 | 100;
    iVar1 = 0;
    do {
      iVar2 = 9;
      do {
        iVar2 = iVar2 + -1;
      } while (iVar2 != 0);
      _DAT_04000138 = _DAT_04000138 & 0xfffc | 2;
      iVar2 = 9;
      do {
        iVar2 = iVar2 + -1;
      } while (iVar2 != 0);
      iVar1 = iVar1 + 1;
    } while (iVar1 != 8);
    if (((uint)param_1 & 1) == 0) {
      *param_1 = *param_1 & 0xff00;
    }
    else {
      *(ushort *)((int)param_1 + -1) = *(ushort *)((int)param_1 + -1) & 0xff;
    }
    param_1 = (ushort *)((int)param_1 + 1);
    param_2 = param_2 + -1;
  } while (param_2 != 0);
  return;
}



