# plot_avgtagspervolume.R
data <- read.csv('results/avgtagspervolume.tsv', sep = '\t', header = FALSE)

p <- ggplot(data, aes(x = V1, y = V2)) + 
  geom_line(color = 'firebrick', size = 1) +
  theme_bw() + ggtitle('Mean number of genre categories per volume\nin the NovelTM dataset') +
  scale_x_continuous("") +
  scale_y_continuous(limits = c(0, 0.5), 'mean number of genre tags from Table 1\n') +
  theme(text = element_text(size = 16, family = "Avenir Next Medium"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black'),
        axis.text = element_text(color = 'black'),
        plot.title = element_text(size = 16, lineheight = 1.1),
        legend.position = 'none')

tiff("rplots/avgtagspervolume.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)