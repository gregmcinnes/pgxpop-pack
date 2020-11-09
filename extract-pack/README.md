# extract-pack

Extract genomics regions from a gVCF and expand the blocks.

```
pack build --builder gcr.io/buildpacks/builder:v1 my-sample --env GOOGLE_ENTRYPOINT="python main.py -f input_file.vcf.gz -o docker_test.vcf"
```

```
docker run -v /Users/gmcinnes/sandbox/docker/exome_test_data/:/workspace/input -v /Users/gmcinnes/sandbox/docker/output/:/workspace/output --rm  my-sample
```





