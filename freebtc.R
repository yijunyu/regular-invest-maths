# Load the markovchain package
library(markovchain)

# Probabilities
p1 <- 0.9
p2 <- 0.8
p3 <- 0.8

# Model of participant behaviours
transitionProbabilities <- matrix(data=c(1-p1,p1,0,0,
                                         0, 0,p2,1-p2,
                                         1-p3,p3,0,0,
                                         0,0,0,1),
                                  byrow=TRUE, nrow=4)
                                  
model <- new("markovchain", states=c("I","R","E", "W"),
             transitionMatrix=transitionProbabilities,
             name="Free BTC")

# Display the model
#show(model)
plot(model, package="diagram")
#steadyStates(model)
#summary(model)

# Simulation
day <- 100
balance <- 1000  # amount of BTC in the initial pool
debt = 0.0
prize <- 0.000001 # 100 satoshi
numberOfParticipants = 100000  # number of participants initially
initialState <- c(numberOfParticipants,0,0,0)



result <- data.frame( "day" = numeric(),
                      "I" = numeric(),
                      "R" = numeric(),
                      "E" = numeric(),
                      "W" = numeric(),
                      stringsAsFactors=FALSE)

for (i in 0:day) {
  newrow <- as.list(c(i,round(as.numeric(initialState * model ^ i),0)))
  result[nrow(result) + 1, ] <- newrow
}

#while ((balance - debt) > prize) {
# day <- day + 1
  
# if (condition) {
#   break()
# }
  
# newrow <- as.list(c(day,round(as.numeric(initialState * (model ^ day)),0)))
# result[nrow(result) + 1, ] <- newrow
#}

plot(result$day,result$I)
points(result$day,result$R, col="red")
points(result$day,result$E, col="green")
points(result$day,result$W, col="blue")
