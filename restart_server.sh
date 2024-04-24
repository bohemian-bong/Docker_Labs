docker stop server-container
docker rm server-container
docker rmi server-image:latest
docker build -t server-image ./lab2_Dockerfile/activity3/server
docker run -id --name server-container -p 3000:3000 --link mongodb-container:mongodb server-image