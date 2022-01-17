import protocol
import sqlite3
import socket

class server(object):
    def __init__(self, SERVER_PORT=1002):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(("0.0.0.0", SERVER_PORT))
        self.soc.listen(4)
        print("Server is up and running\n")

    def get_operators(self):
        """
        gets clients
        """

        while True:
            operator_socket, sever_address = self.soc.accept()
            print("\noperator Connected\n")

            self.get_database(operator_socket)



    def get_database(self, connectionto):
        """the function prints user's data according to the given ID"""
        conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        str1 = "select * from python_quiz;"

        # strsql = "SELECT userId, username, password, email, phone_number from " + self._tablename + " where " + self._userId + "=" + str(
        # userId)

        print(str1)
        questions_data = []

        cursor = conn.execute(str1)
        for row in cursor:
            data = []
            print("questionID = ", row[0])
            data.append(row[0])
            print("Q1 = ", row[1])
            data.append(row[1])
            print("Ans1 = ", row[2])
            data.append(row[2])
            print("Ans2= ", row[3])
            data.append(row[3])
            print("Ans3 =", row[4])
            data.append(row[4])
            print("Ans4 =", row[5])
            data.append(row[5])
            print("AnsCorrect =", row[6])
            data.append(row[6])
            questions_data.append(data)

        print("Operation done successfully")
        protocol.build_send_recv_parse(conn, "GET_GAME", questions_data)
        conn.close()



def main():
    """ Main function """
    my_server = server()
    my_server.get_operators()

    #my_server.select_user_by_id()


if __name__ == '__main__':
    main()

