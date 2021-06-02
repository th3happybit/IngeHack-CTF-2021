#include <pybind11/pybind11.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#define STATE_SIZE 256
#define BUFFER_SIZE 256

namespace py = pybind11;

void get_flag()
{
    char buffer[STATE_SIZE];
    bzero(buffer, BUFFER_SIZE);

    FILE *flag_file = fopen("flag.txt", "r");
    fgets(buffer, BUFFER_SIZE, flag_file);

    printf("FLAG: %s\n", buffer);
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

py::bytes rc4(char *key, char *plaintext)
{
    unsigned char state[STATE_SIZE];
    unsigned char ciphertext[BUFFER_SIZE];

    printf("RC4 Init with key %s...", key);
    bzero(ciphertext, BUFFER_SIZE);

    key_scheduling(key, state);
    pseudo_random_generation(state, plaintext, ciphertext);

    std::string str_ciphertext = std::string(ciphertext, ciphertext + strlen(plaintext));
    return py::bytes(str_ciphertext);
}

PYBIND11_MODULE(ingecryptor, m)
{
    m.def("rc4", &rc4, "rc4 cipher");
    m.def("get_flag", &get_flag, "get flag");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
