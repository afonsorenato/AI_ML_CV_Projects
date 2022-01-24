from multiprocessing import Process
import os
import time

def square_numbers():
    print("Running")


processes = []
num_processes = os.cpu_count()

print(num_processes)

for i in range(num_processes):
    p = Process(target=square_numbers)
    processes.append(p)

# Start
for p in processes:
    p.start()

# Join
for p in processes:
    p.join()


print("End main...")