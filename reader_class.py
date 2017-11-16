class FileReader:
    def __init__(self, file_path):
        self.file = file_path

    def read(self):
        try:
            with open(self.file) as f:
                result = f.read()
        except FileNotFoundError:
            result = ''
        return result
