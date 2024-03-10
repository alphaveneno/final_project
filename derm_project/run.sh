#!/bin/bash

# List of ports to try
ports=(8000 8001 8002)

# Loop over the ports
for port in "${ports[@]}"; do
    # Try to start the server
    echo "Trying to start server on 127.0.0.1:$port"
    python3 manage.py runserver 127.0.0.1:$port

    # If the server started successfully, exit the loop
    if [ $? -eq 0 ]; then
        echo "Server started successfully on 127.0.0.1:$port"
        exit 0
    fi
done

# If the server couldn't be started on any port, print an error message
echo "Failed to start server on any port"
exit 1

