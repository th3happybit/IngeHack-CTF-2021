#include <Windows.h>
#include <stdio.h>
#include "ulnfeat.h"

// real_flag : "IngeHack{D0n7_l337_7L5_CAlLBAcK5_f00L_Y0u}"
// fake_flag : "IngeHack{Do_YOU_R3LLY_7H1NK_7H1s_1s_17!!!}"

const int DATA_SIZE = 42;
int data[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 95, 49, 110, 16, 57, 108, 97, 4, 19, 123, 21, 106, 104, 11, 112, 34, 7, 29, 118, 43, 122, 70, 0, 87, 67, 111, 125, 104, 120, 17, 84, 0};
int xorWith[] = {32, 11, 84, 22, 2, 25, 38, 27, 66, 52, 45, 4, 21, 23, 118, 120, 17, 64, 21, 26, 116, 43, 110, 51, 11, 13, 110, 44, 80, 106, 82, 48, 38, 87, 45, 62, 102, 94, 110, 30, 80, 75};
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
