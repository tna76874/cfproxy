#!/bin/bash
docker build -t ghcr.io/tna76874/cfproxy:edge .

docker run -p 5000:5000 --name cfproxy-container --rm -v $(pwd)/data:/app/data ghcr.io/tna76874/cfproxy:edge
