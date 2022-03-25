import time

def callback(ch, method, properties, body):
    print(" [x] Receive %r " % body.decode())
    time.sleep(body.count(b'.'))
    print("[x] Done")