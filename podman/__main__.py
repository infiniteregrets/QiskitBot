from index import Qiskit
import config
from podman_image import Image
import os 

image = Image(config.IMAGE)    

client = Qiskit()
client.run(config.TOKEN, reconnect = True, bot = True)