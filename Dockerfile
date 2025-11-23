FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    nodejs \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Appium and driver
RUN npm install -g appium
RUN appium driver install uiautomator2

# Copy project
COPY . .

# Install ruff
RUN pip install ruff==0.14.6

CMD ["pytest", "tests/", "-v"]
