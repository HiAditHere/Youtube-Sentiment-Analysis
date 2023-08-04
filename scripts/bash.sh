#!/bin/bash

# Replace 'your-ec2-public-ip' with the actual public IP address of your EC2 instance
EC2_PUBLIC_IP= '${{ secrets.IP_ADDRESS }}'

# SSH command to check if there are any containers running
containers_running=$(ssh -o "StrictHostKeyChecking=no" ubuntu@$EC2_PUBLIC_IP 'docker ps -q')

if [ -n "$containers_running" ]; then
  # If there are running containers, stop and remove them
  ssh -o "StrictHostKeyChecking=no" ubuntu@$EC2_PUBLIC_IP 'docker stop $(docker ps -q) && docker rm $(docker ps -aq)'
else
  echo "No running containers found on the remote EC2 instance."
fi
