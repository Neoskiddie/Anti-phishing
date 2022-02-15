Ubuntu 20.04.3 LTS

Basic setup & docker
```
apt update && apt upgrade -y
apt remove docker docker-engine docker.io containerd runc
apt install ca-certificates curl gnupg lsb-release vim tmux htop unzip git unattended-upgrades -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update && apt install docker-ce docker-ce-cli containerd.io -y
```

```
docker pull ml6team/tf-serving-tfdf

```
create a /models directory at root:
`mkdir /models`


command used to run docker image `docker run -t --rm -p 8501:8501 -v "/models/phishingModel:/models/phishingModel" -e MODEL_NAME=phishingModel ml6team/tf-serving-tfdf:latest`

this should run only on local port:
`docker run -t --rm -p 127.0.0.1:8501:8501 -v "/models/phishingModel:/models/phishingModel" -e MODEL_NAME=phishingModel ml6team/tf-serving-tfdf:latest`

asuming the directory structure for the "phishingModel" is:
`/models/phishingModel/1/<theActualModel>`