from receiver import Receiver
from sender import Sender

def create_upload_keys(ip):
    #Simulation of the key generation process (The public key is sent through the network)
    key_generator = Receiver(generation=True)
    print(f"public key: {key_generator.public_key}, private key: {key_generator.private_key}")#Write them down
    with open("public.txt","w") as f:
        f.write(str(key_generator.public_key))
    with open("private.txt","w") as f:
        f.write(str(key_generator.private_key))
    send = Sender(key_generator.public_key)
    send.send_file(ip,"test","test","public.txt","/cripto")
    return key_generator.public_key, key_generator.private_key

def download_ciphered_file(public_key, private_key):
    obtained_public_key = public_key
    obtained_private_key = private_key
    # The receiver now gets the encrypted file and proceeds to obtain the plaintext
    new_receiver = Receiver(public_key=obtained_public_key, private_key=obtained_private_key)
    new_receiver.download_file_ftp("192.168.137.1", "test", "test", "/cripto", "output_prueba.pdf")
    new_receiver.decrypt_file("output_prueba.pdf")

def main():
    while True:
        opcion=int(input("Digite la opción: \n"
                     "1. Crear llaves\n"
                     "2. Desencriptar archivo\n"
                     "3. Salir \n"))
        if opcion==1:
            try:
                public,private=create_upload_keys(input("Digite la ip \n"))
                print("Archivo con llave pública subido satisfactoriamente!")
            except: print("Ha habido un error al subir el archivo")
        elif opcion==2:
            try:
                download_ciphered_file(public, private)
                print("Archivo descargado y desencriptado con éxito")
            except: print("Algo salió mal")
        else:
            print("Adiós")
            break

main()