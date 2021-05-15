import subprocess 
import logging
import os 
import sys 
from contextlib import contextmanager

    
class Image():
    def __init__(self, tag):
        self.tag = tag
        logging.basicConfig(filename='loginfo.log', 
                            filemode='w', 
                            level=logging.INFO)        
        self.logger = logging.getLogger(__name__)
        self.path = os.getcwd()
        self.image = self.build_image(self.path)
     
        self.sandbox_path = None
        self.image_id = None
        self.image_exists = False

        if self.image != 0:            
            print("Unable to create new image")
            self.logger.critical("Unable to create new image")
   
    def build_image(self, path):
        image = None
        process = subprocess.run(['podman', 'image', 'ls', '-aq'],                         
                                    capture_output = True, 
                                    text = True)
        if process.stdout == "":
            self.logger.warning("Image not built | Building Image now")
            print(self.path)
            self.sandbox_path = str(path) + '/sandbox/'
            with self._temp_path(self.sandbox_path):        
                try:
                    image = subprocess.run(f'podman build --cgroup-manager="cgroupfs" -t {self.tag} - < Dockerfile', 
                                            shell = True, 
                                            text = True,
                                            check = True)
                except Exception as e:                
                    self.logger.critical("Dockerfile Not found | Aborting")
                    sys.exit(f"Error: Dockerfile Not found | {e}")                                 

            self.logger.info("Building Image")

            if image.returncode == 0:
                print('Successfuly created new image.')
                self.logger.info('Successfuly created new image.')
                self.image_exists = True 
                self.image_id = subprocess.run(['podman', 'image', 'ls', '-aq'],                         
                                                    capture_output = True, 
                                                    text = True)
                return image.returncode
        else:
            self.image_exists = True
            self.image_id = process.stdout 
            print("Image already exists.")                
        return process.returncode

    def __delete__(self):
        del_image = subprocess.run(f"podman image rm {self.tag}", 
                                    shell = True, 
                                    capture_output = True, 
                                    text = True)
        if del_image.returncode != 0:
            print(del_image.stderr)
        else:
            print(del_image.stdout)
        return del_image.returncode
        
        

    @property
    def get_image_id(self):
        if self.image_exists:                
            return self._fetch()
        else:
            self.logger.error("Tried fetching ID for an image, but the image does not exist")
            print("Error | Image not found")
            print("Building Image ...")
            self.build_image()
            return self._fetch()
         
    def _fetch(self):
        image_id = subprocess.run('podman image ls -aq', 
                                        shell = True, 
                                        capture_output = True)
        return image_id
    @contextmanager
    def _temp_path(self, path):
        owd = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(owd)   

     