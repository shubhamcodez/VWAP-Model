import numpy as np
import pandas as pd


def optimal_execution(EV,X,Lambda,sigma,ADV,eta,T,N):
    '''
    This function returns the optimal liquidation trajectory with VWAP price as benchmark, solved using Almgren-Chriss framework

    Args:

    times (numpy array): the time of each trading period
    EV (numpy array): the expected cumulative volume at each time point, in fraction
    X (int): number of shares to execute ( positions to liquidate )
    kappa (float): risk aversion parameter. Calculated as sqrt(Lambda * sigma**2 / eta_hat)

    
    Returns:

    numpy array: the optimal positions at each time point
    '''
    kappa = np.sign(Lambda) * np.sqrt(np.abs(Lambda) * sigma / (1.5 * eta * np.sqrt(1 / ADV)))
    times = np.array([i * T / N for i in range(N + 1)])
    if kappa == 0:
        return (1 - times) * X
    return (np.sinh(kappa * (T - times)) / np.sinh(kappa * T) ) * X + (1 - (np.sinh(kappa * (T - times)) + np.sinh(kappa * times)) / np.sinh(kappa * T)) * EV * X


def total_cost(xk,sigma,ADV,prices,volumes,eta,T,N):
    '''
    This function calculate the total cost of a guaranteed VWAP execution of a given trajectory

    Args:
    xk (numpy array): the position at each time point
    sigma (float): the volitality of the stock. Should be volatility of stock return times stock arrival price
    prices (numpy array): stock's prices at each half hour time bucket
    volumes: stock's volume at each half hour time bucket

    Returns:
    tuple (float,float) : a tuple with 2 elements:
    1. the total trading cost incurred
    2. the total deviation from the benckmark price (VWAP)

    '''
    diffs = []
    for i in range(1,len(xk)):
        diffs.append(xk[i] - xk[i-1])
    nk = np.array(diffs)
    diffs = np.array(diffs) / ((T / N) * ADV)

    trading_cost = np.dot(nk,np.sign(diffs) * 1.5 * eta * sigma * np.sqrt(np.abs(diffs)))

    VWAP = np.dot(prices,volumes) / np.sum(volumes)
    X = xk[0]

    spread = X * VWAP - np.dot(-1 * nk,prices)

    return trading_cost , spread
    
def price_spread(sigma,X,ADV,EVK,EVK2,eta,T,N,Lambda = 10**-6):
    '''
    This function calcuate the risk adjusted cost of a guaranteed VWAP execution

    Args:
    sigma (float): the volitality of the stock. Should be volatility of stock return times stock arrival price
    X (int): number of shares to execute ( positions to liquidate )
    ADV (int,float): Average daily value: calculated as average daily volume times arrival price
    EVK (numpy array): he expected cumulative volume at each time point, in fraction
    EVK2 (numpy array): the 2nd moment of the cumulative fractional volume of the day
    Lambda (float): risk aversion parameter. Translate varaince to cost. 

    Returns:
    float: the risk adjusted cost of guaranteed VWAP execution (per share)

    '''
    if X == 0:
        return 0
    
    tau = T / N

    #solve for the optimal trading trajectory
    optimal_xk = optimal_execution(EVK,X,Lambda,sigma,ADV,eta,T,N)

    #compute the estimated trading cost
    diffs = []
    for i in range(1,len(optimal_xk)):
        diffs.append(optimal_xk[i] - optimal_xk[i-1])
    nk = np.array(diffs)
    diffs = np.array(diffs) / ((T / N) * ADV)

    trading_cost = np.dot(nk,np.sign(diffs) * 1.5 * eta * sigma * np.sqrt(np.abs(diffs)))

    #compute the variance
    var = np.sum(sigma**2 * tau * (np.square(optimal_xk) - 2 * EVK * optimal_xk  * X + EVK2 * X**2))

    #return the risk adjusted cost per share
    return (trading_cost +  Lambda * var) / np.abs(X)

