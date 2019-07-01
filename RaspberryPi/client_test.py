from time import sleep

from socket_client_class import *

def main ():
    sc = socket_client()
    sc.connect()
    id = sc.getID()
    print(id)

    while True:

        data = "Hello World!"
        server_reply = sc.send(str.encode(data))
        print(server_reply)

main()