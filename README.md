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


./1\_alignment.py 1\_alignment.config.yaml
./2\_treeConstruction.py 2\_treeConstruction.config.yaml
./3\_treeDistance.py 3\_treeDistance.config.yaml

