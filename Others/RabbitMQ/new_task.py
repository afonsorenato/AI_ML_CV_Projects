import sys
import time

message = ' '.join(sys.argv[1:]) or "Hello world!"

channel.basic_publish(exchange= '',
                      routing_key = 'hello',
                      body=message)

print(" [x] Sent %r " % message)

print("Test concluded")