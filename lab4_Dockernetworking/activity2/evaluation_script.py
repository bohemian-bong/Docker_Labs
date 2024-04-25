import docker

def check_docker_network(network_name):
    client = docker.from_env()
    try:
        network = client.networks.get(network_name)
        return True
    except docker.errors.NotFound:
        return False

def check_container_running(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        return container.status == "running"
    except docker.errors.NotFound:
        return False

def check_container_network(container_name, network_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        return network_name in container.attrs['NetworkSettings']['Networks']
    except docker.errors.NotFound:
        return False

def check_router_container_connected(network_names):
    client = docker.from_env()
    try:
        router_container = client.containers.get("activity2-router-container-1")
        container_networks = router_container.attrs['NetworkSettings']['Networks']
        for network_name in ["activity2_server-network", "activity2_client-network"]:
            if network_name not in container_networks:
                return False
        return True
    except docker.errors.NotFound:
        return False

def main():
    server_network_exists = check_docker_network("activity2_server-network")
    client_network_exists = check_docker_network("activity2_client-network")
    mongodb_container_running = check_container_running("activity2-mongodb-container-1")
    server_container_running = check_container_running("activity2-server-container-1")
    client_container_running = check_container_running("activity2-client-container-1")
    server_container_network = check_container_network("activity2-server-container-1", "activity2_server-network")
    client_container_network = check_container_network("activity2-client-container-1", "activity2_client-network")
    router_connected = check_router_container_connected(["activity2-server-network-1", "activity2_client-network"])

    print("activity2-server-network exists:", server_network_exists)
    print("activity2-client-network exists:", client_network_exists)
    print("activity2-mongodb-container is running:", mongodb_container_running)
    print("activity2-server-container is running:", server_container_running)
    print("activity2-client-container is running:", client_container_running)
    print("activity2-server-container is connected to activity2-server-network:", server_container_network)
    print("activity2-client-container is connected to activity2-client-network:", client_container_network)
    print("activity2-router-container is connected to both networks:", router_connected)

if __name__ == "__main__":
    main()
