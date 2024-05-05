# Use the official Nginx image as base
FROM nginx:latest

# Install Node.js
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    npm install -g n && \
    n latest && \
    ln -sf /usr/local/bin/node /usr/bin/node


# Copy the built app from the host machine to Nginx's HTML directory
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80
