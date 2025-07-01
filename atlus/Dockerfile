FROM node:22-alpine AS builder

WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# Use nginx to serve the build folder
FROM nginx:alpine

# Copy the build output to nginx html directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Optional: Use a custom nginx config (recommended)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
