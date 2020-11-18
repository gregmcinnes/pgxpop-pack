"""
Greg McInes
Altman Lab
gmcinnes@stanford.edu
"""

import argparse
import sys
from lib import get_pgx_bed, break_blocks

import os
from os import listdir


'''
Change the input back to what it was before.  Provide a vcf from the command line as input.vcf.gz
Then extract the name from the header and use that as the prefix
'''


class ExtractPack(object):
    def __init__(self, vcf, fasta, output, index, bed=None, debug=False):
        self.vcf = vcf
        self.fasta = fasta
        self.bed = bed
        self.output = output
        self.index = index
        self.debug = debug

        if self.bed is None:
            self.bed = get_pgx_bed()

    def run(self):

        # (pbilling) Commenting out: only run on single VCF which 
        #   is managed in container by dsub
        # Get input files.  This will run on all files in ./input_data/
        #input_files = self.get_input()


        #input_file = os.path.join("input_data", self.file)
        #input_files = [input_file]

        #print("Found %s files to process" % len(input_files))

        #if len(input_files) == 0:
        #    print("No input files found.  Exiting.")
        #    exit()

        # This will actually be a single step with a bed file passed to break blocks
        # Output will automaticaly be written to the output directory.  The VCF will be named based on the input VCF.

        #for f in input_files:
        #    print("Processing %s" % f)
        break_blocks(
                     vcf = self.vcf, 
                     fasta = self.fasta, 
                     output = self.output,
                     index = self.index, 
                     bed = self.bed,
                     debug = self.debug)

    def get_input(self):
        # get all the vcf.gz files in a directory

        cwd = os.getcwd()
        input_dir = os.path.join(cwd, "input")
        contents = listdir(input_dir)

        vcf_files = []
        for f in contents:
            if f.endswith("vcf.gz"):
                vcf_files.append(os.path.join("input", f))

        return vcf_files


"""
Parse the command line
"""
def parse_command_line():
    parser = argparse.ArgumentParser(
        description = 'This is a script I wrote')
    parser.add_argument("-v", "--vcf", required=True, help="gVCF to process")
    parser.add_argument("-b", "--bed", help="Bed file for subsetting genotypes")
    parser.add_argument("--fasta", required=True, help="Indexed reference genome fasta file.  Index must be in the same location")
    parser.add_argument("-o", "--output", required=True, help="Output bcf file")
    # (pbilling) Specifying index name because dsub needs to manage 
    #   file paths of all inputs/outputs in order to do delocalize
    #   to Google Cloud Storage
    parser.add_argument("-i", "--index", required=True, help="Output bcf index")
    parser.add_argument("-d", "--debug", action='store_true', default=False,
                                help="Output debugging messages.  May be very verbose.")
    options = parser.parse_args()
    return options


"""
Main
"""
if __name__ == "__main__":
    print("Running VCF extraction")
    options = parse_command_line()
    ep = ExtractPack(
                     vcf=options.vcf,
                     bed=options.bed,
                     fasta=options.fasta,
                     output=options.output,
                     index=options.index,
                     debug=options.debug)
    print(f"Options: {options}.")
    ep.run()

