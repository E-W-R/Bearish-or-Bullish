
"
curvesToRData.R (step 4)

Reads the information for each picture as a txt processed by mathify.py
and stores it as an RData object.
"


dissect <- function(animal, reversed) {
  info <- strsplit(animal, " ")[[1]]
  points <- strsplit(info[4:length(info)], ",")
  name = info[1]
  x <- as.integer(unlist(lapply(points, function(L) L[1])))
  if (reversed) {
    x <- rev(x)
    name <- paste0("-", name)
  }
  list(name = name,
       width = as.integer(info[2]), height = as.integer(info[3]),
       x = x, y = as.integer(unlist(lapply(points, function(L) L[2]))))
}

fileName <- "bearCurves.txt"
bears <- readChar(fileName, file.info(fileName)$size)
bears <- strsplit(bears, "\n")[[1]]
bears <- append(lapply(as.list(bears), dissect, reversed = FALSE),
                lapply(as.list(bears), dissect, reversed = TRUE))

fileName <- "bullCurves.txt"
bulls <- readChar(fileName, file.info(fileName)$size)
bulls <- strsplit(bulls, "\n")[[1]]
bulls <- append(lapply(as.list(bulls), dissect, reversed = FALSE),
                lapply(as.list(bulls), dissect, reversed = TRUE))

save(bears, bulls, file = "animals.RData")

stocks <- sort(stockSymbols()$Symbol)
save(stocks, file = "stocks.RData")

