#Daniel Tov
#10.12.2021
#protocol.py

import sqlite3

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT_OPERATOR = {
    "login_msg": "LOGIN",
    "send_ans_msg": "SEND_ANSWER",

}
PROTOCOL_OPERATOR_CLIENT = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR",
    "correct_msg": "CORRECT_ANSWER",
    "wrong_msg": "WRONG_ANSWER"

}
PROTOCOL_SERVER_OPERATOR = {
    "game_data": "YOUR_GAME"

}
PROTOCOL_OPERATOR_SERVER = {
    "my_game": "GET_GAME"

}
# Other constants

ERROR_RETURN = None  # What is returned in case of an error

def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    if len(cmd) <= CMD_FIELD_LENGTH and len(data) <= MAX_DATA_LENGTH:
        full_msg = cmd
        full_msg = full_msg.ljust(CMD_FIELD_LENGTH, ' ')
        length = str(len(data)).zfill(LENGTH_FIELD_LENGTH)
        full_msg += DELIMITER + length + DELIMITER + data
        return full_msg

    return None

def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    data = data.split(DELIMITER)
    cmd = data[0].replace(" ", '')
    len_msg = data[1].replace(" ", '')
    len_msg = int(len_msg)
    msg = data[2]
    if len_msg != len(msg) or len(cmd) > CMD_FIELD_LENGTH or len(msg) > MAX_DATA_LENGTH or len(
            data[1]) > LENGTH_FIELD_LENGTH:
        return None, None
    return cmd, msg

def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    lst = []
    count = 0
    st = ""
    for x in msg:
        if x != DATA_DELIMITER:
            st = st + x
        else:
            count = count + 1
            lst.append(st)
            st = ""
    if count == expected_fields:
        return lst
    else:
        return None

def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like cell1#cell2#cell3
    """
    st = ""
    for x in range(len(msg_fields)-1):
        st = st+msg_fields[x]+DATA_DELIMITER
    st = st+msg_fields[x+1]
    return st

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    full_msg = build_message(code, data)
    if full_msg is not None:
        conn.send(full_msg.encode())
    else:
        error_and_exit("Error!")

def error_and_exit(error_msg):
    """
    The function prints the error message .
    Recieves: msg error
    Returns: None
    """
    print(error_msg)
    exit()

def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """

    full_msg = conn.recv(MAX_MSG_LENGTH).decode()
    cmd, data = parse_message(full_msg)

    return cmd, data


def build_send_recv_parse(socket, cmd, data):
    """
    Builds a new message using chatlib and Recieves a new message from given socket.
    Recieves: socket, cmd, data
    Returns: msg_code, data
    """
    build_and_send_message(socket, cmd, data)
    msg_code, data = recv_message_and_parse(socket)
    return msg_code, data
