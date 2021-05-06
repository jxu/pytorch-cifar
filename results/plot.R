library(tidyverse)


plot_graphs <- function(filenames, title=NULL) {
  df <- data.frame()
  for (filename in filenames) {
    new_df <- read_csv(paste0(filename,".csv"))
    new_df <- new_df %>%
      mutate(model=filename,   
             train_error = 100 - train_acc,
             test_error = 100 - test_acc) %>%
      select(-train_loss, -test_loss, -train_acc, -test_acc)
    
    print(paste(filename, min(new_df$test_error)))

    df <- rbind(df, new_df)
  }
  
  #View(df)
  
  df <- df %>%
    pivot_longer(c(train_error, test_error), names_to="error_type", values_to="error")
  
  
  ggplot(df, aes(x=epoch, y=error, color=model, linetype=error_type)) +
    geom_line() +
    scale_x_continuous(name="Epoch", expand=c(0,0)) +
    scale_y_continuous(name = "Error (%)", limits=c(0,20), expand=c(0,0)) +
    scale_linetype_manual(name = "Dataset", values=c(test_error="solid", train_error="dashed"), 
                          labels=c(test_error="Test", train_error="Train")) +
    scale_color_manual(name = "Model", values=c("black", "red", "blue", "green")) +
    ggtitle(title) +
    theme_classic()

}

plot_graphs(c("res18_baseline", "res18_rect", "res18_ellipse", "res18_diamond"))
plot_graphs(c("res18_rect", "res18_rect2", "res18_rect3", "res18_rect4"))

