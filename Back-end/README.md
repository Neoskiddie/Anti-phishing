# Server setup

API and docker were hosted on Ubuntu 20.04.3 LTS.

Download the docker image with TensorFlow Decision Forests already compiled:
```
docker pull ml6team/tf-serving-tfdf

```

create a /models directory at root:
`mkdir /models`

command used to run docker image: `docker run -t --rm -p 8501:8501 -v "/models/phishingModel:/models/phishingModel" -e MODEL_NAME=phishingModel ml6team/tf-serving-tfdf:latest`

this should run only on local port:
`docker run -t --rm -p 127.0.0.1:8501:8501 -v "/models/phishingModel:/models/phishingModel" -e MODEL_NAME=phishingModel ml6team/tf-serving-tfdf:latest`

assuming the directory structure for the "phishingModel" is:
`/models/phishingModel/1/<theActualModel>`

