# Use the official Node.js image as base
FROM node:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install express
RUN npm install cors
RUN npm install mongoose

# Copy the rest of the application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Command to run the server
CMD ["npm", "start"]
