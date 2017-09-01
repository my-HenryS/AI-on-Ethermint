docker-compose -f bean-hwr-server/docker/docker-compose.yml up -d
docker-compose -f bean-hwr/docker/docker-compose.yml up -d
echo "service running on http://localhost:8080"