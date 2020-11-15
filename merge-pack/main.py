"""
Greg McInes
Altman Lab
gmcinnes@stanford.edu
"""

import argparse
import sys
from lib import merge_bcfs, split_multiallelic, normalize_indels

import os
from os import listdir


class MergePack(object):
    def __init__(self, debug=False):
        #self.fasta = fasta
        self.debug = debug

    def run(self):

        # Create file with list of files to merge
        self.create_file_list()

        # Merge the files
        merge_bcfs("merge_list.txt", "merged_pgx.multiallelic.bcf")

        # Split multiallelic sites
        #split_multiallelic("merged_pgx.multiallelic.bcf", "merged_pgx.split.bcf")
        split_multiallelic("merged_pgx.multiallelic.bcf", "output/merged_pgx.bcf")

        # Normalize INDELs
        #normalize_indels("merged_pgx.split.bcf", "output/merged_pgx.bcf")

    def create_file_list(self):
        # Get input files.  This will run on all files in ./input_data/
        input_files = self.get_input()
        print("Found %s files to process" % len(input_files))

        if len(input_files) == 0:
            print("No input files found.  Exiting.")
            exit()

        # Create a list of the files
        merge_file = open("merge_list.txt", "w")
        for f in input_files:
            print(f)
            merge_file.write("%s\n" % f)
        merge_file.close()

    def get_input(self):
        # get all the bcf files in a directory

        cwd = os.getcwd()
        input_dir = os.path.join(cwd, "input")
        contents = listdir(input_dir)

        bcf_files = []
        for f in contents:
            if f.endswith("bcf"):
                bcf_files.append(os.path.join("input", f))

        return bcf_files


"""
Parse the command line
"""
def parse_command_line():
    parser = argparse.ArgumentParser(
        description = 'This is a script I wrote')
    #parser.add_argument("--fasta", help="Indexed reference genome fasta file.  Index must be in the same location")
    parser.add_argument("-d", "--debug", action='store_true', default=False,
                                help="Output debugging messages.  May be very verbose.")
    options = parser.parse_args()
    return options


"""
Main
"""
if __name__ == "__main__":
    options = parse_command_line()
    mp = MergePack(debug=options.debug)
    mp.run()

