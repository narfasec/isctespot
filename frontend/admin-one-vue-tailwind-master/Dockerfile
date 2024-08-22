# Use a Node image to build and run the Vue 3 application
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose port 5173 for the Vue development server
EXPOSE 5173

# Command to run the Vue development server
CMD ["npm", "run", "dev"]
