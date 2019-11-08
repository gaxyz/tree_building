#!/usr/bin/env python3

import dendropy
import sys
import os
import pandas as pd

treedir = sys.argv[1]
clusters = os.listdir( treedir )
# Read trees in each cluster into list of trees




treeList = []
for cluster_i in clusters:
    for cluster_j in clusters:
    




