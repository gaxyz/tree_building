library( tidyverse )
library( pheatmap )
library(ape)
library(corrplot)
library(gridExtra)
setwd("Facultad/Taller de Bioinformatica/yuyo/tree_building/")


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
matrices_list <- list()


for ( i in 1:length(d_methods)  ){

    distance_method <- d_methods[i]
    distance_file <- paste("tree-distance/",
                       distance_method,
                       "_distance.csv", sep = "")
    d_matrix <- read.csv(file = distance_file,
                  row.names = 1)  %>% as.matrix()

    matrices_list[[i]] <- d_matrix

}

names( matrices_list ) <- d_methods


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

m <- matrices_list["weightedRF"][[1]]

nmds <- cmdscale( m, 3 ) %>%
    as.data.frame() %>%
    rownames_to_column("cluster")

d12 <- ggplot(nmds) +
    geom_point( aes(x = V1, y = V2 ),
                size = 0.4, alpha = 0.8 )

d13 <- ggplot(nmds) +
    geom_point( aes(x = V1, y = V3 ),
                size = 0.4, alpha = 0.8  )

d23 <- ggplot(nmds) +
    geom_point( aes(x = V2, y = V3 ),
                size = 0.4, alpha = 0.8  )

size = rep(6,3)
grid.arrange( d12, d13, d23,
              ncol = 3, widths = size,
              heights = size )

