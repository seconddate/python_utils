"""
@author : seconddate
@date : 2020.08.03
"""
import zipfile
import os

class FileUtils:
    def __init__(self):
        pass
    
    def zip_file(self, file_path, zip_path):
        status = False

        try:
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                zip_file.write(file_path, os.path.basename(file_path))
                status = True

        except Exception as exception:
            print(str(exception))
            status = False
        
        return status

    def del_file(self, file_path):
        status = False

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                status = True
        except Exception as exception:
            print(str(exception))
            status = False
        
        return status
