#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <time.h>

const char CHAR_SET[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!'};
const int LENGTH = 63;

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

void main()
{
    char name[143];
    char input;

    time_t seconds = time(NULL);

    printf("Welcome to a super gussing challenge\n");
    printf("Don't be rude and introduce your self:");
    fflush(stdout);
    fgets(name, 150, stdin);

    srand(seconds);

    char randomeChar;
    for (int i = 0; i < LENGTH; i++)
    {
        randomeChar = CHAR_SET[rand() % LENGTH];
        printf("I chose a random character, gusse it:");
        fflush(stdout);
        scanf("%c", &input);

        // to read extra new line form buffer (ignore it)
        getchar();

        if (input != randomeChar)
        {
            printf("You guessed it wrong! Good by");
            exit(-1);
        }
    }

    printf("You really did it hah!\n");
    printFlag("flag.txt");
}
