
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void main()
{
    long input;
    printf("ββββ πππππ ππ π₯π  πππ₯π¨ππ€ππ£ πππππππππ ββββ\n");
    printf("ββββ πΎππ§π ππ π₯ππ πππππ ππ¦ππππ£: ");
    fflush(stdout);

    scanf("%ld", &input);

    if (((input & -input) == input) && ((input >> 50) == 1))
    {
        printf("βε½‘ βπ πππ£ππ₯π¦πππ₯ππ ππ€. πͺπ π¦ π¨π π ε½‘β\n");
        printFlag("flag.txt");
        fflush(stdout);
        exit(0);
    }

    printf("γο½‘_ο½‘γ βπ π₯ π₯ππ π£ππππ₯ π ππ, π₯π£πͺ πππππ γο½‘_ο½‘γ");
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