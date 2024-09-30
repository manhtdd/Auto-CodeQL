# Use the latest Ubuntu image
FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /app

# Copy the content from the local 'codeql' folder to the '/opt/codeql' directory in the container
COPY ./codeql /opt/codeql

# Add /opt/codeql/codeql to the PATH environment variable
RUN ln -s /opt/codeql/codeql /usr/local/bin/codeql

# Define additional commands or configurations if needed
# Example: install dependencies
# RUN apt-get update && apt-get install -y <package-name>

# Define the entry point or CMD if needed
# Example: CMD ["bash"]
