#!/bin/bash
docker build . -f Dockerfile.local -t h5p.local
docker run --rm -it -p 8888 -v $(pwd):/app h5p.local
