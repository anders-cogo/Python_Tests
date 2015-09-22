#Anders Simpson-Wolf
#09/21/2015
#Learning the Cryptography and PyCrypto libraries

#This is from the cryptography example
from cryptography.fernet  import Fernet
#this is from the pycrypto example
from Crypto.Cipher import AES

#this is the cryptography example
key = Fernet.generate_key()
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(b"A really secret message.  Not for prying eyes.")
plain_text = cipher_suite.decrypt(cipher_text)

print cipher_text
print plain_text

#this is the pycrypto example
encryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
cipher_text2 = encryption_suite.encrypt("A super secret message.   Not for you to see! 16")
decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
plain_text2 = decryption_suite.decrypt(cipher_text2)

print cipher_text2
print plain_text2
