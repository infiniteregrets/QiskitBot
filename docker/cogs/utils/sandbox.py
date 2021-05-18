import docker
from contextlib import contextmanager

client = docker.from_env()

class Sandbox():
    __slots__ = ('image', 'command', 'volume', 'remove', 'stderr', 'stdout', 'detach')
    def __init__(self, image, command, volume=None, 
                remove=True, stderr=True, stdout=True, detach=True):
        self.image = image 
        self.volume = volume
        self.command = command
        self.remove = remove
        self.stderr = stderr
        self.stdout = stdout 
        self.detach = detach

    def run(self):
        output = client.containers.run(
                    image=self.image,
                    volumes=self.volume, 
                    command=self.command,
                    stderr=self.stderr,
                    stdout=self.stderr,
                    remove=self.remove
                )
        return output


# sandbox = Sandbox('qiskitsandbox', '/bin/sh -c "ls"')
# out = sandbox.run()
# print(out)