import docker
import subprocess

def check_docker_network(network_name):
    try:
        client = docker.from_env()
        network = client.networks.get(network_name)
        return True
    except docker.errors.NotFound:
        return False
    except docker.errors.APIError as e:
        print(f"Error occurred: {e}")
        return False

def check_containers_in_network(network_name, container_names):
    try:
        client = docker.from_env()
        network = client.networks.get(network_name)
        container_ids = [container.id for container in client.containers.list()]
        for container_id in container_ids:
            container = client.containers.get(container_id)
            if container.name in container_names and network_name in container.attrs['NetworkSettings']['Networks']:
                return True
        return False
    except docker.errors.APIError as e:
        print(f"Error occurred: {e}")
        return False


def check_container_ips(file_path):
    try:
        with open(file_path, 'r') as file:
            container_ips = {}
            for line in file:
                name, ip = line.strip().split('=')
                container_ips[name.strip()] = ip.strip()

            # Check if IPs match
            for name, ip in container_ips.items():
                command = f"docker exec {name} ifconfig eth0 | grep 'inet ' | awk '{{print $2}}' | cut -d':' -f2"
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, _ = process.communicate()
                container_ip = stdout.decode().strip()
                if not container_ip == ip:
                    return False
            return True
    except Exception as e:
        print(f"Error occurred while checking container IPs: {e}")
        return False

if check_docker_network("my_network_1"):
    print(f"The Docker network my_network_1 is present ...... Checkpoint Completed(1/5)")
    if check_docker_network("my_network_2"):
        print(f"The Docker network my_network_2 is present ...... Checkpoint Completed(2/5)")
        container_names1 = ["container1", "container2"]
        if check_containers_in_network("my_network_1", container_names1):
            print(f"container1 and container2 are running on the network my_network_1 ...... Checkpoint Completed(3/5)")
            container_names2 = ["container3", "container4"]
            if check_containers_in_network("my_network_2", container_names2):
                print(f"container3 and container4 are running on the network my_network_2 ...... Checkpoint Completed(4/5)")
                if check_container_ips("file.txt"):
                    print("All container IPs match the expected IPs. ...... Checkpoint Completed(5/5)")
                else:
                    print("Container IPs do not match the expected IPs. ...... Checkpoint Failed(4/5)")
            else:
                print(f"container3 and container4 not found on the network my_network_2 ...... Checkpoint Failed(3/5)")
        else:
            print(f"container1 and container2 not found on the network my_network_1 ...... Checkpoint Failed(3/5)")
    else:
        print(f"The Docker network my_network_2 is not present ...... Checkpoint Failed(1/5)")
else:
    print(f"The Docker network my_network_1 is not present ...... Checkpoint Failed(0/5)")
