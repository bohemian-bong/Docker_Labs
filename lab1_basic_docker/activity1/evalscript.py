import docker

def check_hello_world_image():
    client = docker.from_env()

    # List all images
    images = client.images.list()

    # Check if "hello-world" image exists
    for image in images:
        for tag in image.tags:
            if "hello-world" in tag:
                return True
    
    return False

if __name__ == "__main__":
    if check_hello_world_image():
        print("Successfully found 'hello-world' Docker image ...... Checkpoint Passed(1/1)")
    else:
        print("The 'hello-world' Docker image not found ........... Chackpoint Failed(0/1)")
