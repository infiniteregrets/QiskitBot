import subprocess 
import logging
import os 
import pickle
import threading 
import sys 
import uuid
from collections import Counter 
import stat


node_type = stat.S_IRUSR 
mode = 0o600 | node_type    

container_map = Counter()
@spawn_thread
def update_map():
    if os.path.exists(f'{str(os.getcwd())}/container_map.pickle'):
        with open('container_map.pickle', 'rb') as cmap:
            if os.stat(f'{str(os.getcwd())}/container_map.pickle').st_size == 0:
                return 
            else:
                container_map = pickle.load(cmap)
                print(container_map)
    else:
        if sys.platform == 'darwin':
            open(f'{str(os.getcwd())}/container_map.pickle', 'w+').close()
        else:
            os.mknod(f'{str(os.getcwd())}/container_map.pickle', mode)

handle = update_map()        


    
class Sandbox:
    def __init__(self, user_id = None, image_id = None):
        logging.basicConfig(filename='loginfo.log', 
                            filemode='w', 
                            level=logging.INFO)        
        self.logger = logging.getLogger(__name__)        
        self.retries = 1
        self.container_name = str(uuid.uuid4())  
        handle.join()      
        global container_map
        self.container_map = container_map        

        if user_id == None or image_id == None:
            print("User ID/Image ID not specified | Aborting ")
            return 
        else:                         
            for i in range(3):   
                try:         
                    container = subprocess.run(f'podman run --name="{self.container_name}"  -i -t -d {image_id}',
                                                capture_output = True, 
                                                text = True,
                                                check = True,
                                                shell = True)                                            
                    self.logger.info(f'Container created successfully | Container Name : {user_id}')                    
                    self.container_map[f'{user_id}'] = self.container_name                                                          
                    with open('container_map.pickle','wb') as cmap:
                        pickle.dump(container_map, cmap)   
                    
                    break                                                
                except Exception as e:
                    print(e)
                    self.retries += 1                    
                    print(f'Error occured while creating a container for {user_id} | retry number -- {self.retries}')                                            
                    self.logger.error(f'Error occured while creating a container for {user_id} | retry number -- {self.retries}')

                if self.retries == 3:
                    self.logger.error(f'Aborting | Could not run container | User ID -- {user_id}')
                    sys.exit("Aborting | Could not run container")             

        print(dict(self.container_map))

    def kill_all(self):
        subprocess.run('podman kill $(podman ps -q)', shell = True)


