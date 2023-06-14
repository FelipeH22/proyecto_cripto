from receiver import Receiver
from sender import Sender

"""#Simulation of the key generation process (The public key is sent through the network)
key_generator = Receiver(generation=True)
print(f"public key: {key_generator.public_key}, private key: {key_generator.private_key}")#Write them down."""

# Copied from the output of executing the commented code. In order to generate new keys, comment all of the following code
obtained_public_key = (170141183460469231731687303715884105727, 143357556492107834470408574398200905821,
                       169221117335223310231454551865032910444)
obtained_private_key = 28482089847786382337691267341681422122

# With the public key, the file is encrypted by the sender
new_sender = Sender(obtained_public_key)
cipher = new_sender.file_encryption(new_sender.read_pdf("prueba.pdf"))
new_sender.export_encrypted_file(cipher, with_password=False)

# The receiver now gets the encrypted file and proceeds to obtain the plaintext
new_receiver = Receiver(public_key=obtained_public_key, private_key=obtained_private_key)
new_receiver.decrypt_file("output.pdf")
