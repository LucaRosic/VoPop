# Start your image with a node base image
FROM node:18-alpine

# The /app directory should act as the main application directory
WORKDIR /app

# Directory path for frontend folder
ARG FRONTEND_DIR=./frontend

# Copy the app package and package-lock.json file
COPY ${FRONTEND_DIR}/package*.json ./

RUN npm install

# Copy all the files into docker working directory
COPY ${FRONTEND_DIR} .

EXPOSE 8080

# Start the app using serve command
CMD [ "npm", "run", "dev" ]