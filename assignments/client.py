import socket
import time


class ClientError(Exception):
    pass


class ClientSocketError(ClientError):
    pass


class ClientProtocolError(ClientError):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientSocketError('error create connection', err)

    def _read(self):
        data = b''
        while not data.endswith(b'\n\n'):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientSocketError('error recv data', err)
        decoded_data = data.decode()
        status, payload = decoded_data.split('\n', 1)
        payload = payload.strip()
        if status == 'error':
            raise ClientProtocolError(payload)
        return payload

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        try:
            self.connection.sendall(f'put {key} {value} {timestamp}\n'.encode())
        except socket.error as err:
            raise ClientSocketError('error send data', err)
        self._read()

    def get(self, key):
        try:
            self.connection.sendall(f'get {key}\n'.encode())
        except socket.error as err:
            raise ClientSocketError('error send data', err)

        payload = self._read()

        data = {}
        if payload != '':
            for row in payload.split('\n'):
                key, value, timestamp = row.split()
                if key not in data:
                    data[key] = []
                data[key].append((int(timestamp), float(value)))

        return data

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientSocketError('error close connection', err)
