# merge-pack

Merge multiple bcf files into a single multi-sample bcf.


## Create the docker image
Create the docker environment using [buildpacks](https://cloud.google.com/blog/products/containers-kubernetes/google-cloud-now-supports-buildpacks). 
This command will create a docker image named 'extract-pack'.
```
pack build --builder gcr.io/buildpacks/builder:v1 merge-pack --env GOOGLE_ENTRYPOINT="python main.py"
```

## Run
The script will automatically check `/workspace/input/` for input data.  The input BCF, index, fasta, and fasta indices need to be copied into the workspace.  The output directory also needs to be mounted in `/workspace/output`. 

It will run on all BCFs in the input directory and output all results to the specified output directory.  It's probably easies to mount a bucket with all the BCFs rather than copy each one.
```
docker run \
    -v /Users/gmcinnes/sandbox/docker/merge_test/input:/workspace/input \
    -v /Users/gmcinnes/sandbox/docker/hg38.fa.gz:/workspace/input/hg38.fa.gz \
    -v /Users/gmcinnes/sandbox/docker/hg38.fa.gz.gzi:/workspace/input/hg38.fa.gz.gzi \
    -v /Users/gmcinnes/sandbox/docker/hg38.fa.gz.gzi:/workspace/input/hg38.fa.gz.gzi \
    -v /Users/gmcinnes/sandbox/docker/merge_test/output:/workspace/output/ \
    merge-pack

```


## Google Cloud details
Fasta files Google Storage locations
```
gs://gbsc-gcp-project-mvp-dev-group/gmcinnes/hg38.fa.gz
gs://gbsc-gcp-project-mvp-dev-group/gmcinnes/hg38.fa.gz.fai
gs://gbsc-gcp-project-mvp-dev-group/gmcinnes/hg38.fa.gz.gzi
```

Image GCR

```
docker tag merge-pack gcr.io/gbsc-gcp-project-mvp-dev/merge-pack
```

```
docker push gcr.io/gbsc-gcp-project-mvp-dev/merge-pack
```

extract-pack image is here on GCR
```
gcr.io/gbsc-gcp-project-mvp-dev/merge-pack
```




