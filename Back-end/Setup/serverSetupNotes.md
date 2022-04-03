Ubuntu 20.04.3 LTS

First add user with
`adduser anon`
`sudo usermod -aG sudo anon`
Then make .ssh directory in user home:
`mkdir /home/anon/.ssh`
`chmod 700 ~/.ssh`

----
If you are copying key that was used by root:
then copy the key you used for root to that directory:
`mv authorized_keys /home/anon/.ssh/`
then
`cd /home/anon/.ssh/`
and change owner of the file:
`chown anon authorized_keys`

If you generated key yourself:
On LOCAL system, not remote run: `ssh-keygen -t rsa`

then copy the key to remote with something like:
`scp –p id_rsa.pub remoteuser@remotehost:`

append the key to authorized keys:
`cat id_rsa.pub >> ~/.ssh/authorized_keys`
`rm id_rsa.pub`
``
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
``

Then go to :
`sudo vim /etc/ssh/sshd_config`

There uncomment Port and change it to somethign different then default
```
Port 6372
PermitRootLogin no
PermitEmptyPasswords no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers anon
```


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