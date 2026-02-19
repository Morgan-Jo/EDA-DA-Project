# Load libraries
library(tidyverse)
library(skimr)

# Load data
data_path <- "data/breast-cancer.csv"
df <- read.csv(data_path, stringsAsFactors = FALSE)

# 1. Understand data structure
glimpse(df)
str(df)

# Check missing values
missing_summary <- colSums(is.na(df))
print(missing_summary)

# 2. Summary statistics
summary(df)

# More detailed summary for numeric variables
skim(df)

# Select numeric columns only
numeric_df <- df %>% select(where(is.numeric))

# 3. Visualise distributions
dist_plot <- numeric_df %>%
  pivot_longer(cols = everything()) %>%
  ggplot(aes(value)) +
  facet_wrap(~ name, scales = "free") +
  geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7) +
  theme_minimal() +
  labs(title = "Distributions of Numeric Features")

# Show plot
print(dist_plot)

# Save plot
ggsave(
  filename = "outputs/plots/feature_distributions.png",
  plot = dist_plot,
  width = 12,
  height = 8,
  dpi = 300
)

# 4. Outlier detection using IQR
detect_outliers <- function(x) {
  Q1 <- quantile(x, 0.25, na.rm = TRUE)
  Q3 <- quantile(x, 0.75, na.rm = TRUE)
  IQR <- Q3 - Q1
  which(x < (Q1 - 1.5 * IQR) | x > (Q3 + 1.5 * IQR))
}

outlier_counts <- sapply(numeric_df, function(col) length(detect_outliers(col)))
print(outlier_counts)

# 5. Boxplot for anomaly detection
boxplot_plot <- numeric_df %>%
  pivot_longer(cols = everything()) %>%
  ggplot(aes(x = name, y = value)) +
  geom_boxplot(fill = "darkgreen", alpha = 0.6) +
  theme_minimal() +
  coord_flip() +
  labs(title = "Outlier Detection Across Features")

# Show plot
print(boxplot_plot)

# Save plot
ggsave(
  filename = "outputs/plots/outlier_boxplots.png",
  plot = boxplot_plot,
  width = 12,
  height = 8,
  dpi = 300
)
