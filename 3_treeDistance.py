#!/usr/bin/env python3

import dendropy as dp
import sys
import os
import pandas as pd
import numpy as np

treedir = sys.argv[1]
matrixfile = sys.argv[2]
clusters = os.listdir( treedir )

def dist_from_files( cl1, cl2 ):
    tns = dp.TaxonNamespace()
    t1 = dp.Tree.get_from_path(src = treedir + "/" +  cl1 + "/" + cl1 + ".phy_phyml_tree.txt",
            schema = "newick",
            taxon_namespace = tns )
    t2 = dp.Tree.get_from_path(src = treedir + "/" +  cl2 + "/" + cl2 + ".phy_phyml_tree.txt",  
            schema = "newick",
            taxon_namespace = tns )
    
    return dp.calculate.treecompare.symmetric_difference( t1, t2 )


# Initialize matrix

d_matrix = pd.DataFrame( 0, index = clusters, columns = clusters )


# Read trees in each cluster into list of trees


for i in range(0, len(clusters)):
    for j in range(i, len(clusters)):


        if i == j:
            d_matrix.at[clusters[i], clusters[j]] =  0 
        else:
            distance = dist_from_files( clusters[i], clusters[j] )
            d_matrix.at[ clusters[i], clusters[j] ] =  distance 
            d_matrix.at[  clusters[j], clusters[i] ] = distance


# Write distance matrix

d_matrix.to_csv( matrixfile  ,sep = ",")
         
            
    




