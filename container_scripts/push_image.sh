regname=$1
imagename=$2
imagever=$3
imageurl=$regname.azurecr.io/$imagename:$imagever
echo $imageurl
az acr login -n $regname &&
docker tag $imagename:$imagever $imageurl &&
docker push $imageurl