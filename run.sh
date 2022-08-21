docker build -t $1 .
docker run -it --name $1 --rm -p 5000:5000 $1
