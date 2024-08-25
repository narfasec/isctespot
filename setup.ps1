# Define container name
$containerName = "project-server-1"

# Define the paths to your scripts inside the container
$createDbScript = "/app/db/setup/create_db.py"
$dataPopulationScript = "/app/db/setup/data_population.py"

# Check if the container is running
$container = docker ps --filter "name=$containerName" --format "{{.Names}}"
if (-not $container) {
    Write-Host "The container $containerName is not running. Please start it first."
    exit 1
}

# Execute the database setup scripts in the correct order
docker exec $containerName python $createDbScript
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error executing create_db.py. Exiting..."
    exit 1
}

docker exec $containerName python $dataPopulationScript
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error executing data_population.py. Exiting..."
    exit 1
}

Write-Host "Database setup and data population completed successfully."
