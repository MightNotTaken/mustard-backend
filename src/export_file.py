import os
import shutil
import subprocess

class ExportComponent:
    total = 0
    paths = []

    def __init__(selff):
        try:
            if os.name == 'posix':
                self.mount_point = '/media/nvidia/pendrive'
                os.system(f'sudo mkdir {self.mount_point}')
        except:
            pass

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

    def get_mountable_drive():
        for dir in os.listdir('/dev'):
            if dir.count('sd'):
                return f'/dev/${dir}'
        return None
        
    def mount(self):
        try:
            flash_drive = self.get_mountable_drive()
            if flash_drive and not os.path.ismount(self.mount_point):
                subprocess.run(['sudo', 'mount', flash_drive, self.mount_point])
        except:
            pass



    def get_destination_path(self):
        if os.name == 'nt':
            return os.path.abspath(os.path.join(os.path.dirname(__file__), './../output'))
        elif os.name == 'posix':
            return self.mount_point


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

