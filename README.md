This program allows you to submit a HTML form with link to a image, and receive the prediction result of the ResNet50 model.

To create a new docker image, run:
docker build -t <IMAGE_NAME> .

To run a docker container on this image, run:
docker run -it --name <CONTAINER_NAME> --rm -p 5000:5000 <IMAGE_NAME>
