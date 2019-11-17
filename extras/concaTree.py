#!/usr/bin/env python3

import yaml
import sys
from Bio import AlignIO
import os
from Bio.Phylo.Applications._Phyml import PhymlCommandline


config_file = sys.argv[1]

# Read config 

with open( config_file, 'r' ) as handle:
    config = yaml.safe_load( handle )


alndir = config["alndir"]
outdir = config["outdir"]

# Read fasta containing dir

mfastas = []
for i in os.listdir( alndir ):
    if os.path.isfile( alndir + "/" + i ):
        mfastas.append( alndir + "/"  + i )




# Concatenate alignments
counter = 0
i = 0
als = len( mfastas )

for f in mfastas:

  counter += 1
  sys.stdout.write("\rConcatenating alignments... {0}/{1}".format(counter, als ) )
  sys.stdout.flush()
  alignment = AlignIO.read(f, "phylip")
  alignment.sort()  # sort the sequence identifiers so they match in all files
  if i==0:
    cat_algn = alignment
  else:
    cat_algn += alignment
  i += 1

# Write concatenated file

outfile =  outdir + "/" + "concatenated.phy"
sys.stdout.write("\r\nWriting concatenated file...\n")
outf = open(outfile , "w")
AlignIO.write(cat_algn, outf, "phylip")
outf.close()


sys.stdout.write("Done.\n")


# Construct tree

sys.stdout.write("Constructing tree using PhyML...\n")



phyml = PhymlCommandline(
        input = outfile,
        datatype = config["datatype"],
        model = config["subsmodel"],
        prop_invar = config["pinvariants"],
        alpha = config["gammashape"],
        nclasses = config["ratecategs"],
        bootstrap = config["bootstraps"],
        r_seed = config["rseed"]
        )


phyml()

sys.stdout.write( "Done.\n" )



























