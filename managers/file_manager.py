class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        try:
            with open(self.filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                return ""

    def write_file(self, content):
        with open(self.filename, 'w') as file:
            file.write(content)