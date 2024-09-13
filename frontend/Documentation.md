# Documentation for Frontend of VoPOP

## Initial setup
To get set up for running the frontend server on local machine you will need two things installed first:
- Node
- NPM

You can download these CLI you can do so through this guide: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

Once installed, `cd` into the `frontend` folder. You want to run `npm install` command to install all the React dependencies for the application (you only need to do this once).

## Starting up frontend server
It is very simple to start up the frontend server. 
- `cd` into `frrontend` folder.
- Run the command `npm run dev`

Bing Bang Boom the server should be running now. In the command terminal, the server address should be shown and you can access the website using this (it should be localhost:3000).

## Using Docker to build frontend
With Docker you don't need to install all the dependencies. All you need to do is make sure Docker is installed on your machine. It is recommended you install Docker through Docker Desktop.

Steps to get docker container running:
- `cd` into `frontend` folder.
- Run `docker build -t vopop-frontend .` to create the Docker image.

The above steps are to create the Docker image. You only need to rebuild the docker image when there are file changes.

To run the image created in a container, run: `docker run -d --name vopop-frontend -p 3000:3000 vopop-frontend`. NOTE: if you have already created the container before, you can simply do `docker start vopop-frontend` to re-run that container.

To see the container that is running, open up the browser and go to `localhost:3000` (or `localhost:3000/dummy` when backend server is not running)

To stop the container running, simply run: `docker stop vopop-frontend`

## Folder structure
The frontend folder contains lots of stuff. What the developers mainly need to concern themselves with is found in the `src` folder. This is where all the code for the React components and pages are.

Each file in the folder should be commented with an explanation of it's purpose. General overview of the files
- `src/`
  - `main.tsx` is the entry point of the React application.
  - `App.tsx`  defines all the routes for the application.
  - `api.tsx` is for the authentiicated API object (used to call API requests that require backend authorization).
  - `tokenManager.ts` is for defening the refresh token functionality and checking current authorization.
  - `dummyData.ts` defines dummy data to use for testing independent of backend server running.
- `src/components/` -> folder containng all React components.
- `src/pages/` -> folder containing all the pages of our web application.

