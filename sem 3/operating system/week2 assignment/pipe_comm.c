#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void) {
    int fd[2];
    pid_t pid;
    char buffer[100];

    // Create pipe before fork()
    if (pipe(fd) == -1) {
        perror("pipe failed");
        return 1;
    }

    // Create child process
    pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }

    if (pid > 0) {
        // Parent process
        close(fd[0]);  // Close read end

        const char message[] = "Hello from the parent process!";
        write(fd[1], message, sizeof(message));

        close(fd[1]);  // Close write end
        wait(NULL);

    } else {
        // Child process
        close(fd[1]);  // Close write end

        ssize_t bytes_read = read(fd[0], buffer, sizeof(buffer) - 1);

        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';
            printf("Child received message: %s\n", buffer);
        }

        close(fd[0]);  // Close read end
    }

    return 0;
}
