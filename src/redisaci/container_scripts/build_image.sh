imagename=$1
imagever=$2
dockerfile=$3
rediskey=$4
docker build -f "$dockerfile" --progress=plain -t $imagename:$imagever --build-arg REDIS_KEY=$rediskey .