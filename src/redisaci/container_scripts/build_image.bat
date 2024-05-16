set imagename=%1
set imagever=%2
set dockerfile=%3
set rediskey=%4
call echo %rediskey%
call docker build -f "%dockerfile%" --progress=plain -t %imagename%:%imagever% --build-arg REDIS_KEY=%rediskey% .