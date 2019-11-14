#!/usr/bin/env python3
import sys
import yaml
import os
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



def phyml( alignment  ):

    gene_name = alignment.split("/")[-1].split(".")[0]

    outdir = "{0}/{1}/".format(  output_dir, gene_name  )
    try:
        os.mkdir( outdir )
    except FileExistsError:
        pass

    tree_command = "phyml -i {0} -d {1} -m {2} -v {3} -a {4} -c {5} -b {6} --r_seed {7}".format(alignment,
                                                                                                                            config["datatype"],
                                                                                                                            config["subsmodel"],
                                                                                                                            config["pinvariants"],
                                                                                                                            config["gammashape"],
                                                                                                                            config["ratecategs"],
                                                                                                                            config["bootstraps"],
                                                                                                                            config["rseed"] )

    os.system(tree_command) 
   


Parallel( n_jobs = threads)( delayed( phyml )(al) for al in alignments )

trees = glob.glob(  "{0}/*.txt".format(  aligned_dir   )  )

for f in trees:

    filename = f.split("/")[-1]
    os.rename( f , "{0}/{1}".format( outdir, filename )   )










