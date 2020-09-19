# Plots the difference between in-genre comparisons and comparisons
# to volumes assigned to a different genre.
setwd('/Users/tunder/Dropbox/python/reviews/kirkus/genrexp2/')
library(ggplot2)

fishertransformdiff <- function(a, b) {
  transformeda <- atanh(a-1)
  transformedb <- atanh(b-1)
  
  difference = transformeda - transformedb
  return(tanh(difference))
}

data <- read.csv('../genrexp2/annotated_loc2_delta_results3.tsv', sep = '\t')
data$othergenrediff <- fishertransformdiff(data$othergenredist, data$ingenredist)
  
# first identify the peak year, considered as the year with the biggest
# positive correlation to y and negative thereafter
biggest = 0
peak = 1859
for (y in 1885 : 1995) {
  res1 = cor.test(data$meandate[data$meandate <= y], data$othergenrediff[data$meandate <= y])
  res2 = cor.test(data$meandate[data$meandate >= y], data$othergenrediff[data$meandate >= y])
  # we attempt correlation in both directions
  
  # we want a big positive correlation in the first half of the timeline
  # and negative in the second half
  # but to avoid maximizing one at the expense of the overall trend,
  # we also weight them by the number of results in that segment
  # of the timeline
  # (otherwise the endpoints could win)
  
  len1 = length(data$meandate[data$meandate <= y])
  len2 = length(data$meandate[data$meandate >= y])
  
  weightedgap = as.vector(res1$estimate) * len1 - as.vector(res2$estimate) * len2
  
  
  if (weightedgap > biggest) {
    # cat(y, gap, '\n')
    biggest <- weightedgap
    peak <- y
    pvalues <- c(res1$p.value, res2$p.value)
    rvalues <- c(res1$estimate, res2$estimate)
  }
}
cat('peak: ', peak, '\n')
cat(biggest, '\n')
cat(pvalues, '\n')
cat(rvalues, '\n')

dates = c()
diffs = c()
lower = c()
upper = c()

for (i in 1864:2005) {
  thesediffs = data$othergenrediff[data$meandate >= i - 4 & data$meandate <= i + 4]
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

p <- ggplot(df, aes(x = meandate, y = diff)) + 
  geom_line(color = 'cyan4', size = 1) +
  geom_ribbon(aes(ymin=lower, ymax=upper, x = meandate, fill = 'band'), fill = 'gray50', alpha = 0.3) +
  theme_bw() + ggtitle('Difference between in-genre and other-genre comparisons\nfor Library of Congress categories') +
  scale_x_continuous("", breaks = c(1875, 1900, 1950, 2000)) +
  scale_y_continuous('difference between cosines') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16, lineheight = 1.1),
        legend.position = 'none')

tiff("../genrexp2/rplots/othergenrediffs_cosdeltas3.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)