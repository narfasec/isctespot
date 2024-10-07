#!/bin/bash

# Define container name
containerName="isctespot-server-1"

# Define the paths to your scripts inside the container
cleanDbScript="/app/db/setup/clean_db.py"
createDbScript="/app/db/setup/create_db.py"
dataPopulationScript="/app/db/setup/data_population.py"

# Check if the container is running
if ! docker ps --filter "name=$containerName" --format "{{.Names}}" | grep -q "$containerName"; then
    echo "The container $containerName is not running. Please start it first."
    exit 1
fi

# Execute the database setup scripts in the correct order
docker exec $containerName python $cleanDbScript
if [ $? -ne 0 ]; then
    echo "Error executing clean_db.py. Exiting..."
    exit 1
fi

docker exec $containerName python $createDbScript
if [ $? -ne 0 ]; then
    echo "Error executing create_db.py. Exiting..."
    exit 1
fi

docker exec $containerName python $dataPopulationScript
if [ $? -ne 0 ]; then
    echo "Error executing data_population.py. Exiting..."
    exit 1
fi

echo "Database setup and data population completed successfully."
