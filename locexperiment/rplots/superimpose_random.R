# Superimposes LoC and Kirkus trajectories
# for the other-genre baseline

setwd('/Users/tunder/Dropbox/python/reviews/kirkus/genrexp/kirkusdeltas/')
library(ggplot2)

fishertransformdiff <- function(a, b) {
  transformeda <- atanh(a-1)
  transformedb <- atanh(b-1)
  
  difference = transformeda - transformedb
  return(tanh(difference))
}

data <- read.csv('kirkus_delta_results_uncut.tsv', sep = '\t')
data$fullrandomdiff <- fishertransformdiff(data$fullrandomdist, data$ingenredist)

kirkusdates = c()
kirkusdiffs = c()

for (i in 1934:2005) {
  thesediffs = data$fullrandomdiff[data$meandate >= i - 4 & data$meandate <= i + 4]
  kirkusdiffs = c(kirkusdiffs, median(thesediffs))
  kirkusdates = c(kirkusdates, i)
}

setwd('/Users/tunder/Dropbox/python/reviews/kirkus/genrexp2/')
data <- read.csv('../genrexp2/annotated_loc2_delta_results3.tsv', sep = '\t')
data$fullrandomdiff <- fishertransformdiff(data$fullrandomdist, data$ingenredist)

locdates = c()
locdiffs = c()

for (i in 1864:2005) {
  thesediffs = data$fullrandomdiff[data$meandate >= i - 4 & data$meandate <= i + 4]
  locdiffs = c(locdiffs, median(thesediffs))
  locdates = c(locdates, i)
}

locdiffs <- locdiffs[locdates >=1934]
locdates <- locdates[locdates >=1934]

df <- data.frame(meandate = c(locdates, kirkusdates),
                 diff = c(locdiffs, kirkusdiffs),
                 source = c(rep('loc', length(locdates)), rep('kirkus', length(kirkusdates))))

p <- ggplot(df, aes(x = meandate, y = diff, color = source)) + 
  geom_line(size = 1) +
  scale_color_manual(values = c('darkorchid3', 'darkolivegreen3')) +
  theme_bw() + ggtitle('Library of Congress and Kirkus\nfully random baseline') +
  scale_x_continuous("", breaks = c(1875, 1900, 1950, 2000)) +
  scale_y_continuous('difference between cosines') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16, lineheight = 1.1))

tiff("../genrexp2/rplots/superimposed_fullrandom.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)