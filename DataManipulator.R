x <- read.csv("EPI2016_Final_resampling.csv")

x$iso <- as.character(x$iso)
x$country <- as.character(x$country)

RowsWithNA <- c()

# Remove all the rows with NA values only in:
# "code"  "iso" "country"  "variable" "year"
for (i in 1:5) 
{
    RowsWithNA <- union(which(is.na(x[,i]) == T), RowsWithNA)
}

if (length(RowsWithNA) > 0)
{
  x <- x[-c(RowsWithNA),]
  print("Following Rows Deleted")
  print(RowsWithNA)
}


# Print only those variables which don't have 2330 occurences
# All variables should have 2330 total occurences in the data
sum(x$variable == "ACSAT")

for (i in unique(x$variable)) 
{
  if(sum(x$variable == i) != 2330)
  {
    print(c(i, sum(x$variable == i)))
  }
}



#Create 43 csv's, one for each variable
for (var in unique(x$variable)) 
{
  #Create an empty data frame z, which will be written to a csv
  z <- data.frame(code=integer(234),
                  iso=character(234),
                  country=character(234),
                  stringsAsFactors=FALSE)
  z[1,] <- c(0, "0", "0")
  
  for (i in '2007':'2016')
  {
    for (j in c("lower", "median", "upper"))
    {
      column_name <- paste(j, i, sep = "_")
      z[, column_name] <- 0
    }
  }

  
  ptm <- proc.time()
  #Process countries sequentially
  for (i in 1:length(unique(x$iso))) 
  {
    subset_x <- x[x$variable == var,]
    subset_x <- subset_x[subset_x$iso == unique(subset_x$iso)[i],]
    
    # add all of that country's data to z
    for (j in 1:nrow(subset_x))
    {
      column_names <- c("lower", "median", "upper")
      column_names <- paste(column_names, as.character(subset_x[j, "year"]), sep = "_")
      
      # first occurence of this particular country
      if (j == 1)
      {
        z[i, c('code', 'iso', 'country', column_names)] <- subset_x[j, -c(4,5)]
        z[i, c('iso')] <- as.character(subset_x[j, c('iso')])
      }
      
      else
      {
        z[unique(subset_x$iso)[1] == z$iso, c(column_names)] <- subset_x[j, 6:8]
      }
    }
  }
  proc.time() - ptm
  
  write.csv(x = z, file = paste(var, '.csv', sep = ''))
}



z <- read.csv("ACCESS.csv")
library(jsonlite)
x <- toJSON(z)
cat(x)



