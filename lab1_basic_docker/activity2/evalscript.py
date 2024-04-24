import docker
import psutil

def parse_container_name(containers, target_name):
    for container in containers:
        if container.name == target_name:
            return container.name
    return None

def get_container_cpu_cores(container):
    try:
        cpu_count = psutil.cpu_count(logical=False)
        return cpu_count
    except Exception as e:
        print(f"Error retrieving CPU cores: {e}")
        return None

def extract_cpu_cores_from_file(filename):
    try:
        with open(filename, 'r') as file:
            line = file.readline().strip()  # Read the first line and remove leading/trailing whitespace
            cpu_cores = int(line.split(':')[1])  # Split the line at ':' and extract the second part
            return cpu_cores
    except Exception as e:
        print(f"Error extracting CPU cores from file: {e} ........ Checkpoint Failed (1/2)")
        return None

def main():
    # Connect to the Docker daemon
    client = docker.from_env()
    
    # Get a list of all containers
    all_containers = client.containers.list(all=True)
    
    # Parse the container name
    target_name = "my_ubuntu_container"
    parsed_name = parse_container_name(all_containers, target_name)
    
    if parsed_name:
        print(f"Container '{parsed_name}' found! ........ Checkpoint Completed (1/2)")
        
        # Get CPU information within the container
        container = client.containers.get(parsed_name)
        container_cpu_cores_from_file = extract_cpu_cores_from_file("file.txt")  # Read the value from the file
        
        container_cpu_cores_from_docker = get_container_cpu_cores(container)
        
        if container_cpu_cores_from_docker is not None:
            
            if container_cpu_cores_from_file == container_cpu_cores_from_docker:
                print("Number of CPU cores matches! ........ Checkpoint Completed (2/2)")
            else:
                print("Number of CPU cores does not match! ........ Checkpoint Failed (1/2)")
        else:
            print("Failed to retrieve CPU core information for the container from the Docker API. ......... Checkpoint Failed (0/2)")
    else:
        print(f"Container '{target_name}' not found. ........ Checkpoint Failed (0/2)")

if __name__ == "__main__":
    main()

