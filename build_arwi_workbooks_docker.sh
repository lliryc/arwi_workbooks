# Build and push docker image - push only if build succeeds
docker buildx build --platform linux/amd64 -t chelliryc/arwi-workbooks:0.1.1 -f Dockerfile . && \
docker push chelliryc/arwi-workbooks:0.1.1
