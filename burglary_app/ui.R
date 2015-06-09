library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(

  # Application title
  titlePanel("Expected number of burglaries"),

  # Sidebar with a slider input for the number of bins
  sidebarLayout(
    sidebarPanel(
      helpText("Increased near-repeat probabilities."),

      selectInput("increase",
        label = "Choose increased probability type",
        choices = c("Marginal increase", "Baseline increase"),
        selected = "Marginal increase"),

      fileInput("file", label=h3("File input")),

      hr(),
      fluidRow(column(4, verbatimTextOutput("value")))),

    # Show a plot of the generated distribution
    mainPanel(plotOutput("distPlot"))
  )
))
