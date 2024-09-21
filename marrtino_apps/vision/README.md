# Setup objrec server

Build docker image

    cd docker
    docker build --build-arg UID=`id -u` --build-arg GID=`id -g` -t marrtino:objrec -f Dockerfile.objrec .

Run docker container

    cd docker
    docker-compose -f docker-compose.objrec up -d

Check docker container

    docker exec -it objrec tmux a


Run takephoto ROS node

    cd camera
    python takephoto.py

Send ROS topic to send image to server
    
    rostopic pub /takephoto ... 'send <server> <port> [<width> <height>]'

Read result

    rosparam get /takephoto/imageresult

Image is saved in this folder (you sen set a different one)

    rosparam get /takephoto/imagefolder



