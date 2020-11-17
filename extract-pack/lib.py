import sys
import os
import pysam
import pysam.bcftools as bcftools
from subprocess import Popen, PIPE

"""
Normalize chromosome names.  Sometimes chromosomes are listed as just numbers, other times they start with 'chr'. 
This function strips the 'chr' and returns just the chromosome number, if applicable.

Inputs: 
    chr: variable containing chromosome id
Returns:
    chr with 'chr' stripped from beginning.

"""
def clean_chr(chr, prefix=False):
    if prefix is False:
        if isinstance(chr, int):
            return chr
        if chr.startswith('chr'):
            return chr.replace("chr", "")
    else:
        if not chr.startswith('chr'):
            return "chr%s" % chr
        return chr

'''
This function parses a line from a VCF into an object with some useful functions.

Inputs:
    line: A string directly from a VCF representing an entire row of call data.
Returns:
    VCFfields object
'''
def parse_vcf_line(line):
    CHROM = 0
    POS = 1
    ID = 2
    REF = 3
    ALT = 4
    QUAL = 5
    FILTER = 6
    INFO = 7
    FORMAT = 8
    calls = 9

    if isinstance(line, list) is True:
        fields = line
    else:
        fields = line.rstrip().split()

    class VCFfields(object):
        def __init__(self):
            self.chrom = None
            self.pos = None
            self.id = None
            self.ref = None
            self.alt = None
            self.qual = None
            self.filter = None
            self.info = {}
            self.format = None
            self.calls = []
            self.gt_index = None

        def print_row(self, chr=True, minimal=False, return_string=False):
            info_print_format = self.format_info()
            calls_print_format = "\t".join(self.calls)
            if chr:
                # If I want to make sure the output has chr on the chromosome, do this.  Kind of messy but works.
                #chrom = "chr%s" % clean_chr(self.chrom)
                chrom = clean_chr(self.chrom, prefix=True)
            else:
                chrom = self.chrom
            if minimal is True:
                out = "%s\t%s\t%s\t%s\t%s" % (chrom, self.pos, self.id, self.ref, self.alt)

            else:
                out = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (chrom, self.pos, self.id, self.ref, self.alt,
                                                                  self.qual, self.filter, info_print_format,
                                                                  self.format, calls_print_format)
            if return_string is True:
                return out
            else:
                print(out)

        def intake_info(self, info):
            fields = info.split(';')
            for f in fields:
                try:
                    key, value = f.split("=")
                    self.info[key] = value
                except:
                    pass

        def format_info(self):
            output = []
            if len(self.info) == 0:
                return "."
            for key, value in self.info.items():
                output.append("%s=%s" % (key, value))

            if len(output) == 0:
                return "."

            return ";".join(output)

        def add_info(self, key, value):
            self.info[key] = value

        def add_allele(self, new):
            if new == self.alt:
                return
            self.alt += ",%s" % new

        def make_multiallelic(self, new_vcf):
            self.add_allele(new_vcf.alt)
            # add the info
            for i in new_vcf.info:
                self.add_info(i, new_vcf.info[i])
            # update the genotypes
            for i in range(len(new_vcf.calls)):
                if "/" in new_vcf.calls[i]:
                    alleles = new_vcf.calls[i].split("/")
                elif "|" in new_vcf.calls[i]:
                    alleles = new_vcf.calls[i].split("|")
                else:
                    print("Unrecognized delimiter!")
                    print(new_vcf.calls[i])
                    exit()

                alt_found = False

                n_alts = str(len(self.alts()))

                if alleles[0] == '1':
                    alleles[0] = n_alts
                    alt_found = True
                if alleles[1] == '1':
                    alleles[1] = n_alts
                    alt_found = True
                if alt_found:
                    self.calls[i] = "/".join(alleles)

        def alts(self):
            return self.alt.split(",")

        def is_multiallelic(self):
            if len(self.alts()) == 1:
                return False
            return True

        def max_insertion(self):
            max_insert = 1
            for a in self.alts():
                if len(a) > max_insert:
                    max_insert = len(a)
            return max_insert

        def is_indel(self):
            if len(self.ref) > 1 or len(self.alt) > 1:
                return True
            return False

    fields = list((fields))

    row = VCFfields()
    row.chrom = fields[CHROM]
    row.pos = int(fields[POS])
    row.id = fields[ID]
    row.ref = fields[REF]
    row.alt = fields[ALT]
    row.qual = fields[QUAL]
    row.filter = fields[FILTER]
    row.intake_info(fields[INFO])
    if len(fields) > 8:
        row.format = fields[FORMAT]
        row.calls = fields[calls:]

    #row = VCFfields()
    #row.chrom = fields.chrom
    #row.pos = fields.pos
    #row.id = fields.id
    #row.ref = fields.ref
    #row.alt = fields.alts[0]
    #row.qual = fields.qual
    #row.filter = fields.filter
    #row.intake_info(fields.info)
    #row.format = fields.format
    #row.calls = fields.samples

    return row

'''
Read a VCF and return the subject IDs
'''
def get_vcf_subject_ids(vcf):
    ids = []
    with smart_open(vcf) as f:
        for line in f:
            try:
                line = byte_decoder(line)
            except:
                line = line
            if line.startswith("#CHROM"):
                fields = line.rstrip().split()
                ids = fields[9:]
                break
    return ids


'''
Detect if a file is gzipped before opening.  If it is open with gzip, otherwise open normally.
'''
def smart_open(file):
    if file.endswith('gz'):
        import gzip
        return gzip.open(file)
    return open(file)

'''
Decode byte data into utf-8
'''
def byte_decoder(a):
    return a.decode("utf-8")


'''
Split a genotype string into an array
'''
def split_genotype(gt):
    gt = gt.split(":")[0]
    if "/" in gt:
        alleles = gt.split("/")
        return alleles
    elif "|" in gt:
        alleles = gt.split("|")
        return alleles
    print("Unrecognized delimiter! %s" % gt, file=sys.stderr)
    gt = [None, None]
    return gt

'''
Determine if a VCF encodes chromosome names with "chr" preceding the chromosome number.
'''
def chr_string(vcf):
    with smart_open(vcf) as f:
        for line in f:
            try:
                line = byte_decoder(line)
            except:
                line = line
            if line.startswith("#"):
                continue
            if line.startswith("chr"):
                f.close()
                return True
            else:
                f.close()
                return False


def extract_regions_tabix(vcf, chromosome, start, end):
    print(vcf, chromosome, start, end)
    tb = tabix.open(vcf)
    records = tb.query("%s" % chromosome, start, end)
    return records

def extract_regions_bcftools(vcf, chromosome, start, end):
    print(vcf, chromosome, start, end)
    file = pysam.VariantFile(vcf)
    records = file.fetch(chromosome, start, end)

    parsed = []
    for r in records:
        parsed.append(str(r).split())

    return parsed


def gt_splitter(gt):
    if "/" in gt:
        alleles = gt.split("/")
    elif "|" in gt:
        alleles = gt.split("|")
    else:
        alleles = None
    return alleles


def get_output_name(file):
    file_name = os.path.basename(file)
    base = file_name.split(".vcf")[0]
    output_name = base + ".pgx.vcf"
    output_path = os.path.join("output", output_name)
    return output_path

def break_blocks(vcf, fasta, output, index, bed=None, filter=False, debug=False):
    # Write a new vcf by extracting calls from the input vcf and breaking apart reference call blocks

    # Get the bed regions
    if bed:
        regions = get_bed_regions(bed)
    else:
        print("Bed file currently required")
        exit(1)

    pgx_variants = get_pgx_variants()

    outfilename = get_output_name(vcf)

    # Set up the output
    outfile = open(outfilename, "w")

    # Print the header
    header = get_header(vcf)
    outfile.write(header)

    # Check the format of the chromosome names in the VCF
    chr_prefix = vcf_chr_format(vcf)

    # For each region get the calls
    for r in regions:
        chr = r['chr']
        start = r['start']
        stop = r['end']

        if chr_prefix is False:
            chr = clean_chr(chr)

        #records = extract_regions_tabix(vcf, chr, start, stop)
        records = extract_regions_bcftools(vcf, chr, start, stop)

        for r in records:

            # todo: Quality filtering

            vcf_row = parse_vcf_line(r)

            # Quality filtering.  Could be more robust.  Need to see the data first.
            if filter is True:
                if vcf_row.filter != "PASS":
                    continue


            # Clean up the FORMAT, and GT columns - This removes all quality info!
            vcf_row.format = "GT"

            for i in range(len(vcf_row.calls)):
                vcf_row.calls[i] = vcf_row.calls[i].split(":")[0]

            if "END" in vcf_row.info:
                # It's a block!  Break it

                begin = vcf_row.pos
                end = int(vcf_row.info["END"])



                r[0] = clean_chr(r[0], prefix=True)
                r[4] = '.'
                #out = "\t".join(r)
                #outfile.write(out + "\n")

                for i in range(begin, end+1):
                    record_out = r.copy()

                    vcf_row_blocked = parse_vcf_line(record_out)
                    vcf_row_blocked.pos = str(i)

                    #record_out[1] = str(i)


                    # Check if the position is in any definitions
                    # If it's not we don't really care about adding a reference call
                    #if "%s_%s" % (clean_chr(record_out[0], prefix=True), record_out[1]) not in pgx_variants:
                    if "%s_%s" % (clean_chr(vcf_row.chrom, prefix=True), vcf_row_blocked.pos) not in pgx_variants:
                        #print("bad variant")
                        continue


                    #print("i am printing")
                    #record_out[3] = fasta_extract(chr, i, i)
                    #vcf_row_blocked.ref = fasta_extract(chr, i, i)
                    vcf_row_blocked.ref = fasta_extract(chr, i, i, fasta)
                    vcf_row_blocked.alt = "."
                    #record_out[4] = "."

                    #record_out[4] = "."
                    #out = "\t".join(record_out)
                    #outfile.write(out + "\n")

                    # Clear the info
                    vcf_row_blocked.info = {}

                    # Clean up the FORMAT, and GT columns - This removes all quality info!
                    vcf_row_blocked.format = "GT"

                    for i in range(len(vcf_row_blocked.calls)):
                        vcf_row_blocked.calls[i] = vcf_row_blocked.calls[i].split(":")[0]

                    out = vcf_row_blocked.print_row(chr=True, return_string=True)
                    outfile.write(out + "\n")


            else:
                # It's a variant.  Print it!
                alts = []
                for a in vcf_row.alts():
                    #print(a)
                    if a != '<NON_REF>':
                        alts.append(a)
                if len(alts) == 0:
                    vcf_row.alt = '.'
                else:
                    vcf_row.alt = ",".join(alts)
                #print(vcf_row.alt)

                # Clear the INFO
                vcf_row.info = {}

                out = vcf_row.print_row(chr=True, return_string=True)
                outfile.write(out + "\n")

    # I would like to normalize indels here but it hasn't been working

    outfile.close()

    bcf = vcf2bcf(outfilename)

    normalized_bcf = normalize_indels(bcf)

    # verify that the number of records is the same between the two
    vcf_count = count_variants(outfilename)
    norm_count = count_variants(normalized_bcf)

    if vcf_count != norm_count:
        # something bad happened.  Log it
        print("Number of records unequal between vcf and normalized bcf.  Something happened.")

    # Clean up output
    os.remove(outfilename)
    os.remove(bcf)
    #os.rename(normalized_bcf, bcf)
    #os.rename(normalized_bcf + ".csi", bcf + ".csi")

    # (pbilling) Delocalization of outputs is controlled by dsub
    #   so we need to use the paths it generates for all outputs
    os.rename(normaized_bcf, output)
    os.rename(normalized_bcf + ".csv", index)


def normalize_indels(vcf, output=None):
    if output is None:
        #output = vcf.rstrip(".vcf") + ".norm.vcf"
        output = vcf.rstrip(".bcf") + ".norm.bcf"

    fasta = get_fasta_hg38()
    bcftools.norm("-f", fasta, "-c", "s", "-O", "b", "-o", output, vcf, catch_stdout=False)
    index_bcf(output)
    return output


def vcf2bcf(vcf, output=None):
    if output is None:
        output = vcf.rstrip(".vcf") + ".bcf"
    bcftools.view("-O", "b", "-o", output, vcf, catch_stdout=False)
    index_bcf(output)
    return output


def index_bcf(bcf):
    bcftools.index(bcf, catch_stdout=False)


def count_variants(vcf):
    records = bcftools.view(vcf)
    records = records.split('\n')

    count = 0
    for r in records:
        if not r.startswith("#"):
            count += 1

    return count


def get_pgx_bed():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    bed_name = "pgx.grch38.bed"
    bed_file = os.path.join(script_dir, "data", bed_name)
    return bed_file

def get_fasta_hg38():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    fasta_name = "hg38.fa.gz"
    #fasta_name = "pgx.grch38.fa"
    #fasta_file = os.path.join(script_dir, "data", fasta_name)
    fasta_file = os.path.join("/workspace/input", fasta_name)
    return fasta_file

def get_pgx_variants():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = "definition_variants.txt"
    file_path = os.path.join(script_dir, "data", file_name)
    variants = []
    with open(file_path) as f:
        for line in f:
            fields = line.rstrip().split()
            variants.append("%s_%s" % (fields[0], fields[1]))
    return variants

def get_bed_regions(bed):
    regions = []
    with open(bed) as f:
        for line in f:
            fields = line.rstrip().split()
            chr = clean_chr(fields[0], prefix=True)
            start = int(fields[1])
            end = int(fields[2])
            gene = fields[3]
            new_region = {"chr": chr,
                          "start": start,
                          "end": end,
                          "gene": gene}
            regions.append(new_region)
    return regions

def get_header(vcf):
    header = ''
    with smart_open(vcf) as f:
        for line in f:
            try:
                line = byte_decoder(line)
            except:
                line = line
            if line.startswith("#"):
                header += line
            else:
                return header


def vcf_chr_format(vcf):
    with smart_open(vcf) as f:
        for line in f:
            try:
                line = byte_decoder(line)
            except:
                line = line
            if line.startswith("#"):
                continue
            fields = line.rstrip().split()
            chr = fields[0]
            if chr.startswith("chr"):
                return True
            else:
                return False
    return None



def bgzip(filename):
    """Call bgzip to compress a file."""
    cmd = ['bgzip', '-f', filename]
    Popen(cmd)

def tabix_index(filename, preset="vcf"):
    """Call tabix to create an index for a bgzip-compressed file."""
    cmd = ['tabix', '-p', preset, filename]
    print(" ".join(cmd))
    Popen(cmd)

def fasta_extract(chr, start, end, fasta=None):

    if fasta is None:
        fasta = get_fasta_hg38()

    region = "%s:%s-%s" % (clean_chr(chr, prefix=True), start, end)
    response = pysam.faidx(fasta, region)
    sequence = response.split("\n")[1].upper()
    return sequence

