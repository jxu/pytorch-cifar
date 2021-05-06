library(tidyverse)


plot_graphs <- function(filenames) {
  df <- data.frame()
  for (filename in filenames) {
    new_df <- read_csv(paste0(filename,".csv"))
    new_df <- new_df %>%
      mutate(model=filename)
    
    df <- rbind(df, new_df)
  }
  df <- df %>%
    select(-train_loss, -test_loss) %>%
    mutate(train_error = 100 - train_acc,
           test_error = 100 - test_acc) %>%
    pivot_longer(c(train_error, test_error), names_to="error_type", values_to="error")
  
  ggplot(df, aes(x=epoch, y=error, color=model, linetype=error_type)) +
    geom_line() +
    scale_x_continuous(expand=c(0,0)) +
    scale_y_continuous(limits=c(0,20), expand=c(0,0)) +
    scale_color_manual(values=c("black", "red", "blue", "green")) +
    theme_classic()

}

plot_graphs(c("res18_baseline", "res18_rect", "res18_ellipse", "res18_diamond"))

