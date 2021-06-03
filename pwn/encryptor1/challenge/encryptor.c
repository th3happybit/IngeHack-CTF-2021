#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STATE_SIZE 256
#define BUFFER_SIZE 256

void get_flag()
{
    char buffer[STATE_SIZE];
    memset(buffer, 0, BUFFER_SIZE);

    FILE *flag_file = fopen("flag.txt", "r");
    fgets(buffer, BUFFER_SIZE, flag_file);

    write(1, buffer, strlen(buffer));
}

void swap(unsigned char *a, unsigned char *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int key_scheduling(char *key, unsigned char *state)
{

    int len = strlen(key);
    int j = 0;

    for (int i = 0; i < STATE_SIZE; i++)
        state[i] = i;

    for (int i = 0; i < STATE_SIZE; i++)
    {
        j = (j + state[i] + key[i % len]) % STATE_SIZE;

        swap(&state[i], &state[j]);
    }

    return 0;
}

int pseudo_random_generation(unsigned char *state, char *plaintext, unsigned char *ciphertext)
{

    int i = 0;
    int j = 0;

    for (size_t n = 0, len = strlen(plaintext); n < len; n++)
    {
        i = (i + 1) % STATE_SIZE;
        j = (j + state[i]) % STATE_SIZE;

        swap(&state[i], &state[j]);
        unsigned char rnd = state[(state[i] + state[j]) % STATE_SIZE];

        ciphertext[n] = rnd ^ plaintext[n];
    }

    return 0;
}

void rc4(char *key, char *plaintext)
{
    unsigned char ciphertext[BUFFER_SIZE];
    unsigned char state[STATE_SIZE];

    memset(ciphertext, 0, BUFFER_SIZE);

    key_scheduling(key, state);
    pseudo_random_generation(state, plaintext, ciphertext);

    printf(ciphertext);
}

int main(int argc, char **argv)
{
    char key[1024];
    char plaintext[1024];

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    memset(key, 0, 1024);
    memset(plaintext, 0, 1024);

    printf("Key: \n");
    fgets(key, 1024, stdin);
    key[strlen(key) - 1] = '\0';

    while (1)
    {
        printf("Data: \n");
        fgets(plaintext, 1024, stdin);
        plaintext[strlen(plaintext) - 1] = '\0';
        rc4(key, plaintext);
    }
    return 0;
}
