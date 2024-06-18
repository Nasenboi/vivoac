# Store some nice variables:
image_name="vivoac:local"
container_name="vivoac"
volume_mount_1="C:/Users/cboen/Documents/Programmierungen/GitStuff/vivoac/data/piper-voice:/piper-voice"
volume_mount_2="C:/Users/cboen/Documents/Programmierungen/GitStuff/vivoac/data/excel_scripts:/excel_scripts"
port=8080
target="deploy"

# Stop and remove the container if it exists
docker stop $container_name
docker rm $container_name

# Build the image
docker build --target $target -t $image_name .

# Run the container
docker run -itd -p $port:8080 --name $container_name -v $volume_mount_1 -v $volume_mount_2 $image_name