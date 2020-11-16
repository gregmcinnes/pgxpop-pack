
# Phase

Phase a multisample VCF or BCF with [Eagle2](https://alkesgroup.broadinstitute.org/Eagle/).

There is no buildpack for phasing, only a docker image that has Eagle2 installed.



## Create the docker image
Used [this](https://hub.docker.com/layers/ljanin/eagle/2.0.4/images/sha256-7fd69ae2b427ad803f160c7b4639d588ddfda29d9232dd70b623e5c724a24eea?context=explore) as a base image and wrote some wrapper code within the image.


## Run
Copy the input file and index into `/input`.  Specify an output directory mounted to `/output`.  `phaser.sh` will run Eagle2 for each chromosome outputing all files to the output directory.  The output files will be named based on the input file.
```
docker run \
    -v /PATH/TO/merged_pgx.bcf:/input/merged_pgx.bcf \
    -v /PATH/TO/merged_pgx.bcf.csi:/input/merged_pgx.bcf.csi \
    -v /PATH/TO/output/:/output/ \
    eagle2 \
    sh /phaser.sh /input/merged_pgx.bcf
```


## Google Cloud details

Image GCR

```
docker tag eagle2 gcr.io/gbsc-gcp-project-mvp-dev/eagle2
```

```
docker push gcr.io/gbsc-gcp-project-mvp-dev/eagle2
```

extract-pack image is here on GCR
```
gcr.io/gbsc-gcp-project-mvp-dev/eagle2
```














