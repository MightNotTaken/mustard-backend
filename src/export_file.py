import os
import shutil

class ExportComponent:
    total = 0
    paths = []

    def load(self):
        try:
            self.reset()
            files = os.listdir(os.path.join(os.path.dirname(__file__), './../database'))
            if files:
                self.total = len(files)
                self.paths = files
            return self.total
        except OSError as error:
            return error

    def get_total(self):
        return self.total

    def reset(self):
        self.total = 0
        self.paths = []

    def get_destination_path(self):
        if os.name == 'nt':
            return os.path.abspath(os.path.join(os.path.dirname(__file__), './../output'))
        elif os.name == 'posix':
            drives = os.listdir('/media/nvidia')
            if drives:
                return os.path.join('/media/nvidia', drives[-1])
            else:
                return None

    def export(self, id):
        try:
            print('path: ', self.get_destination_path())
            source_path = os.path.join(os.path.dirname(__file__), './../database', self.paths[id])
            destination_path = os.path.join(self.get_destination_path(), self.paths[id])
            if os.name == 'nt':
                shutil.copyfile(source_path, destination_path)
            elif os.name == 'posix':
                shutil.copyfile(source_path, destination_path)
            return True
        except OSError as error:
            print(error)
            return False

