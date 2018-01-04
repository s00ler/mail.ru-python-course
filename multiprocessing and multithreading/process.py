import time
import os

pid = os.fork()
if pid == 0:
    print('Child {}'.format(os.getpid()))
else:
    print('Parent {}'.format(os.getpid()))

while True:
    print(pid, time.time())
    time.sleep(2)
