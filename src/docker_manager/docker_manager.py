import docker

class DockerManager:
    """
    Manages interactions with the Docker daemon.
    """
    def __init__(self):
        """
        Initializes the Docker client.
        """
        self.client = docker.from_env()

    def list_containers(self):
        """
        Returns a list of all running containers.
        """
        return self.client.containers.list()

    def stop_container(self, container_id):
        """
        Stops a specific Docker container.

        Args:
            container_id (str): The ID or name of the container to stop.
        """
        container = self.client.containers.get(container_id)
        container.stop()