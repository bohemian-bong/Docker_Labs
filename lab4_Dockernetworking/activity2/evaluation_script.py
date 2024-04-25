import socket
import docker
import subprocess
import json

def check_connection(ip, port):
    try:
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # Timeout for connection attempt (2 seconds)

        # Attempt to connect to the IP and port
        s.connect((ip, int(port)))

        # If connection succeeds, print success message
        print(f"Connection to {ip}:{port} successful")
        return True

    except Exception as e:
        # If connection fails, print error message
        print(f"Failed to connect to {ip}:{port}: {e}")
        return False

def check_docker_compose_running():
    try:
        # Execute the command to list running containers and their labels
        result = subprocess.run(['docker', 'ps', '--format', '{{json .}}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

        # Check if the command was successful (exit code 0)
        if result.returncode == 0:
            containers_info = result.stdout.decode('utf-8').splitlines()
            for container_info in containers_info:
                container = json.loads(container_info)
                labels = container.get('Labels', {})
                if 'com.docker.compose.project' in labels:
                    print("Running containers were created with Docker Compose")
                    return True

            print("No containers created with Docker Compose found")
        else:
            print("Failed to list containers")
        return False

    except FileNotFoundError:
        print("Docker not found or not installed")
        return False

def check_containers_running():
    try:
        # Initialize Docker client
        client = docker.from_env()

        # Check if the containers are running
        containers_running = True
        for container_name in ['activity2-mongodb-container-1', 'activity2-server-container-1', 'activity2-client-container-1']:
            container = client.containers.get(container_name)
            if container.status != 'running':
                print(f"Container '{container_name}' is not running")
                containers_running = False

        if containers_running:
            print("All containers are running")
            return True
        else:
            print("Not all containers are running")
            return False

    except docker.errors.NotFound as e:
        print(f"Error: {e}. Check if Docker is installed and running.")
        return False

def main():
    # Read IPs and ports from file
    print("Checking if Docker Compose is running...")
    if check_docker_compose_running():
        print("Checking if containers are running...")
        if check_containers_running():
        
            with open('file.txt', 'r') as f:
                lines = f.readlines()
                database_ip = lines[0].split(":")[1].strip()
                database_port = lines[1].split(":")[1].strip()
                server_ip = lines[2].split(":")[1].strip()
                server_port = lines[3].split(":")[1].strip()
                client_ip = lines[4].split(":")[1].strip()
                client_port = lines[5].split(":")[1].strip()

            # Check connections for database, server, and client
            print("\nVerifying Database connection:")
            db_connection_status = check_connection(database_ip, database_port)

            print("\nVerifying Server connection:")
            server_connection_status = check_connection(server_ip, server_port)

            print("\nVerifying Client connection:")
            client_connection_status = check_connection(client_ip, client_port)

            # Return connection statuses
            return db_connection_status, server_connection_status, client_connection_status

if __name__ == "__main__":
    main()
