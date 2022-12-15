# Installing Docker on Ubuntu

Some issues and Googling has to be done to properly spin up Docker on an Ubuntu EC2 instance --> here is what I did in hopes that is saves humans time


1. Setting Up Docker Repo- 
```
# get deps
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Official GPG Key from Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Install + Set Up Repo
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

2. Getting Docker Engine 
  - see this post for why docker engine is preferred for SSH-esque machines- https://forums.docker.com/t/difference-between-docker-desktop-and-docker-engine/124612
```
# Update Machine
sudo apt-get update

# Main Install via apt
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Update Docker Daemon Permissions (to solve socket error)
sudo usermod -a -G docker ubuntu
  #ubuntu in above is the default username of a new Machine (assuming you choose ubuntu for the server, updates the specified username's permissions to be able to user docker)
sudo chmod 777 /var/run/docker.sock #read, write & execute permissions for everyone --> kinda dangerous?

# Verify w Hello World Example (installation is working correctly)
sudo docker run hello-world
```

3. Getting Docker Compose (for orchestration)
```
sudo apt-get install docker-compose
```



