#include <Windows.h>
#include <stdio.h>
#include "ulnfeat.h"

// real_flag : "Ingehack{D0n7_l337_7L5_CAlLBAcK5_f00L_Y0u}"
// fake_flag : "IngeHack{Do_YOU_R3LLY_7H1NK_7H1s_1s_17!!!}"

const int DATA_SIZE = 42;
int data[] = {0x0, 0x0, 0x0, 0x0, 0x20, 0x0, 0x0, 0x0, 0x0, 0x0, 0x5f, 0x31, 0x6e, 0x10, 0x39, 0x6c, 0x61, 0x4, 0x13, 0x7b, 0x15, 0x6a, 0x68, 0xb, 0x70, 0x22, 0x7, 0x1d, 0x76, 0x2b, 0x7a, 0x46, 0x0, 0x57, 0x43, 0x6f, 0x7d, 0x68, 0x78, 0x11, 0x54, 0x0};
int xorWith[] = {0x20, 0xb, 0x54, 0x16, 0x2, 0x19, 0x26, 0x1b, 0x42, 0x34, 0x2d, 0x4, 0x15, 0x17, 0x76, 0x78, 0x11, 0x40, 0x15, 0x1a, 0x74, 0x2b, 0x6e, 0x33, 0xb, 0xd, 0x6e, 0x2c, 0x50, 0x6a, 0x52, 0x30, 0x26, 0x57, 0x2d, 0x3e, 0x66, 0x5e, 0x6e, 0x1e, 0x50, 0x4b};
char randomData[] = {105, 101, 51, 115, 74, 120, 69, 112, 57, 112, 66, 91, 76, 88, 35, 39, 67, 115, 89, 86, 45, 116, 89, 123, 58, 67, 37, 115, 103, 34, 99, 67, 121, 102, 94, 97, 87, 105, 79, 63, 113, 54};

void __stdcall callback(void *lpInstance, DWORD dwReason, void *lpReserved)
{
  if (dwReason != DLL_PROCESS_ATTACH)
    return;

  short isBeingDebugged = 0;
  __asm {
		; Grab the PEB at offset 30 of the fs register
		mov eax, fs:[30h]
		; push it to the stack 
		push ecx
		; Grab the IsBeingDebugged flag out of the PED
		mov ecx, [eax+2]
		mov isBeingDebugged, cx
		pop ecx
  }
  if (isBeingDebugged) return;

  for (int i = 0; i < DATA_SIZE; ++i)
  {
    randomData[i] = data[i] ^ randomData[i];
  }
}

TLS_CALLBACK(c1, callback);

int main(void)
{
  char input[DATA_SIZE];
  char flag[DATA_SIZE + 1];
  int index;

  for (int i = 0; i < DATA_SIZE; ++i)
  {
    int value = xorWith[i] ^ randomData[i];
    flag[i] = value;
  }
  flag[DATA_SIZE] = '\0';

  printf("WELECOME\nEnter the secret word : ");
  scanf("%s", input);

  if (strcmp(input, flag) != 0)
  {
    printf("Not the right one at all kido ;)");
  }
  else
  {
    printf("It may or may not be the right one ;)");
  }

  // this call just to prevent compiler from removing callback function from binary
  // remove this by patching binary and replace function call with nop instructions
  callback(NULL, NULL, NULL);
  return 0;
}
