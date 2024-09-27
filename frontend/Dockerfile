# Start your image with a node base image
FROM node:18-alpine

# The /app directory should act as the main application directory
WORKDIR /usr/src/app

# Copy the app package and package-lock.json file
COPY package*.json ./

RUN npm install

# Copy all the files into docker working directory
COPY . .

EXPOSE 3000

# Start the app using serve command
CMD [ "npm", "run", "dev" ]