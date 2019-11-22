#!/usr/bin/env python3

import sys
import glob
import os
from Bio import SeqIO


fasta_dir = sys.argv[1]
outfile = sys.argv[2]

prot_dict ={}

for fasta in glob.glob(fasta_dir + "/" + "*.aas " ):
    for seq in SeqIO.parse( fasta, "fasta"):
        

        clname = fasta.split("/")[-1].split(".")[0]
        newname = seq.id + "_" clname

        prot_dict[newname] = str( seq.seq )

with open( outfile , 'r' ) as handle:

    for name in prot_dict:
        handle.write(  ">" + name + "\n"   )
        handle.write( prot_dict[name] + "\n" )


