# Building Milvus from Scratch

- Pull Image from Docker `sudo docker pull milvusdb/milvus:1.0.0-cpu-d030521-1ea92e` -- CPU Only, GPU install available @ https://milvus.io/docs/v1.0.0/install_milvus.md
- Configure Milvus for Local OS
  - Make Config dir at Home and Go There `mkdir -p ~/milvus/conf && cd ~/milvus/conf`
    - Download sample config file `wget https://raw.githubusercontent.com/milvus-io/milvus/v1.0.0/core/conf/demo/server_config.yaml`
	  - Defaults are reasonable, Milvus should run on Port `19530` w a 4GB CPU cache
	  - Launch Milvus in Docker
	  ```
	  sudo docker run -d --name milvus_cpu_test \
	  -p 19530:19530 \
	  -p 19121:19121 \
	  -v ~/milvus/db:/var/lib/milvus/db \
	  -v ~/milvus/conf:/var/lib/milvus/conf \
	  -v ~/milvus/logs:/var/lib/milvus/logs \
	  -v ~/milvus/wal:/var/lib/milvus/wal \
	  milvusdb/milvus:1.0.0-cpu-d030521-1ea92e
	  ```
	  - View Error/Container Logs- `sudo docker logs milvus_cpu` --> if `milvus_cpu` is our container name
	  - Check Container is online with a `curl localhost:19121` --> if in a local terminal (where milvus is accessible via localhost, not in a sep docker container)

	  *for testing, the `FLAT` index is sufficient (highest recall and largest in size, not too slow for millions of Vectors)
	
