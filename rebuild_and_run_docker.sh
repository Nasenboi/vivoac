# Store some nice variables:
image_name="vivoac:local"
container_name="vivoac"
volume_mount_1="./backend/data/piper_voices:/piper_voices"
volume_mount_2="./backend/data/excel_scripts:/excel_scripts"
port=8080
target="base"
compose=1

# Stop and remove the container if it exists
docker stop $container_name > /dev/null 2>&1
docker rm $container_name > /dev/null 2>&1
# Stop and remove the container stack if it exists
docker-compose -f ./backend/docker-compose.yaml -p vivoac down > /dev/null 2>&1

# Build the image
docker build --target $target -t $image_name ./backend

if [ "$compose" -eq 1 ]; then
    # Run the container with docker-compose
    docker-compose -f ./backend/docker-compose.yaml -p vivoac up -d
else
    # Run the container
    docker run -itd -p $port:8080 --name $container_name -v $volume_mount_1 -v $volume_mount_2 $image_name
fi