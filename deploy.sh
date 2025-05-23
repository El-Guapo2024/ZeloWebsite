#!/bin/bash
set -e

# Define variables
LINODE_SSH_USER="tino"
LINODE_IP="172.234.244.143" # Replace with your Linode IP
REMOTE_PATH="/home/$LINODE_SSH_USER/zelo_website"
LOCAL_PATH="."

# Determine if script is running locally or on remote server
IS_LOCAL=false
if [ -z "$GITHUB_ACTIONS" ]; then
    IS_LOCAL=true
fi

# Function to stop and remove existing containers
cleanup_docker() {
    echo "Cleaning up Docker containers..."
    docker-compose down --remove-orphans
    docker system prune -f
    echo "Docker cleanup completed!"
}

# Function to copy files
copy_files() {
    if [ "$IS_LOCAL" = false ]; then
        echo "Copying files to Linode..."
        scp -r "$LOCAL_PATH" "$LINODE_SSH_USER@$LINODE_IP:$REMOTE_PATH"
        echo "Files copied successfully!"
    fi
}

# Create remote directory if needed
setup_remote_dir() {
    if [ "$IS_LOCAL" = false ]; then
        echo "Setting up remote directory..."
        ssh $LINODE_SSH_USER@$LINODE_IP "mkdir -p $REMOTE_PATH"
        if [ $? -eq 0 ]; then
            echo "Created $REMOTE_PATH"
        else
            echo "Can't create $REMOTE_PATH in server, please check credentials"
            exit 1
        fi
    fi
}

# Function to setup environment
setup_env() {
    if [ "$IS_LOCAL" = true ]; then
        if [ -f .env.dev ]; then
            echo "Using development environment file..."
            cp .env.dev .env
        else
            echo "Warning: .env.dev file not found!"
            exit 1
        fi
    else
        echo "Using production environment file..."
        if [ ! -f .env ]; then
            echo "Error: Production .env file not found!"
            exit 1
        fi
    fi
}

# Function to start Docker containers
start_docker() {
    echo "Starting Docker containers..."
    docker-compose up --build -d
    echo "Docker containers started successfully!"
}

deploy() {
    if [ "$IS_LOCAL" = true ]; then
        echo "Running local deployment..."
        setup_env
    else
        echo "Running production deployment..."
    fi
    
    cleanup_docker
    start_docker
    echo "Deployment completed successfully!"
}

deploy
