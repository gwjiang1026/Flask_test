
# How to build image
```
## build docker image
image_name="tdri/yolov4-python-flask:demo"
docker build -t "$image_name" .
```
# Run Container 
### run as deamon 
```
container_name="yolov4-flask-01"
image_name="tdri/yolov4-python-flask:demo"
docker run -d --gpus all --name ${container_name} \
    -p 5000:5000 \
    ${image_name} \
    tail -f /dev/null
```
### direct run flask 
```
container_name="yolov4-flask-01"
image_name="tdri/yolov4-python-flask:demo"
docker run --gpus all -d --rm --name ${container_name} \
    -p 5000:5000 \
    ${image_name} \
    flask run --host=0.0.0.0 --no-reload

```

