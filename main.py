import socket
import threading

import rsa

public_key, private_key = rsa.newkeys(1024)
pkey_partner = None


choice = input('Do you want to host (1) or to connect (2): ')

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.43.211", 9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1('PEM'))
    pkey_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.43.211", 9999))
    pkey_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1('PEM'))

else:
    exit()


def send_msg(c):
    while True:
        message = input('')
        c.send(rsa.encrypt(message.encode(), pkey_partner))

        print("You :" + message)


def receive_msg(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())


threading.Thread(target=send_msg, args=(client, )).start()
threading.Thread(target=receive_msg, args=(client, )).start()
