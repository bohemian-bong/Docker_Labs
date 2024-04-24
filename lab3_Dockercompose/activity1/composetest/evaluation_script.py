import subprocess
import sys
import requests
import psutil


def check_services_running():
    try:
        # Run the "docker compose ps" command to get the status of services
        result = subprocess.run(["docker", "compose", "ps"], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        
        # Check if both redis and web services are running
        if "redis" in output and "Up" in output and "web" in output and "Up" in output:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def check_hello_world():
    try:
        response = requests.get("http://localhost:8000")
        return "Hello" in response.text
    except Exception as e:
        print(f"An error occurred while making the request: {e}")
        return False

def check_compose_watch_running():
    try:
        # Run the command and capture the output
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        ps_output = result.stdout
        
        # Count the number of lines containing "compose watch" in the output
        count = sum(1 for line in ps_output.split('\n') if "compose" in line and "watch" in line)
        
        return count
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def check_hello_iit():
    try:
        response = requests.get("http://localhost:8000")
        return "Hello IIT Bombay" in response.text
    except Exception as e:
        print(f"An error occurred while making the request: {e}")
        return False

if __name__ == "__main__":
    print("----PART-I------")
    if check_services_running():
        print("Redis and web services are running. ....... Checkpoint Completed(1/4)")
        if check_hello_world():
            print("The web service is running successfully on localhost. ....... Checkpoint Completed(2/4)")
            print("----PART-II------")
            if check_compose_watch_running():
                print("Compose watch is running successfully ......... Checkpoint Completed(3/4)")
                if check_hello_iit():
                    print("Files changed and running successfully ......... Checkpoint Completed(4/4)")
                else:
                    print("Files not changed ......... Checkpoint Failed(3/4)")
            else:
                print("Compose watch is not running ......... Checkpoint Failed(2/4)")
        else:
            print("The web is not running on localhost. ....... Checkpoint Failed(1/4)")
            sys.exit(1)
    else:
        print("Redis and/or web services are not running. ....... Checkpoint Failed(0/4)")
        sys.exit(1)