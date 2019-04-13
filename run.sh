if [ "$1" = "production" ] ; then
    docker run --detach=false --publish=8000:8000 -e STAGE=production stavatech/stavanet-service:latest
else
    docker run --detach=false --publish=8000:8000 -e STAGE=beta -v $(pwd)/app:/srv/app stavatech/stavanet-service:dev
fi