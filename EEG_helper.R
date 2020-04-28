library(timeSeries)
###########code I adapted from the CMU stats course about spline: http://www.stat.cmu.edu/~cshalizi/402/lectures/11-splines/lecture-11.pdf##############
resampler <- function(data) {
  n <- nrow(data)
  resample.rows <- sample(1:n,size=n,replace=TRUE)
  return(data[resample.rows,])
}

spline.estimator <- function(data,m) {
  fit <- smooth.spline(x=data[,"Time"],y=data[,"Signal"],cv=TRUE, nknots = 15) ###in this matrix, in particular, the time points are in the 3rd column and signal in the 4th column
  eval.grid <- seq(from=min(data[,"Time"]),to=max(data[,"Time"]),length.out=m)
  return(predict(fit,x=eval.grid)$y) # We only want the predicted values
}

spline.cis <- function(data,B=1000,alpha=0.05,m=91) {####n is the number of knots for the spline, also fix the parameters so that we can use the function direction in ddply.
  spline.main <- spline.estimator(data,m=m)
  spline.boots <- replicate(B,spline.estimator(resampler(data),m=m))
  cis.lower <- 2*spline.main - apply(spline.boots,1,quantile,probs=1-alpha/2)
  cis.upper <- 2*spline.main - apply(spline.boots,1,quantile,probs=alpha/2)
  return(data.frame(time=seq(from=min(data[,"Time"]),to=max(data[,"Time"]),length.out=m), signal=spline.main, signal.lower=cis.lower, signal.upper=cis.upper))
}