#!/usr/bin/env python3
import sys
import yaml
import os
import subprocess
from Bio import AlignIO

config_file = sys.argv[1]

def convert_to_phylip( multifasta, overwrite = False ):

    newname = multifasta.split(".")[0] + ".phy"
    aln = AlignIO.read( multifasta, "fasta" )
    AlignIO.write( aln, newname, "phylip-relaxed" )
    
    if overwrite == True:
        os.remove( multifasta )




# Read config

with open( config_file, 'r' ) as handle:
    config = yaml.safe_load( handle )


unaligned_dir = config[ "inputdir" ]
output_dir = config["outputdir"]


# Get paths to multifastas (only orthologs in each mfasta)
mfastas = []

for item in os.listdir( unaligned_dir ):
    if os.path.isfile( unaligned_dir + "/" + item ):
        mfastas.append( unaligned_dir + "/" + item )




for mf in mfastas:

    gene_name = mf.split("/")[-1].split(".")[0]

    outfile = "{0}/{1}.aln".format(  output_dir, gene_name  )
    
    align_command = [ "muscle", "-in", mf ,"-out", outfile ,"-seqtype", config["seqtype"] ]

    subprocess.run( align_command )

    if config["phylip"] == "true":
        convert_to_phylip( outfile, overwrite = True )









        


