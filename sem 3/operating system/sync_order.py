# Student Name: Rani Kumari | Roll No: B25BS1270 | Email: b25bs1270@iitj.ac.in
# Operating Systems (OS) - Week 4 Assignment: Process Synchronization using Binary Semaphore

import threading
import time

# Initialize binary semaphore to 0 (forces Process P2 to wait for P1's signal)
sync_semaphore = threading.Semaphore(0)

def process_p1():
    # Instruction Set S1
    print("Process P1: Executing Instruction Set S1...")
    time.sleep(0.5)  # Simulating processing time for S1
    
    # Signal operation to increment binary semaphore and unblock P2
    print("Process P1: S1 completed. Sending signal() to semaphore.")
    sync_semaphore.release()

def process_p2():
    print("Process P2: Calling wait() on semaphore. Waiting for P1...")
    # Wait operation to block until P1 issues the signal() call
    sync_semaphore.acquire()
    
    # Instruction Set S2
    print("Process P2: Signal received. Executing Instruction Set S2...\n")

if __name__ == "__main__":
    print("================================================================================")
    print("PROCESS SYNCHRONIZATION SIMULATION USING BINARY SEMAPHORE")
    print("Student: Arun Pratap Singh | Roll No: B24BS2044 | Email: b24bs2044@iitj.ac.in")
    print("================================================================================\n")
    
    # Run the simulation 5 consecutive times to prove synchronization guarantee
    for i in range(1, 6):
        print(f"--- Run {i} ---")
        
        # Create threads for P1 and P2
        t1 = threading.Thread(target=process_p1)
        t2 = threading.Thread(target=process_p2)

        # Start thread P2 first to explicitly prove that P2 blocks and waits for P1
        t2.start()
        time.sleep(0.1)  # Small delay to ensure P2 initiates wait() before P1 starts
        t1.start()

        # Wait for both threads to complete current run before proceeding
        t1.join()
        t2.join()

    print("================================================================================")
    print("SIMULATION SUCCESSFUL: S1 (P1) executed before S2 (P2) across all 5 runs.")
    print("================================================================================")
