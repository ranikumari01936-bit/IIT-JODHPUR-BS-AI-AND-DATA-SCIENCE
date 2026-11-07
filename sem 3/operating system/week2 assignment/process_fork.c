#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    } else if (pid == 0) {
        printf("Child process: PID = %d, Parent PID = %d\n",
               (int)getpid(), (int)getppid());
    } else {
        printf("Parent process: PID = %d, Child PID = %d\n",
               (int)getpid(), (int)pid);
        wait(NULL);
    }

    return 0;
}
