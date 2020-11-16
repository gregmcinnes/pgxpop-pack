# PGxPOP


Call pharmacogenetic alleles using [PGxPOP](https://github.com/PharmGKB/PGxPOP).

There is no buildpack for phasing, only a docker image that has PGxPOP installed.


## Create the docker image
Used `docker.io/library/ubuntu:20.04` as a base image and wrote some wrapper code within the image.


## Run
Mount the directory with the phased files to `/input`.  Specify an output directory mounted to `/output`.  `pgxpop.sh` will run PGxPOP for each chromosome outputing all files to the output directory.
```
docker run \
    -v /PATH/TO/input:/input/ \
    -v /PATH/TO/output/:/output/ \
    pgxpop \
    sh pgxpop.sh

```


## Google Cloud details

Image GCR

```
docker tag pgxpop gcr.io/gbsc-gcp-project-mvp-dev/pgxpop
```

```
docker push gcr.io/gbsc-gcp-project-mvp-dev/pgxpop
```

pgxpop image is here on GCR
```
gcr.io/gbsc-gcp-project-mvp-dev/pgxpop
```

