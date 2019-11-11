#!/usr/bin/env python3

import dendropy as dp
import sys
import os
import pandas as pd
import numpy as np
import yaml



config_file = sys.argv[1] 

# Read config
with open( config_file, 'r' ) as handle:
    config = yaml.safe_load( handle )

treedir = config["treedir"]
matrixfile = config["matrixfile"]
distance_method = config["distance_method"]
clusters = os.listdir( treedir )


# Define distance calculating functions

def dist_from_files( cl1, cl2, distance_method = False ):
    if distance_method  == False:
        print("ERROR: must provide distance method")
        sys.exit(1)

    distance = {
            "symmetric" : dp.calculate.treecompare.symmetric_difference,
            "weightedRF": dp.calculate.treecompare.weighted_robinson_foulds_distance,
            "euclidean" : dp.calculate.treecompare.euclidean_distance
            }





    tns = dp.TaxonNamespace()
    t1 = dp.Tree.get_from_path(src = treedir + "/" +  cl1 + "/" + cl1 + ".phy_phyml_tree.txt",
            schema = "newick",
            taxon_namespace = tns )
    t2 = dp.Tree.get_from_path(src = treedir + "/" +  cl2 + "/" + cl2 + ".phy_phyml_tree.txt",  
            schema = "newick",
            taxon_namespace = tns )
    
    try:
        distance = distance[distance_method]( t1, t2 )
    except KeyError:
        "ERROR: distance method {0} not found".format(distance_method)
        sys.exit(1)

    return distance


# Initialize matrix

d_matrix = pd.DataFrame( 0, index = clusters, columns = clusters )


# Read trees in each cluster into list of trees


for i in range(0, len(clusters)):
    for j in range(i, len(clusters)):

        log = "Measuring {0} distance between {1} and {2}".format(distance_method, clusters[i], clusters[j])
        if i == j:
            print(log)
            d_matrix.at[clusters[i], clusters[j]] =  0 

        else:
            print(log)
            distance = dist_from_files( clusters[i], clusters[j], distance_method = config["distance_method"] )
            d_matrix.at[ clusters[i], clusters[j] ] =  distance 
            d_matrix.at[  clusters[j], clusters[i] ] = distance


# Write distance matrix

d_matrix.to_csv( matrixfile  ,sep = ",")
         
            
    




