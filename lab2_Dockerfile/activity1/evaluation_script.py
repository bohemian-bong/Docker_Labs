import docker

def check_image_and_container():
    client = docker.from_env()
    image_name = "alpine-git"
    image_tag = "labs-git-v1"
    container_name = "alpine-git-container"

    # Check if the image exists
    try:
        image = client.images.get(f"{image_name}:{image_tag}")
        print(f"Image {image_name}:{image_tag} exists. ................... Checkpoint Completed (1/3)")
    except docker.errors.ImageNotFound:
        print(f"Image {image_name}:{image_tag} does not exist. ........... Checkpoint Failed (0/3)")
        return

    # Check if a container is running based on the image
    containers = client.containers.list(filters={"ancestor": f"{image_name}:{image_tag}"})
    if containers:
        print(f"A container based on {image_name}:{image_tag} is running. ....... Checkpoint Completed (2/3)")
        container = containers[0]  # Assuming only one container is running
        # Check if git is installed in the container
        exec_command = "/usr/bin/git --version"
        try:
            exec_result = container.exec_run(exec_command)
            print("Git is installed on the container. ........... Checkpoint Completed (3/3)")
        except docker.errors.APIError:
            print("Git is not installed on the container. ............ Checkpoint Failed (2/3)")
    else:
        print(f"No container based on {image_name}:{image_tag} is running. .............. Checkpoint Failed (1/3)")

if __name__ == "__main__":
    check_image_and_container()

