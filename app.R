
library(quantmod)
library(png)
library(jpeg)
library(shiny)

ui <- fluidPage(

  titlePanel("Bearish or Bullish?"),
  
  hr(),
  
  mainPanel(
    
    fluidRow(
      column(6, selectInput("ticker", "Enter a stock ticker:", c())),
      
      column(6, dateRangeInput("date", "Enter a date range:", start = Sys.Date() - 365))
    ),
    
    plotOutput("main")
    
  )
)

server <- function(input, output, session) {
  
  load("animals.RData")
  load("stocks.RData")
  
  suppressWarnings(updateSelectInput(session, "ticker",
                                     choices = stocks, selected = NA))
  
  output$main <- renderPlot({
    ticker <- input$ticker
    if (ticker == "") return()
    getSymbols(ticker)
    stock <- eval(parse(text = paste0(ticker, "$", ticker, ".Open")))
    l <- length(stock)
    start <- input$date[1]
    end <- input$date[2]
    dates <- as.Date(as.integer(start):as.integer(end))
    stock <- as.vector(stock[dates,])
    val <- Vectorize(function(animal) {
      stock <- stock[round(animal$x * length(stock) / animal$width)]
      suppressWarnings(cor(animal$y, stock))
    })
    
    if (stock[1] > stock[length(stock)]) species <- "Bears"
    else species <- "Bulls"
    
    vals <- val(eval(parse(text = tolower(species))))
    animal <- eval(parse(text = tolower(species)))
    animal <- animal[[which(vals > max(vals - 0.0001, na.rm = T))[1]]]
    print(animal$y)
    
    try(animal <- readPNG(paste(getwd(), species, animal$name, sep = "/")))
    try(animal <- readJPEG(paste(getwd(), species, animal$name, sep = "/")))
    y <- stock
    plot(1:length(y), seq(min(y), max(y), length = length(y)),
         type='n', main="Bearish", xlab="x", ylab="y")
    lim <- par()
    rasterImage(animal, lim$usr[1], lim$usr[3], lim$usr[2], lim$usr[4])
    grid()
    lines(1:length(y), y, lwd = 4)
  })
}

shinyApp(ui = ui, server = server)
