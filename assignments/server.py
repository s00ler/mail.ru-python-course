import asyncio
import sys


class Storage:
    _data = {}

    @classmethod
    def put(cls, key, value, timestamp):
        metric = cls._data.get(key, {})
        metric.update({timestamp: value})
        cls._data[key] = metric

    @classmethod
    def get(cls, key):
        result = ''
        if key == '*':
            for metric in cls._data.keys():
                result += cls._form_result(metric)
        else:
            result += cls._form_result(key)
        return result

    @classmethod
    def _form_result(cls, key):
        result = ''
        for timestamp, value in cls._data.get(key, {}).items():
            result += f'{key} {value} {timestamp}\n'
        return result


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        response = ClientServerProtocol.process_data(data.decode())
        print(response)
        self.transport.write(response.encode())

    @staticmethod
    def process_data(data):
        data = data.split('\n')[0].split(' ')
        # data = data.split('\n')[-1].split(' ')
        print(data)

        status = 'ok'
        response = ''
        if ((data[0] == 'put' and len(data) != 4)
            or (data[0] == 'get' and len(data) != 2)
                or data[0] not in ['put', 'get']):
            status = 'error\nwrong command'
        else:
            if data[0] == 'put':
                Storage.put(data[1], float(data[2]), int(data[3]))
            if data[0] == 'get':
                response = str(Storage.get(data[1]))
        return '\n'.join([status, response]) + '\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    listener = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(listener)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    run_server(sys.argv[1], int(sys.argv[2]))
