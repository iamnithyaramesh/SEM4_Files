import socket

def server():
    host=socket.gethostname()
    port=5000

    server=socket.socket()
    server.bind(host,port)
    server.listen(2)
    conn,address=server.accept()
    print(str(address))

    while True:
        data=conn.recv(1024).decode()
        if not data:
            break
        data=input('Server:')
        conn.send(data.encode())
    conn.close()



def client():
    client=socket.socket()
    client.connect(socket.gethostname(),5000)
    msg=input("Client")
    while msg!='bye':
        client.send(msg.encode())
        data=client.recv(1024).decode()
        print(data)
        msg=input("Client")
    client.close()

     