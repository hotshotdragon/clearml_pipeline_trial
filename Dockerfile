# FROM python:3.10

# # Set the working directory
# WORKDIR /app

# # Copy and install requirements
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of your application code
# COPY . .

# # WORKDIR /usr/agent

# # COPY . /usr/agent
# # RUN apt-get update
# # RUN apt-get dist-upgrade -y
# # RUN apt-get install -y curl python3-pip git
# # RUN curl -sSL https://get.docker.com/ | sh
# # RUN python3 -m pip install -U pip
# # RUN python3 -m pip install clearml-agent
# # RUN python3 -m pip install -U "cryptography>=2.9"

# ENTRYPOINT ["entrypoint.sh"]
# # RUN python3 -m clearml_agent daemon --queue services --docker clearml-pipeline:0.6
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages
RUN apt-get update && apt-get install -y \
    curl \
    git

# Install Docker
# RUN curl -sSL https://get.docker.com/ | sh

# Copy the rest of your application code
COPY . .

CMD ["BASH"]
# Make entrypoint.sh executable
# RUN chmod +x entrypoint.sh

# ENTRYPOINT ['python','main.py']
