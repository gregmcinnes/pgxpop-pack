import os
import pysam.bcftools as bcftools


def merge_bcfs(file_list, output=None):
    print("Merging BCFs")
    bcftools.merge("-l", file_list, "-O", "b", "-o", output, catch_stdout=False)
    print("Merge complete")
    index_bcf(output)
    return output


def index_bcf(bcf):
    print("Indexing BCF")
    bcftools.index(bcf, catch_stdout=False)
    print("Index complete")


def split_multiallelic(bcf, output):
    print("Splitting multiallelic sites")
    bcftools.norm("-m-any", "-o", output, "-O", "b", bcf, catch_stdout=False)
    index_bcf(output)
    print("Split complete")


def normalize_indels(vcf, output=None):
    print("Normalizing INDELs")
    fasta = get_fasta_hg38()
    bcftools.norm("-f", fasta, "-c", "s", "-O", "b", "-o", output, vcf, catch_stdout=False)
    index_bcf(output)
    print("Normalization complete")


def get_fasta_hg38():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    fasta_name = "hg38.fa.gz"
    #fasta_name = "pgx.grch38.fa"
    fasta_file = os.path.join(script_dir, "data", fasta_name)
    return fasta_file