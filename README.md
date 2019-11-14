# Treee Building

This is a repo that contains a pipeline for tree building and comparison of orthologous genes.

The pipelines here are not really robust in terms of data structure and naming, so special care must be taken when running it. For example, unaligned multifasta filenames should contain **only one** dot ("."), like `*.faa`.



### Set environment


With conda installed, run:

`conda env create -f conda_env.yaml`


`conda activate tree_building`


### Config files

Modify \*.config.yaml files accordingly (they come with default values).

### Run the scripts


`./1_alignment.py 1_alignment.config.yaml`


`./2_treeConstruction.py 2_treeConstruction.config.yaml`


`./3_treeDistance.py 3_treeDistance.config.yaml`




# Future useful modifications

1. BioPythonize applications (i.e. use biopython wrappers for phyml and muscle)
2. Modularize functions properly
3. Ditch config files except for large command line options. Replace them with argparse. 

 

