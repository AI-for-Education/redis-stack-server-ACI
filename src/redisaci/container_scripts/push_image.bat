set regname=%1
set imagename=%2
set imagever=%3
set imageurl=%regname%.azurecr.io/%imagename%:%imagever%
echo %imageurl%
call az acr login -n %regname%
call docker tag %imagename%:%imagever% %imageurl%
call docker push %imageurl%