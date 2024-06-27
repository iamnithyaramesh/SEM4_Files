import socket

def client_pgm():
    host=socket.gethostname()
    port=5000

    client_socket=socket.socket()
    client_socket.connect((host,port))

    msg=input('client:')

    while msg!='bye':
        client_socket.send(msg.encode())
        data=client_socket.recv(1024).decode()
        print(('Received data:',data))
        msg=input('client:')
    client_socket.close()

if __name__=='__main__':
    client_pgm()
