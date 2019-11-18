#!/usr/bin/env python3


import dendropy as dp
import sys
import os
import pandas as pd
import numpy as np
import yaml
import subprocess
import shutil
import glob


config_file = sys.argv[1]


with open( config_file, 'r' ) as handle:
    config = yaml.safe_load( handle )


concatenated = config["concatenated"]
treedir = config["treedir"]
outdir = config["outdir"]
distance_method = config["distance_method"]
treefiles = glob.glob( treedir + "/" + "*"  + ".phy_phyml_stats.txt"   )
clusters = []
for i in treefiles:
    
    clusters.append( i.split("/")[-1].split(".")[0] )



# Define distance calculating functions

def quartet_distance(t1, t2 ):
    # write temp tree files
    os.mkdir( ".tmp"  )
    t1.write(path=".tmp/t1.nwk", schema="newick")
    t2.write( path = ".tmp/t2.nwk" , schema = "newick" )
    # run tqdist
    process = ["quartet_dist", ".tmp/t1.nwk", ".tmp/t2.nwk"]
    proc = subprocess.Popen( process , stdout = subprocess.PIPE )
    out = proc.communicate()[0].strip()
    # remove tmp dir
    shutil.rmtree(".tmp")

    return float( out )




def triplet_distance(t1, t2 ):
    # write temp tree files
    os.mkdir( ".tmp"  )
    t1.write(path=".tmp/t1.nwk", schema="newick")
    t2.write( path = ".tmp/t2.nwk" , schema = "newick" )

    # run tqdist triplet distance

    process = ["triplet_dist", "-v", ".tmp/t1.nwk", ".tmp/t2.nwk"]
    proc = subprocess.Popen( process , stdout = subprocess.PIPE )
    out = proc.communicate()[0].strip()

    # remove tmp dir
    shutil.rmtree( ".tmp" )

    return float( out )


def dist_from_files( cl1, cl2, distance_method = False ):
    if distance_method  == False:
        print("ERROR: must provide distance method")
        sys.exit(1)

    distance = {
            "symmetric" : dp.calculate.treecompare.symmetric_difference,
            "weightedRF": dp.calculate.treecompare.weighted_robinson_foulds_distance,
            "euclidean" : dp.calculate.treecompare.euclidean_distance,
            "quartet": quartet_distance,
            "triplet": triplet_distance
            }

    tns = dp.TaxonNamespace()
    t1 = dp.Tree.get_from_path(src = treedir + "/" + cl1 + ".phy_phyml_tree.txt",
            schema = "newick" )
    t2 = dp.Tree.get_from_path(src = cl2 ,
            schema = "newick",
            taxon_namespace = t1.taxon_namespace )

    try:
        distance = distance[distance_method]( t1, t2 )
    except KeyError:
        "ERROR: distance method {0} not found".format(distance_method)
        sys.exit(1)

    return distance

# Initialize matrix

d_matrix = pd.DataFrame( 0, index = clusters, columns = [ distance_method ] )





# Read trees in each cluster into list of trees

msg = "\n# Compare trees to concatenated tree using {0} #\n".format(distance_method)

print("#"*(len(msg)-2) + msg  + "#"*(len(msg)-2) + "\n"  )
counter = 0
total_comps = len(clusters)
for i in range(0, len(clusters)):
    counter += 1
    log = "Comparison {0}/{1}".format(counter, total_comps)
    sys.stdout.write("\r{0}".format(log))
    sys.stdout.flush()

    distance = dist_from_files( clusters[i], concatenated, distance_method = config["distance_method"] )
    d_matrix.at[clusters[i], distance_method ] = distance


print("\n")



# Write distance matrix

d_matrix.to_csv( outdir + "/" + config["distance_method"] + "_concatenated_distance.csv"  ,sep = ",")


 














