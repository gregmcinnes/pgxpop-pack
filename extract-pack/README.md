# extract-pack

Extract genomics regions from a gVCF and expand the blocks.


## Create the docker image using buildpacks
Create the docker environment using [buildpacks](https://cloud.google.com/blog/products/containers-kubernetes/google-cloud-now-supports-buildpacks). 
This command will create a docker image named 'extract-pack'.
```
pack build --builder gcr.io/buildpacks/builder:v1 extract-pack --env GOOGLE_ENTRYPOINT="python main.py"
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


## Google Cloud details
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

extract-pack image is here on GCR
```
gcr.io/gbsc-gcp-project-mvp-dev/extract-pack
```

# Run via Dsub on Google Cloud

## Create the image using Docker
Run this in the same directory as the Dockerfile to generate a Docker image.
```
docker build --tag extract-pack .
docker tag extract-pack:1.0 gcr.io/gbsc-gcp-project-mvp-dev/pgxpop/extract-pack:1.0
docker push gcr.io/gbsc-gcp-project-mvp-dev/pgxpop/extract-pack:1.0
```

## Dsub command for extracting regions
You can get the dsub tool here: https://github.com/DataBiosphere/dsub. Dsub is a tool to submit jobs to the Cloud Life Sciences API: https://cloud.google.com/life-sciences/docs/reference/rest.

```
dsub \
    --name pgx-extract \
    --provider google-v2 \
    --regions us-west1 \
    --project gbsc-gcp-project-mvp-dev \
    --min-cores 1 \
    --logging gs://gbsc-gcp-project-mvp-dev-from-personalis-phase3-logs/pgx-extract-test/ \
    --image gcr.io/gbsc-gcp-project-mvp-dev/pgxpop/extract-pack:1.0 \
    --use-private-address \
    --network trellis \
    --subnetwork trellis-us-west1 \
    --command 'python3 /pgxpop-pack/extract-pack/main.py --vcf ${VCF} --bed ${BED} --fasta ${FASTA_REF} --output ${BCF} --index ${BCF_INDEX}' \
    --input VCF=gs://gbsc-gcp-project-mvp-dev-from-personalis-phase3-data/DVALABP000398/SHIP4946374/gatk-5-dollar/201016-010219-048-8abfcd56/output/germline_single_sample_workflow/b89444cb-77b5-4b13-9824-b6ffd54db190/call-MergeVCFs/SHIP4946374.g.vcf.gz \
    --input FASTA_INDEX=gs://gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta.fai \
    --input VCF_INDEX=gs://gbsc-gcp-project-mvp-dev-from-personalis-phase3-data/DVALABP000398/SHIP4946374/gatk-5-dollar/201016-010219-048-8abfcd56/output/germline_single_sample_workflow/b89444cb-77b5-4b13-9824-b6ffd54db190/call-MergeVCFs/SHIP4946374.g.vcf.gz.tbi \
    --input FASTA_REF=gs://gcp-public-data--broad-references/hg38/v0/Homo_sapiens_assembly38.fasta \
    --input BED=gs://gbsc-gcp-project-mvp-dev-trellis/pgx.grch38.bed \
    --output BCF=gs://gbsc-gcp-project-mvp-dev-from-personalis-phase3-data/extract-vcf-regions/pgx-pop/output/SHIP4946374.pgx-pop.bcf \
    --output BCF_INDEX=gs://gbsc-gcp-project-mvp-dev-from-personalis-phase3-data/extract-vcf-regions/pgx-pop/output/SHIP4946374.pgx-pop.bcf.csi
```



