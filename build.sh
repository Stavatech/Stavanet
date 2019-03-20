if [ "$1" = "production" ] ; then
    docker build -t stavatech/stavanet-service:latest . -f docker/Dockerfile.production
else
    docker build -t stavatech/stavanet-service:dev . -f docker/Dockerfile.development
fi