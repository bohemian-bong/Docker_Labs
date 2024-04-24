import os
import requests

# Function to check if Docker image exists
def check_image_exists(image_name):
    images = os.popen("docker images --format '{{.Repository}}'").read().splitlines()
    return image_name in images

# Function to check if Docker container is running
def check_container_running(container_name):
    containers = os.popen("docker ps --format '{{.Names}}'").read().splitlines()
    return container_name in containers

# Function to parse file.txt and extract host, port, and flag
def parse_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        host = None
        port = None
        flag = None

        for line in lines:
            if line.startswith('HOST'):
                port = int(line.split('=')[1].strip())
            elif line.startswith('FLAG'):
                flag = line.split('=')[1].strip()
        return host, port, flag

# Function to make HTTP request and verify flag
def verify_flag(host, port, flag):
    url = f"http://localhost:{port}"
    response = requests.get(url)
    if response.status_code == 200 and response.text.strip() == flag:
        return True
    return False

# Main function to evaluate the lab
def evaluate_lab():
    image_name = "my_flask_server"
    container_name = "my_server_container"
    filename = "file.txt"

    if not check_image_exists(image_name):
        print("Docker image not found. .......... Checkpoint Failed (0/3)")
        return
    else:
        print("Docker image exists. ......... Checkpoint Completed (1/3)")
    
    if not check_container_running(container_name):
        print(f"Docker container is not running. ......... Checkpoint Failed (1/3)")
        return
    else:
        print("Docker container is running. .......... Checkpoint Completed (2/3)")
    
    host, port, flag = parse_file(filename)
    if not port or not flag:
        print("Error: Invalid format in file.txt.")
        return
    
    if verify_flag(host, port, flag):
        print("Flag verification successful! ......... Checkpoint Completed (3/3)")
    else:
        print("Error: Flag verification failed. ......... Checkpoint Failed (2/3)")

if __name__ == "__main__":
    evaluate_lab()

