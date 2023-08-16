# Use an official Node.js runtime as the base image
FROM node:14 as build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Vue.js app
RUN npm run build

# Use a lightweight Nginx image as the final base image
FROM nginx:alpine

# Copy the built app from the build stage to the nginx document root
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for the nginx server
EXPOSE 8000

# Start the nginx server
CMD ["nginx", "-g", "daemon off;"]
