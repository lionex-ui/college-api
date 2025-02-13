docker build -f deploy/Dockerfile -t cs .

docker stop csc 2>/dev/null || true
docker rm csc 2>/dev/null || true

docker run -d --name csc -p 8000:8000 cs