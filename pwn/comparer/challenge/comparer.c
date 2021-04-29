#include <stdlib.h>
#include <stdio.h>

#define MAX_SIZE 32
#define PASSFILE "flag.txt"

int long_cmp(long x, long y)
{
    if (x == y)
        return 0;
    if (x > y)
        return 1;
    else
        return -1;
}

int main(int argc, char **argv)
{
    char pass_buf[MAX_SIZE];
    FILE *pass_file = NULL;

    long input_pass, pass;

    if (argc != 2)
    {
        printf("Usage %s <PASS>.\n", argv[0]);
        exit(1);
    }

    if ((pass_file = fopen(PASSFILE, "r")) == NULL || fgets(pass_buf, MAX_SIZE, pass_file) == NULL)
    {
        printf("Failed reading PASSFILE: %s.\n", PASSFILE);
        exit(2);
    }

    input_pass = atol(argv[1]);
    pass = atol(pass_buf);

    if (long_cmp(input_pass, pass) == 0)
    {
        printf("Good Job, here is your flag:\nIngeHack{%ld}\n", pass);
    }
}
