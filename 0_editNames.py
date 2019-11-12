#!/usr/bin/env python3

import os
from Bio import SeqIO
import sys
import glob

fasta_dir = sys.argv[1]
newdir = sys.argv[2]

fastas = glob.glob(fasta_dir + "/"  + "*.aas")

for i in fastas:

    clname = i.split("/")[-1]
    with open( newdir + "/" + clname , 'w' ) as handle:

        for seq in SeqIO.parse( i , "fasta" ):
            newname = seq.id.split(".")[0]

            handle.write( ">" + newname + "\n" )
            handle.write( str(seq.seq) + "\n" )


