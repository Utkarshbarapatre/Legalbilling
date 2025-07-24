# Multi-stage build for Railway deployment
FROM python:3.11-slim as python-app

# Set working directory for Python app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application
COPY app/ ./app/
COPY static/ ./static/
COPY chrome-extension/ ./chrome-extension/
COPY .env* ./

# Create database directory
RUN mkdir -p /app/data

# Stage 2: Node.js for Next.js
FROM node:18-alpine as nextjs-app

WORKDIR /nextjs

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy Next.js app
COPY app/ ./app/
COPY static/ ./static/
COPY next.config.js ./
COPY tsconfig.json ./

# Build Next.js app
RUN npm run build

# Final stage: Combine both
FROM python:3.11-slim

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python app
COPY --from=python-app /app /app
COPY --from=python-app /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-app /usr/local/bin /usr/local/bin

# Copy Next.js build
COPY --from=nextjs-app /nextjs/.next /app/.next
COPY --from=nextjs-app /nextjs/node_modules /app/node_modules
COPY --from=nextjs-app /nextjs/package.json /app/package.json

# Create startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# Start both services
CMD ["/app/start.sh"]
