import protocol
import socket
import threading
import time
import random

class operator(object):
    def __init__(self, server_address):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(server_address)
        print("connection succeed")
    def request_data(self):
        database_trivia = protocol.recv_message_and_parse(self.soc)
        print(database_trivia)


    def start(self):
        try:
           print('server starts up on ip %s port %s' % (self.ip, self.port))
           # Create a TCP/IP socket
           sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           sock.bind((self.ip, self.port))
           sock.listen(3)

           while True:
                print('waiting for a new client')

                clientSocket, client_address = sock.accept() # block

                print('new client entered')

                # send receive example
                clientSocket.sendall('Hello this is server'.encode())
                msg = clientSocket.recv(1024)
                print('received message: %s' % msg.decode())
                self.count += 1
                print(self.count)
                # implement here your main logic
                self.handleClient(clientSocket, self.count)
        except socket.error as e:
            print(e)
    def handleClient(self, clientSock, current):
        print ("hello")
        client_handler = threading.Thread(target=self.handle_client_connection, args=(clientSock, current,))
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        client_handler.start()

    def table(self, num):
        st = ""
        for i in range(1, num + 1):
            for j in range(1, num + 1):
                st += str(i * j) + " "
            st += "\n"
        return st

    def instruction(elsf):
        """
        The Function Will Send The Client All The Available Commands
        :rtype: string
        :return: All the instructions
        """
        instructions = "Help -> Shows You This Message\n"
        instructions += "Name ___ -> Welcome Message\n"
        instructions += "Rand -> Your Grade :)\n"
        instructions += "Input A Number 1-10 -> Multiplication Table\n"
        instructions += "Time -> Get The Exact Time\n"
        return instructions

    def handle_client_connection(self, client_socket, current):
        print("strat")
        while True:
            request = client_socket.recv(1024).decode()
            if request == 'Help':
                output = self.instruction()
            elif request[:4] == 'Name':
                output = "Ahalan " + request[5:] + " Nice To Meet You"
            elif request == 'Time':
                output = time.asctime(time.localtime(time.time()))
            elif request == 'Rand':
                output = str(random.randint(0, 100))
            elif request.isdigit():
                output = self.table(int(request))
            else:
                output = 'Unknown Command, Please Type Again'
            client_socket.sendall(output.encode())


if __name__ == '__main__':
    server_adress = ("127.0.0.1", 1002)
    my_operator = operator(server_adress)
    my_operator.request_data(server_adress)

