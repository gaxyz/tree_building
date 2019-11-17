#!/usr/bin/env python3


import sys
from Bio import AlignIO
import os

alndir = sys.argv[1]
outfile = sys.argv[2]


mfastas = []
for i in os.listdir( alndir ):
    if os.path.isfile( alndir + "/" + i ):
        mfastas.append( alndir + "/"  + i )

for f in mfastas:

    
  alignment = AlignIO.read(f, "phylip")
  alignment.sort()  # sort the sequence identifiers so they match in all files
  print("Alignment of length %i" % alignment.get_alignment_length())
  if i==0:
    cat_algn = alignment
  else:
    cat_algn += alignment
  i += 1



outf = open(outfile, "w")
AlignIO.write(cat_algn, outfh, "phylip")
outfh.close()
