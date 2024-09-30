# Use the latest Ubuntu image
FROM ibm-semeru-runtimes:open-11-jdk-jammy

# Set the working directory to /app
WORKDIR /app

# Copy the content from the local 'codeql' folder to the '/opt/codeql' directory in the container
COPY ./codeql /opt/codeql

# Add /opt/codeql/codeql to the PATH environment variable
RUN ln -s /opt/codeql/codeql /usr/local/bin/codeql


RUN apt-get update && \
    apt-get install -y curl wget unzip python3 python3-pip cpanminus subversion perl git