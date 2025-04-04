# Stage 1: Build stage
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    wget \
    netcat-traditional \
    gnupg \
    curl \
    unzip \
    xvfb \
    libgconf-2-4 \
    libxss1 \
    libnss3 \
    libnspr4 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    xdg-utils \
    fonts-liberation \
    dbus \
    xauth \
    xvfb \
    x11vnc \
    tigervnc-tools \
    supervisor \
    net-tools \
    procps \
    python3-numpy \
    fontconfig \
    fonts-dejavu \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    && rm -rf /var/lib/apt/lists/*

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc \
    && git clone https://github.com/novnc/websockify /opt/novnc/utils/websockify \
    && ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# Set platform for ARM64 compatibility
ARG TARGETPLATFORM=linux/amd64

# Set up working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Ensure Python PATH includes our dependencies
ENV PATH=/root/.local/bin:$PATH

# Copy the application code
COPY . .

# Install Playwright and browsers with system dependencies
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN playwright install --with-deps chromium
RUN playwright install-deps

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    BROWSER_USE_LOGGING_LEVEL=info \
    CHROME_PATH=/ms-playwright/chromium-*/chrome-linux/chrome \
    ANONYMIZED_TELEMETRY=false \
    DISPLAY=:99 \
    RESOLUTION=1920x1080x24 \
    VNC_PASSWORD=vncpassword \
    CHROME_PERSISTENT_SESSION=true \
    RESOLUTION_WIDTH=1920 \
    RESOLUTION_HEIGHT=1080

# Create necessary directories
RUN mkdir -p /tmp/record_videos /tmp/traces /tmp/agent_history /var/log/supervisor

# Set up supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for web UI, vnc, and novnc
EXPOSE 7788 6080 5901

# Create .dockerignore if it doesn't exist
RUN if [ ! -f .dockerignore ]; then \
    echo "**/.git\n**/.gitignore\n**/.vscode\n**/venv\n**/__pycache__\n**/*.pyc" > .dockerignore; \
    fi

# Start supervisord to manage processes
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
