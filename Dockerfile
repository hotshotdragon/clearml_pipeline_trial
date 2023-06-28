# FROM python:3.10

# # Set the working directory
# WORKDIR /app

# # Copy and install requirements
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of your application code
# COPY . .

# # Set the entry point
# ENTRYPOINT ["python", "control.py"]
# # ENTRYPOINT ["bash"]


FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set the entry point and make it executable
# RUN apt-get update && apt-get install -y bash
# RUN chmod +x /usr/bin/bash
# ENTRYPOINT ["/usr/bin/bash", "-l", "-c" ]
