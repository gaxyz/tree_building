library( dplyr )
library( pheatmap )
setwd("Facultad/Taller de Bioinformatica/yuyo/tree_building/")
rf <- read.csv(file = "tree-distance/rf_dist.csv",
              row.names = 1)  %>% as.matrix()

w_rf <- read.csv(file = "tree-distance/weightedRF_dist.csv",
                 row.names = 1)  %>% as.matrix() 

eucl <- read.csv(file = "tree-distance/euclidean_dist.csv",
                 row.names = 1)  %>% as.matrix() 


pheatmap(rf, fontsize_row = 0.1, 
         fontsize_col = 0.8 )

pheatmap(w_rf, fontsize_row = 0.1, 
         fontsize_col = 0.8 )
pheatmap(eucl, fontsize_row = 0.1, 
         fontsize_col = 0.8 )



