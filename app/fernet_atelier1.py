import os
import sys
from cryptography.fernet import Fernet

key = os.getenv("FERNET_KEY").encode()
fernet = Fernet(key)

mode = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

with open(input_file, "rb") as f:
    data = f.read()

if mode == "encrypt":
    result = fernet.encrypt(data)

elif mode == "decrypt":
    result = fernet.decrypt(data)

with open(output_file, "wb") as f:
    f.write(result)

print("Opération réussie :", output_file)