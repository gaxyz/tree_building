library( tidyverse )
library( pheatmap )
library(ape)
library(corrplot)
library(gridExtra)
setwd("~/Facultad/Taller de Bioinformatica/yuyo/tree_building/")


# Def function to easily get tree -------------
getTree <- function(name){
    treedir <- "./trees/"
    ext <- ".phy_phyml_tree.txt"
    fileName <- paste( treedir, name, ext, sep = "" )
    return( read.tree(fileName) )
}


# Load distance matrices --------------


d_methods <- c("euclidean",
               "symmetric",
               "weightedRF",
               "quartet",
               "triplet")
d_matrices <- list()
nmds_matrices <- list()
nmds_dims <- 3

for ( i in 1:length(d_methods)  ){

    distance_method <- d_methods[i]
    distance_file <- paste("tree-distance/",
                       distance_method,
                       "_distance.csv", sep = "")
    d_matrix <- read.csv(file = distance_file,
                  row.names = 1)  %>% as.matrix()

    d_matrices[[i]] <- d_matrix
    
    nmds_matrices[[i]] <- cmdscale( d_matrix, nmds_dims )
    
    
}

names( d_matrices ) <- d_methods
names( nmds_matrices ) <- d_methods

# Load concatenated data  ------
concat_d <- read.csv( file = "concatenated/distances/quartet_concatenated_distance.csv")
concat_tree <- read.tree("concatenated/concatenated.phy_phyml_tree.txt")




# Exploration   --------


t <- getTree(name = "cluster_437")
cophyloplot( t, concat_tree , rotate = TRUE)


corrplot(corr = d_matrix,
         is.corr = FALSE,
         diag = FALSE,method = "color",
         order = "hclust",
         hclust.method = "centroid",
         tl.pos = "n",)



 
## Explore matrices  --------------



d1<- nmds_matrices[["triplet"]]
d2 <- nmds_matrices[["euclidean"]]



corrplot( cor(d1, d2, method = "spearman") ,
          method = "number" )

pairs(d2)



















