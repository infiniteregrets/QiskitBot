from index import Qiskit
import config

client = Qiskit()
client.run(config.TOKEN, reconnect = True, bot = True)