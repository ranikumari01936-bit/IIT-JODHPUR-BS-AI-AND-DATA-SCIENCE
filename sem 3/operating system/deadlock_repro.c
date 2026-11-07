/* 
 * Student Name: Rani Kumari | Roll No: B25BS1270 | Email: b25bs1270@iitj.ac.in
 * Operating Systems (OS) - Week 4 Question 2: Deadlock Reproduction
 * 
 * File: deadlock_repro.c
 * Description: Demonstrates a deadlock scenario using two processes (threads P0, P1) 
 *              and two binary semaphores (S, Q). P0 requests S then Q, while P1 
 *              requests Q then S, creating a Circular Wait condition.
 */

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

// Binary Semaphores
sem_t S;
sem_t Q;

void* process_P0(void* arg) {
    printf("P0: Trying to acquire Semaphore S...\n");
    sem_wait(&S);
    printf("P0: Acquired Semaphore S! Sleeping for 1 second...\n");
    
    sleep(1); // Force context switch to allow P1 to acquire Q
    
    printf("P0: Trying to acquire Semaphore Q...\n");
    sem_wait(&Q); // Deadlock occurs here: P0 waits for Q (held by P1)
    
    printf("P0: Acquired both S and Q. Executing critical section.\n");
    
    sem_post(&Q);
    sem_post(&S);
    return NULL;
}

void* process_P1(void* arg) {
    printf("P1: Trying to acquire Semaphore Q...\n");
    sem_wait(&Q);
    printf("P1: Acquired Semaphore Q! Sleeping for 1 second...\n");
    
    sleep(1); // Force context switch
    
    printf("P1: Trying to acquire Semaphore S...\n");
    sem_wait(&S); // Deadlock occurs here: P1 waits for S (held by P0)
    
    printf("P1: Acquired both Q and S. Executing critical section.\n");
    
    sem_post(&S);
    sem_post(&Q);
    return NULL;
}

int main() {
    pthread_t t0, t1;
    
    printf("==================================================================\n");
    printf("DEADLOCK REPRODUCTION SIMULATION\n");
    printf("Student: Arun Pratap Singh | Roll No: B24BS2044 | Email: b24bs2044@iitj.ac.in\n");
    printf("==================================================================\n\n");

    // Initialize both binary semaphores to 1
    sem_init(&S, 0, 1);
    sem_init(&Q, 0, 1);
    
    printf("Starting Deadlock Reproduction Execution...\n");
    
    pthread_create(&t0, NULL, process_P0, NULL);
    pthread_create(&t1, NULL, process_P1, NULL);
    
    pthread_join(t0, NULL);
    pthread_join(t1, NULL);
    
    // Unreachable due to deadlock (System Hangs indefinitely)
    printf("Execution Completed Successfully.\n"); 
    
    sem_destroy(&S);
    sem_destroy(&Q);
    return 0;
}
