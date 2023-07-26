# Use an official Fedora base image
FROM fedora:latest

# Install necessary dependencies
RUN dnf update -y && dnf install -y python3 python3-pip wget unzip curl gnupg2 ca-certificates
RUN dnf install -y chromium libXcomposite libXcursor libXdamage libXext libXi libXtst cups-libs libXScrnSaver libXrandr GConf2 alsa-lib atk gdk-pixbuf2 gtk3

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install Chromium and its dependencies
RUN dnf install -y chromium

# Install Chromedriver
RUN dnf install -y chromedriver

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the build arguments (environment variables)
ARG URL_BY_CATEGORY
ARG CATEGORY_LEVEL1
ARG CATEGORY_LEVEL2
ARG CATEGORY_LEVEL3
ARG N_PAGES
ARG MAX_RETRIES
ARG NAME_LINKS_FILE
ARG NAME_DATA_EXTRACTED_FILE

# Set the environment variables using the build arguments
ENV URL_BY_CATEGORY=$URL_BY_CATEGORY
ENV CATEGORY_LEVEL1=$CATEGORY_LEVEL1
ENV CATEGORY_LEVEL2=$CATEGORY_LEVEL2
ENV CATEGORY_LEVEL3=$CATEGORY_LEVEL3
ENV N_PAGES=$N_PAGES
ENV MAX_RETRIES=$MAX_RETRIES
ENV NAME_LINKS_FILE=$NAME_LINKS_FILE
ENV NAME_DATA_EXTRACTED_FILE=$NAME_DATA_EXTRACTED_FILE

ENV DATA_PATH=/Users/jassielmg/Documents/data_extracted

VOLUME $DATA_PATH:/app/data_extracted

# Set the path to Chromedriver
ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver

# Run the main.py script
CMD ["python3", "main.py"]
