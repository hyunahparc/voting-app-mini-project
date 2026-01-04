# 1. Node.js 18
FROM node:18-alpine

# 2. Working directory inside the container
WORKDIR /app

# 3. Copy dependency files first (for cache optimization)
COPY package*.json ./

# 4. Install production dependencies only
RUN npm install --production

# 5. Copy the rest of the source code
COPY . .

# 6. Port exposed by the Node server
EXPOSE 3000

# 7. Run the application
CMD ["npm", "start"]
