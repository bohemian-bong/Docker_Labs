import docker

def get_container_id(container_name):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()
        
        # Get a list of all containers
        all_containers = client.containers.list(all=True)
        
        # Search for the container with the specified name
        for container in all_containers:
            if container.name == container_name:
                return container.id
        
        # If the container is not found
        print(f"Container '{container_name}' not found.")
        return None
    except Exception as e:
        print(f"Error retrieving container ID: {e}")
        return None

def is_container_running(container_id):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()
        
        # Get the container object by ID
        container = client.containers.get(container_id)
        
        # Check if the container is running
        return container.status == "running"
    except Exception as e:
        print(f"Error checking container status: {e}")
        return False

def get_container_id_from_script(container_id):
    try:
        # Connect to the Docker daemon
        client = docker.from_env()
        
        # Get the container object by ID
        container = client.containers.get(container_id)
        
        # Execute a command inside the container to run the script
        exec_id = container.exec_run(cmd='./home/script.sh')
        
        # Get the output of the script
        script_output = exec_id.output.decode('utf-8').strip()
        
        # Check if the output matches the container ID
        return script_output == container_id[0:12]
    except Exception as e:
        print(f"Error retrieving container ID from script: {e}")
        return False

# Container name to search for
container_name = "my_ubuntu_container"

# Get the container ID
container_id = get_container_id(container_name)
if container_id:
    
    # Check if the container is running
    if is_container_running(container_id):
        print("Container is running. ........ Checkpoint Completed (1/2)")
        
        # Check if the container ID obtained from the script matches the Docker API ID
        if get_container_id_from_script(container_id):
            print("Container ID matches. ........ Checkpoint Completed (2/2)")
        else:
            print("Container ID does not match. ........ Checkpoint Failed (1/2)")
    else:
        print("Container is not running. ........ Checkpoint Failed (0/2)")
else:
    print("Failed to retrieve container ID. ........ Checkpoint Failed (0/2)")
