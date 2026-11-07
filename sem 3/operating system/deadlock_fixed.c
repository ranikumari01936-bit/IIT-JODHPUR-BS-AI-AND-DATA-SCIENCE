/* 
 * Student Name: Rani Kumari | Roll No: B25BS1270 | Email: b25bs1270@iitj.ac.in
 * Operating Systems (OS) - Week 4 Question 2: Deadlock Resolution
 * 
 * File: deadlock_fixed.c
 * Description: Corrects the deadlock scenario by enforcing consistent resource ordering.
 *              Both P0 and P1 request Semaphore S first, then Semaphore Q, breaking
 *              the Circular Wait condition.
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
    printf("P0: Acquired Semaphore S!\n");
    
    sleep(1);
    
    printf("P0: Trying to acquire Semaphore Q...\n");
    sem_wait(&Q);
    printf("P0: Acquired both S and Q. Executing critical section.\n");
    
    sem_post(&Q);
    sem_post(&S);
    printf("P0: Released both semaphores S and Q.\n\n");
    return NULL;
}

void* process_P1(void* arg) {
    // FIX: Resource Ordering Strategy. Both processes request S first, then Q.
    printf("P1: Trying to acquire Semaphore S...\n");
    sem_wait(&S);
    printf("P1: Acquired Semaphore S!\n");
    
    sleep(1);
    
    printf("P1: Trying to acquire Semaphore Q...\n");
    sem_wait(&Q);
    printf("P1: Acquired both S and Q. Executing critical section.\n");
    
    sem_post(&Q);
    sem_post(&S);
    printf("P1: Released both semaphores S and Q.\n\n");
    return NULL;
}

int main() {
    pthread_t t0, t1;
    
    printf("==================================================================\n");
    printf("DEADLOCK RESOLUTION SIMULATION (RESOURCE ORDERING FIX)\n");
    printf("Student: Arun Pratap Singh | Roll No: B24BS2044 | Email: b24bs2044@iitj.ac.in\n");
    printf("==================================================================\n\n");

    // Initialize both binary semaphores to 1
    sem_init(&S, 0, 1);
    sem_init(&Q, 0, 1);
    
    printf("Starting Fixed Execution...\n\n");
    
    pthread_create(&t0, NULL, process_P0, NULL);
    pthread_create(&t1, NULL, process_P1, NULL);
    
    pthread_join(t0, NULL);
    pthread_join(t1, NULL);
    
    printf("Execution Completed Successfully without Deadlock.\n");
    
    sem_destroy(&S);
    sem_destroy(&Q);
    return 0;
}
