library(shiny)
library(tidyverse)

# Load data
df <- read.csv("../data/breast-cancer.csv", stringsAsFactors = FALSE)

numeric_vars <- df %>% select(where(is.numeric)) %>% colnames()

ui <- fluidPage(
  
  titlePanel("Breast Cancer EDA Dashboard"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("variable", "Choose a variable:", choices = numeric_vars)
    ),
    
    mainPanel(
      h3("Summary Statistics"),
      tableOutput("summary_table"),
      
      h3("Distribution"),
      plotOutput("hist_plot"),
      
      h3("Outlier Detection (Boxplot)"),
      plotOutput("box_plot")
    )
  )
)

server <- function(input, output) {
  
  selected_data <- reactive({
    df[[input$variable]]
  })
  
  output$summary_table <- renderTable({
    data.frame(
      Min = min(selected_data(), na.rm = TRUE),
      Q1 = quantile(selected_data(), 0.25, na.rm = TRUE),
      Median = median(selected_data(), na.rm = TRUE),
      Mean = mean(selected_data(), na.rm = TRUE),
      Q3 = quantile(selected_data(), 0.75, na.rm = TRUE),
      Max = max(selected_data(), na.rm = TRUE),
      SD = sd(selected_data(), na.rm = TRUE)
    )
  })
  
  output$hist_plot <- renderPlot({
    hist(selected_data(),
         col = "skyblue",
         border = "white",
         main = paste("Distribution of", input$variable),
         xlab = input$variable)
  })
  
  output$box_plot <- renderPlot({
    boxplot(selected_data(),
            col = "salmon",
            main = paste("Outliers in", input$variable),
            horizontal = TRUE)
  })
}

shinyApp(ui = ui, server = server)
