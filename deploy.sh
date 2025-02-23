#!/bin/bash
set -e

# Define variables
LINODE_SSH_USER="tino"
LINODE_IP="172.234.244.143" # Replace with your Linode IP
REMOTE_PATH="/home/$LINODE_SSH_USER/zelo_website"
LOCAL_PATH="."

# Add to Known Hosts
mkdir -p ~/.ssh
ssh-keyscan $LINODE_IP >> ~/.ssh/known_hosts

# Function to copy files
copy_files() {
  echo "Copying files to Linode..."
  scp -r "$LOCAL_PATH" "$LINODE_SSH_USER@$LINODE_IP:$REMOTE_PATH"
  echo "Files copied successfully!"
}

#copy file, create a directory
test_file(){
    ssh $LINODE_SSH_USER@$LINODE_IP "mkdir -p $REMOTE_PATH"
    if [ $? -eq 0 ]; then
        echo "Created $REMOTE_PATH"
    else
        echo "Can't create $REMOTE_PATH in server, please check credentials"
        exit 1
    fi
}

# Function to run remote commands
restart_docker(){
  echo "Restarting Docker containers on Linode..."
  ssh $LINODE_SSH_USER@$LINODE_IP 
  ssh 
  EOF
    cd "$REMOTE_PATH"
    docker-compose -f docker-compose.yml up --build -d
  EOF
  echo "Docker containers restarted successfully!"
}

deploy() {
  test_file
  copy_files
  restart_docker
}

deploy
