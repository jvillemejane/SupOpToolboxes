import threading
def even():#creating second function
    for i in range(0,20,2):
        print(i)
def odd():
    for i in range(1,20,2):
        print(i)

# creating a thread for each function
trd1 = threading.Thread(target=even)
trd2 = threading.Thread(target=odd)

trd1.start() # starting the thread 1
trd2.start() # starting the thread 2

print('End')