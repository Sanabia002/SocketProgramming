import socket
import tqdm
import os
import threading
from cryptography.fernet import Fernet
#key = Fernet.generate_key()

#with open('mykey.key', 'wb') as mykey:
    #mykey.write(key)
with open('mykey.key', 'rb') as mykey:
    key = mykey.read()
f = Fernet(key)

with open('plaintext.txt', 'rb') as original_file:
    original = original_file.read()

encrypted = f.encrypt(original)

with open ('cipher.txt', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
host = "169.254.123.111"
port = 5001
# the name of file we want to send, make sure it exists
filename = "cipher.txt"
# get the file size
filesize = os.path.getsize(filename)
# create the client socket
s = socket.socket()
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())
# start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in 
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
