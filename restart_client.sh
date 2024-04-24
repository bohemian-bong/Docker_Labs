docker stop client-container
docker rm client-container
docker rmi client-image:latest
docker build -t client-image ./lab2_Dockerfile/activity3/client
docker run -d --name client-container -p 80:80 client-image