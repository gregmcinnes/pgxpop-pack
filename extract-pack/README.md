# extract-pack

Extract genomics regions from a gVCF and expand the blocks.


## Create the docker image
Create the docker environment using [buildpacks](https://cloud.google.com/blog/products/containers-kubernetes/google-cloud-now-supports-buildpacks). 
This command will create a docker image named 'extract-pack'.
```
pack build --builder gcr.io/buildpacks/builder:v1 extract-pack --env GOOGLE_ENTRYPOINT="python main.py"```
```

## Run
The script will automatically check `/workspace/input/` for input data.  The input VCF, index, fasta, and fasta indices need to be copied into the workspace.  The output directory also needs to be mounted in `/workspace/output`. 

It will run on all VCFs in the input directory and output all results to the specified output directory.
```
docker run \
    -v /PATH/TO/SHIP4946367.g.vcf.gz:/workspace/input/SHIP4946367.g.vcf.gz \
    -v /PATH/TO/SHIP4946367.g.vcf.gz.tbi:/workspace/input/SHIP4946367.g.vcf.gz.tbi \
    -v /PATH/TO/hg38.fa.gz:/workspace/input/hg38.fa.gz \
    -v /PATH/TO/hg38.fa.gz.gzi:/workspace/input/hg38.fa.gz.gzi \
    -v /PATH/TO/hg38.fa.gz.gzi:/workspace/input/hg38.fa.gz.gzi \
    -v /PATH/TO/output:/workspace/output/ \
    extract-pack

```


Fasta files Google Storage locations
```
gs://gbsc-gcp-project-mvp-dev-group/gmcinnes/hg38.fa.gz
gs://gbsc-gcp-project-mvp-dev-group/gmcinnes/hg38.fa.gz.fai
gs://gbsc-gcp-project-mvp-dev-group/gmcinnes/hg38.fa.gz.gzi
```

Image GCR

```
docker tag extract-pack gcr.io/gbsc-gcp-project-mvp-dev/extract-pack

```

```
docker push gcr.io/gbsc-gcp-project-mvp-dev/extract-pack
```





