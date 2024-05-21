# VWAP-Model

## Description

This project aims to develop an pricing strategy for a guaranteed VWAP execution for algorithmic trading and quantitative strategies. The model is mostly inspired by Almgren-Chriss "Optimal Execution in Portfolio Transactions"

## Objective

The main objective is to calculate the risk adjusted cost of a guaranteed VWAP execution. The cost consist of a the expected execution cost and the variance of the spread cost times the risk aversion parameter. Our project first solved for the optimal trading trajectory to minimize the expected risk adjusted cost of execution, and then using a multiple linear regression to construct a volume model. Combined, we solve for the risk adjusted cost of the execution. 

## Data

- Utilizes the TAQ dataset, focusing on a subset of S&P 500 stocks for liquidity.
- Uses average daily value traded instead of average daily volume traded to account for stock splits.
- Data processing involves computing various metrics such as mid-quote returns, total daily value, arrival price, and terminal price.

## Methodology
1. Solved for the optimal trading trajectory to minimize the expected risk adjusted cost of execution.
2. Using a multiple linear regression to construct a volume model.
3. Using the input from the volume model, we compute for the risk adjusted cost of the execution.
The details of the solution is in optimal_execution.ipynb

## Results
According to the non-linear regression equations:

$$h = \eta * \sigma * (\frac{X}{VT})^\beta$$

$h$: temporary impact
$\sigma$: stock specific volatility
$X$: Daily imbalance (value)
$V$:Average daily value 
$T$: time

We discovered $\eta = 0.33244$, $\beta = 0.36127$.

The analysis of the fit of the model are in [descriptiveStats.ipynb](https://github.com/ssnyu/Market-Impact-Model/blob/main/descriptiveStats.ipynb)



## Supplementary 

### Directory structure - [Directory.ReadME](https://github.com/ssnyu/Market-Impact-Model/blob/main/Directory.md)
