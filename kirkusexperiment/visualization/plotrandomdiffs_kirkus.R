# Plots the difference between in-genre comparisons and comparisons
# to volumes assigned to a different genre.

fishertransformdiff <- function(a, b) {
  transformeda <- atanh(a-1)
  transformedb <- atanh(b-1)
  
  difference = transformeda - transformedb
  return(tanh(difference))
}
setwd('/Users/tunder/Dropbox/python/reviews/kirkus/genrexp/kirkusdeltas/')
library(ggplot2)
data <- read.csv('kirkus_delta_results_uncut.tsv', sep = '\t')
data$fullrandomdiff <- fishertransformdiff(data$fullrandomdist, data$ingenredist)


dates = c()
diffs = c()
lower = c()
upper = c()

for (i in 1934:2005) {
  thesediffs = data$fullrandomdiff[data$meandate >= i - 4 & data$meandate <= i + 4]
  replication = c()
  for (j in 1:1000) {
    bootstrap = sample(thesediffs, size = length(thesediffs), replace = TRUE)
    replication <- c(replication, median(bootstrap))
  }
  replication <- sort(replication)
  diffs = c(diffs, median(replication))
  lower <- c(lower, replication[25])
  upper <- c(upper, replication[975])
  dates = c(dates, i)
}

df <- data.frame(meandate = dates, diff = diffs, upper = upper, lower = lower)

p <- ggplot(df) + 
  geom_line(aes(x = meandate, y = diff), color = 'dodgerblue', size = 1) +
  geom_ribbon(aes(ymin=lower, ymax=upper, x = meandate, fill = 'band'), fill = 'gray50', alpha = 0.3) +
  theme_bw() + ggtitle('Difference between in-genre and random comparisons\nfor genres in Kirkus') +
  scale_x_continuous("", breaks = c(1875, 1900, 1950, 2000)) +
  scale_y_continuous('difference between cosines') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16, lineheight = 1.1),
        legend.position = 'none')

tiff("randomdiffs_kirkusdeltas.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)