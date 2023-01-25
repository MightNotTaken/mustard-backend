import os
import shutil
from time import sleep
import subprocess

class ExportComponent:
    total = 0
    paths = []

    def __init__(self):
            self.mount_points = ['/media/nvidia/pd1', '/media/nvidia/pd2', '/media/nvidia/pd3', '/media/nvidia/pd4']
            self.flashs = []
            for point in self.mount_points:
                try:
                    os.system(f'sudo mkdir {point}')
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

    def get_mountable_drive(self):
        self.flashs = []
        for dir in os.listdir('/dev'):
            if dir.count('sd'):
                self.flashs.append(f'/dev/${dir}')
        return self.flashs
        
    def mount(self):
        try:
            flash_drives = self.get_mountable_drive()
            for i in range(len(flash_drives)):
                print('mounting', flash_drives[i], 'at', self.mount_points[i])
                subprocess.run(['sudo', 'mount', flash_drives[i], self.mount_points[i]])
                sleep(1)
        except Exception as e:
            print(e)
            pass



    def get_destination_path(self, index):
        return self.mount_points[index]


    def export(self, id):
        try:
            source_path = os.path.join(os.path.dirname(__file__), './../database', self.paths[id])
            flash_drives = self.get_mountable_drive()
            for i in range(len(flash_drives)):
                try:
                    destination_path = os.path.join(self.get_destination_path(i), self.paths[id])
                    if os.name == 'nt':
                        shutil.copyfile(source_path, destination_path)
                    elif os.name == 'posix':
                        shutil.copyfile(source_path, destination_path)
                except:
                    pass
            return True
        except OSError as error:
            print(error)
            return False

