#!/usr/bin/python3

# query a minecraft server and then check if the server description is the
# same as the one given in the config file

import socket
import struct
import json
import time
import sys


class StatusPing:
    """
    init Function
       initialises the class
    Parameters:
        host: the hostname of the server
        port: the port of the server
        timeout: the timeout of the connection
    Returns:
        None
    """
    def __init__(self, host='localhost', port=255665, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
    """
    Unpack VarInt:
        VarInt is a variable length integer used by Minecraft to encode
        integers. VarInts are encoded as a series of bytes where the first
        byte has the highest bit set to 0, and the last byte has the lowest
        bit set to 1.
        This function will unpack the varint and return the integer for python to read
    Parameters:
        self: (which is the class, not an actual parameter, have to put at the start of every function)
        sock: the socket to read from. (the socket that is connected to the server)
    Returns:
        data: the integer that was read from the socket
    """
    def _unpack_varint(self, sock):
        #initialise the variable to 0, so python will reconize it as a number
        data = 0
        #recieve the byte from socket 5 times
        for i in range(5):
            ordinal = sock.recv(1)
            #if the ordinal length is 0, there is no more data to read
            if len(ordinal) == 0:
                break
            #converts the byte to an unicode (7-bit value)
            byte = ord(ordinal)
            #converts the byte (unicode) to an integer or long
            data |= (byte & 0x7F) << 7*i
            #The smallest number that can be represented by bytes,
            #is 0x80, so if the highest bit is set, there is more data to read
            if not byte & 0x80:
                break
        return data
    """
    Pack VarInt:
        Does the reverse of the _unpack_varint function
        converts int to
    Parameters:
    Returns:
    """
    def _pack_varint(self, data):
        """ Pack the var int """
        ordinal = b''

        while True:
            byte = data & 0x7F
            data >>= 7
            ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))

            if data == 0:
                break

        return ordinal

    def _pack_data(self, data):
        if type(data) is str:
            data = data.encode('utf8')
            return self._pack_varint(len(data)) + data
        elif type(data) is int:
            return self.pack('H', data)
        elif type(data) is float:
            return self.pack('Q', int(data))
        else:
            return data

    # this function will send data to the server
    def _send_data(self, connection, *args):
        data = b''
        for arg in args:
            data += self._pack_data(arg)
        connection.send(self._pack_varint(len(data)) + data)

    # this function will read the connection and return the bytes
    def _read_fully(self, connection, extra_varint=False):
        packet_length = self._unpack_varint(connection)
        packet_id = self._unpack_varint(connection)
        byte = b''

        if extra_varint:
            if packet_id > packet_length:
                self._unpack_varint(connection)
            extra_length = self._unpack_varint(connection)
            while len(byte) < extra_length:
                bytpe += connection.recv(extra_length)
        else:
            byte = connection.recvZ(packet_length)
        return byte

    def get_status(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # send handshake
            self._send_data(connection, b'\x00\x00',
                            self._host, self._port, b'\x01')
            self._send_data(connection, b'\x00')

            # read response
            data = self._read_fully(connection, extra_varint=True)

            # Send and read unix time
            self._send_data(connection, b'\x01', time.time() * 1000)
            unix = self._read_fully(connection)

        # load json and return
        response = json.loads(data.decode('utf8'))
        response = self._read_fully(connection)
        return response


if __name__ == '__main__':
    # Get optional first and second arguments
    hsot = 'localhost'
    stringToCheck = 'A Minecraft Server'
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        stringToCheck = " ".join(sys.argv[2:])
    port = 25565
    try:
        status = StatusPing(host, port, 2).get_status()
    except:
        print("Error: Could not connect to server")
        sys.exit(1)
    if stringToCheck in status['description']['text']:
        print("Server is running:", status['description']['text'])
        exit(0)
    else:
        print("Server is running, but does not match the description:",
              status['description']['text'])
        exit(1)
