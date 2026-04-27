import os
import sys
from nacl.secret import SecretBox
from nacl.utils import random
from nacl.exceptions import CryptoError
import base64

def get_secretbox_key():
    key_b64 = os.getenv("SECRETBOX_KEY")

    if not key_b64:
        print("Erreur : variable d'environnement SECRETBOX_KEY absente.")
        sys.exit(1)

    return base64.b64decode(key_b64)

def encrypt_file(input_file, output_file):
    key = get_secretbox_key()
    box = SecretBox(key)

    with open(input_file, "rb") as file:
        data = file.read()

    nonce = random(SecretBox.NONCE_SIZE)
    encrypted = box.encrypt(data, nonce)

    with open(output_file, "wb") as file:
        file.write(encrypted)

    print(f"Fichier chiffré avec SecretBox : {output_file}")

def decrypt_file(input_file, output_file):
    key = get_secretbox_key()
    box = SecretBox(key)

    with open(input_file, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted = box.decrypt(encrypted_data)
    except CryptoError:
        print("Erreur : clé invalide ou fichier modifié.")
        sys.exit(1)

    with open(output_file, "wb") as file:
        file.write(decrypted)

    print(f"Fichier déchiffré avec SecretBox : {output_file}")

if len(sys.argv) != 4:
    print("Utilisation :")
    print("python app/secretbox_atelier2.py encrypt fichier_source fichier_sortie")
    print("python app/secretbox_atelier2.py decrypt fichier_chiffre fichier_sortie")
    sys.exit(1)

action = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

if action == "encrypt":
    encrypt_file(input_file, output_file)
elif action == "decrypt":
    decrypt_file(input_file, output_file)
else:
    print("Action inconnue. Utilisez encrypt ou decrypt.")