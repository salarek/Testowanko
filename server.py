  
import socket
import select
import time
import pickle
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#PORT = int(os.environ(['$PORT']))
s.bind(("0.0.0.0", 8080))
s.listen()
s_list = [s]
clients = {}


def rec_message(client_socket):
    try:
        msg = client_socket.recv(2048)
        msgs = pickle.loads(msg)
        return msgs

    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(s_list, [], s_list)
    for soc in read_sockets:
        if soc == s:
            client_socket, client_address = s.accept()
            print(f"Connected to server")
            user = rec_message(client_socket)
            #if user is False:
               # continue
            s_list.append(client_socket)
            clients[client_socket] = user
            
        else:
            msg = rec_message(soc)
            #msgz = pickle.dumps(msg)
            if msg is False:
                print("Ending Communication")
                s_list.remove(soc)
                del clients[soc]
            
                continue
            user = clients[soc]
            print(f'res message')
            print(msg)
        
            for client_socket in clients:
                if client_socket != soc:
                    client_socket.send(bytes(msg, "utf-8"))
    for soc in exception_sockets:
        s_list.remove(soc)
        del clients[soc]
        
        

        