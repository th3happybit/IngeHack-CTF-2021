
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void main()
{
    long input;
    printf("░▒▓█ 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕥𝕠 𝕓𝕚𝕥𝕨𝕚𝕤𝕖𝕣 𝕔𝕙𝕒𝕝𝕝𝕖𝕟𝕘𝕖 █▓▒░\n");
    printf("░▒▓█ 𝔾𝕚𝕧𝕖 𝕞𝕖 𝕥𝕙𝕖 𝕞𝕒𝕘𝕚𝕔 𝕟𝕦𝕞𝕓𝕖𝕣: ");
    fflush(stdout);

    scanf("%ld", &input);

    if (((input & -input) == input) && ((input >> 50) == 1))
    {
        printf("★彡 ℂ𝕠𝕟𝕘𝕣𝕒𝕥𝕦𝕝𝕒𝕥𝕚𝕠𝕟𝕤. 𝕪𝕠𝕦 𝕨𝕠𝕟 彡★\n");
        printFlag("flag.txt");
        fflush(stdout);
        exit(0);
    }

    printf("【｡_｡】 ℕ𝕠𝕥 𝕥𝕙𝕖 𝕣𝕚𝕘𝕙𝕥 𝕠𝕟𝕖, 𝕥𝕣𝕪 𝕒𝕘𝕒𝕚𝕟 【｡_｡】");
    fflush(stdout);
    exit(1);
}

void printFlag(char fileName[])
{
    // Open file
    FILE *fptr;
    setreuid(geteuid(), geteuid());
    fptr = fopen(fileName, "r");
    if (fptr == NULL)
    {
        printf("Cannot open file \n");
        exit(1);
    }

    // Read contents from file
    char c = fgetc(fptr);
    while (c != EOF)
    {
        printf("%c", c);
        c = fgetc(fptr);
    }

    fclose(fptr);
}