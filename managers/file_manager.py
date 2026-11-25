"""Low-level text file access."""

class FileManager:
    """Reads and writes a single text file."""

    def __init__(self, filename):
        """Stores the name of the file to manage."""
        self.filename = filename

    def read_file(self):
        """Returns the file content. Creates an empty file if it does not exist."""
        try:
            with open(self.filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                return ""

    def read_lines(self):
        """Yields the file lines one by one."""
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    yield line.strip()
        except FileNotFoundError:
            return

    def append_file(self, content):
        """Adds content to the end of the file."""
        with open(self.filename, 'a') as file:
            file.write(content)

    def write_file(self, content):
        """Replaces the file content."""
        with open(self.filename, 'w') as file:
            file.write(content)