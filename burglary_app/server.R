library(shiny)
knox_merge_77 <- read.csv("/Users/louisegeraghty/Documents/Knox_coef_matrix/burglary_app/data/knox_merge_50.csv")

# Define server logic required to draw a histogram
shinyServer(function(input, output) {

  # Expression that generates a histogram. The expression is
  # wrapped in a call to renderPlot to indicate that:
  #
  #  1) It is "reactive" and therefore should re-execute automatically
  #     when inputs change
  #  2) Its output type is a plot

  output$distPlot <- renderPlot({
    #Render a barplot
    Area_50_Score_Freq    <- knox_merge_50[,1]
            ylab="Expected value"
            xlab="Block"

    hist(Area_50_Score_Freq, col = 'darkgray', border = 'white')


  })
})
