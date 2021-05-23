#define  _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>
#include <openssl/sha.h>
#include <string.h>
/* Number of users */
#define N 2 


struct user {
    char username[33];
    char password[64];
    int uid;
    int gid;
    char shell[33];
};
void sha256(char *string, char outputBuffer[65])
{
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    int i = 0;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, string, strlen(string));
    SHA256_Final(hash, &sha256);
    for(i = 0; i < SHA256_DIGEST_LENGTH; i++)
    {
        sprintf(outputBuffer + (i * 2), "%02x", hash[i]);
    }
    outputBuffer[64] = 0;
}

struct user *Parser(FILE *fd){
    /*Function Parser*/
    /*It parses our custom passwd file 
    that is defined in the format:
    username:password:uid:gid:shell
    */
    /*It returns a list of users parsed from CustomPasswd*/
    struct user *users = malloc(sizeof(struct user) * N);
    char * line = NULL;
    char * part = NULL;
    size_t len = 0;
    ssize_t read;
    int n = 0;
    while (((read = getline(&line, &len, fd)) != -1) && (n < N)) {
        part = strtok(line, ":");
        strcpy(users[n].username, part);
        part = strtok(NULL, ":");
        strcpy(users[n].password, part);
        part = strtok(NULL, ":");
        users[n].uid = atoi(part);
        part = strtok(NULL, ":");
        users[n].gid = atoi(part);
        part = strtok(NULL, ":");
        part[strcspn(part, "\n")] = 0; /* remove the trailing newline */
        strcpy(users[n].shell, part);
        n++;
    }

    return users;
}

int main () {
    FILE *file_descriptor;
    int i = 0;
    char username[33];
    char password[33];
    char hashedPassword[65];
    struct user loggedInUser, *users;
    char *args[] = {NULL, 0};
    strcpy(loggedInUser.username,"");
    file_descriptor = fopen("./customPasswds", "r");
    printf("Username:");
    fflush(stdout);
    fgets(username,33,stdin);
    username[strcspn(username, "\n")] = 0;
    if(strlen(username)<4){
        puts("Invalid username");
        return -1;
    }
    printf("Passsword:");
    fflush(stdout);
    fgets(password,33,stdin);
    password[strcspn(password, "\n")] = 0;
    sha256(password,hashedPassword);
    users = Parser(file_descriptor);

    for(i=0;i<N;i++){
        if(strcmp(username,users[i].username)==0){
            if(strcmp(hashedPassword , users[i].password)==0){
                loggedInUser = users[i];
                break;
            }else{
                puts("Wrong Password");
                free(users);
                return -1;
            }
        }
    }
    /* Restoring resources */
    fseek(file_descriptor, 0L, 0);
    free(users);


    if(strcmp(loggedInUser.username, "")==0){
        puts("User doesn't exist");
        return -1;
    }

    printf("OPEN SESAME!\n");
    fflush(stdout);

    /* dropping privileges */
    setgroups(0, NULL);
    setgid(loggedInUser.gid); 
    setuid(loggedInUser.uid); 

    args[1] = loggedInUser.shell;
    execvp(loggedInUser.shell, args);
    return 0;
}
