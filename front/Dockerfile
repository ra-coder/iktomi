# Stage 1: Build Stage
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package.json /app/package.json

# Install the necessary dependencies
RUN npm install @reown/appkit @reown/appkit-adapter-wagmi wagmi viem @tanstack/react-query

# Copy the rest of the application code
COPY ./html /app/.

# If you have a build script in your package.json, you can run it here
COPY tsconfig.json /app/tsconfig.json
RUN npm run build

# Stage 2: NGINX Serve Stage
FROM nginx:alpine

# Copy built files from the previous stage to NGINX html directory
COPY --from=build /app /usr/share/nginx/html

# Copy NGINX configuration file
COPY ./nginx/iktomi.conf /etc/nginx/conf.d/

# Expose port 80 to the outside world
EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]