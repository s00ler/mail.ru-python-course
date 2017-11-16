from os import path
from tempfile import gettempdir


class File:
    def __init__(self, file_name):
        self.file_name = file_name

    def __str__(self):
        return self.file_name

    def write(self, line):
        with open(self.file_name, 'a') as f:
            f.write(line)

    def __iter__(self):
        return open(self.file_name, 'r')

    def __add__(self, other):
        temp_path = path.join(gettempdir(), 'new_file.txt')
        with open(self.file_name, 'r') as sf,\
                open(other.file_name, 'r') as of,\
                open(temp_path, 'w') as nf:
            nf.write(sf.read())
            nf.write(of.read())
        return File(temp_path)
