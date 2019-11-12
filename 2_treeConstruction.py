#!/usr/bin/env python3
import sys
import yaml
import os
import subprocess
import glob
from joblib import Parallel, delayed



config_file = sys.argv[1]



# Move phylip files

def move_phylip(olddir, newdir):
    l = glob.glob( olddir + "/*.txt"   )
    for f in l:
        basename = f.split("/")[-1]
        os.rename( f, newdir + "/" + basename )


# Read config

with open( config_file, 'r' ) as handle:
    config = yaml.safe_load( handle )


aligned_dir = config[ "inputdir" ]
output_dir = config[ "outputdir" ]
threads = int( config["threads"] )

# Get paths to multifastas (only orthologs in each mfasta)
alignments = []

for item in os.listdir( aligned_dir ):
    if os.path.isfile( aligned_dir + "/" + item ) and ( item.split(".")[1] == "phy" ) :
        alignments.append( aligned_dir + "/" + item )



def phyml( al ):

    gene_name = al.split("/")[-1].split(".")[0]


    outdir = "{0}/{1}/".format(  output_dir, gene_name  )
    try:
        os.mkdir( outdir )
    except FileExistsError:
        pass

    tree_command = ["phyml", "-i", al,
                            "-d", config["datatype"],
                            "-m", config["subsmodel"],
                            "-v", config["pinvariants"],
                            "-a", config["gammashape"],
                            "-c", config["ratecategs"],
                            "-b", config["bootstraps"],
                            "--r_seed", config["rseed"]      ]
    sys.stdout.write("Running PhyML for {0}...".format(gene_name) )
    subprocess.run( tree_command , stdout = subprocess.DEVNULL )
    move_phylip( aligned_dir, outdir )


Parallel( n_jobs = threads)( delayed( phyml )(al) for al in alignments )
 








