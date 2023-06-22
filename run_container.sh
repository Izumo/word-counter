podman run --name tokenizer --cpu-period=1000000 --cpu-quota=200000 -d -p 8001:8001 tokenizer
podman run --name mapper -d -p 8002:8002 mapper
podman run --name reducer -d -p 8003:8003 reducer
podman run --name wordfreq -d -e TOKENIZER_URL=http://192.168.11.168:8001 -e MAPPER_URL=http://192.168.11.168:8002 -e REDUCER_URL=http://192.168.11.168:8003 -p 8000:8000 wordfreq
