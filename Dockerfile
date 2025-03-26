FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libxss1 \
    libappindicator3-1 \
    libindicator7 \
    fonts-liberation \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && apt-get clean

# Install Google Chrome
RUN curl -sS https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && \
    dpkg -i chrome.deb && \
    apt-get -y install -f && \
    rm chrome.deb

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/110.0.5481.77/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Chrome
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/google-chrome-stable

# Run the script (using headless mode)
CMD google-chrome-stable --headless --disable-gpu --no-sandbox --remote-debugging-port=9222 && python main.py
