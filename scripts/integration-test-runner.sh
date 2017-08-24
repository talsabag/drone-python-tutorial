#!/bin/sh
# remove old containers
docker-compose -p ci --file docker-compose.yml --file docker-compose.yml rm -f

# Clean up name collitions and don't error out or try and kill anything running...
docker rm $(docker ps -a -q --filter 'exited=0') 2>/dev/null

# run
docker-compose -p ci --file docker-compose.yml --file docker-compose.test.yml build

# Startup web database
docker-compose -p ci --file docker-compose.yml --file docker-compose.test.yml up -d database
docker-compose -p ci --file docker-compose.yml --file docker-compose.test.yml up -d redis
docker-compose -p ci --file docker-compose.yml --file docker-compose.test.yml up -d web
docker-compose -p ci --file docker-compose.yml --file docker-compose.test.yml up sut
# Stop the services
docker-compose -p ci --file docker-compose.yml --file docker-compose.test.yml stop

docker-compose -p ci --file docker-compose.yml --file docker-compose.test.yml ps -q | xargs docker inspect -f '{{ .State.ExitCode }}' | while read code; do
    echo "Exit code is currently $code"
    if [ "$code" != "0" ]; then
        # Clean up name collitions and don't error out or try and kill anything running...
        docker rm $(docker ps -a -q --filter 'exited=0') 2>/dev/null
        exit $code
    fi
done

# Clean up name collitions and don't error out or try and kill anything running...
docker rm $(docker ps -a -q --filter 'exited=0') 2>/dev/null
