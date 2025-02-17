FROM python:3.9-slim

# Set environment variables
ENV QUESTDB_CONF="http::addr=questdb:9000;"

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY script.py /app/script.py

# Install required dependencies
RUN pip install --no-cache-dir pyserial questdb ingress

# Set the device permissions (optional, depending on usage)
RUN usermod -a -G dialout root

# Run the script
CMD ["python", "script.py"]
