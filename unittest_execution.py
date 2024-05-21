import unittest
import numpy as np
from execution import optimal_execution, total_cost, price_spread  # replace 'your_module' with the actual module name

class TestOptimalExecution(unittest.TestCase):
    def test_zero_risk_aversion(self):
        EV = np.array([0,0.1, 0.5, 0.9])
        X = 1000
        Lambda = 0
        sigma = 0.02
        ADV = 1000000
        eta = 0.1
        T = 1
        N = 3
        expected = (1 - np.array([i * T / N for i in range(N + 1)])) * X
        np.testing.assert_array_almost_equal(optimal_execution(EV, X, Lambda, sigma, ADV, eta, T, N), expected)

    def test_negative_kappa(self):
        EV = np.array([0,0.1, 0.5, 0.9, 1])
        X = 1000
        Lambda = -0.01
        sigma = 0.02
        ADV = 1000000
        eta = 0.1
        T = 1
        N = 4
        result = optimal_execution(EV, X, Lambda, sigma, ADV, eta, T, N)
        self.assertEqual(len(result), N + 1)
        self.assertTrue(np.all(result >= 0))
        
    def test_kappa_equal_zero(self):
        EV = np.array([0,0.2, 0.4, 0.6, 0.8, 1])
        X = 500
        Lambda = 0
        sigma = 0.02
        ADV = 1000000
        eta = 0.1
        T = 1
        N = 5
        times = np.array([i * T / N for i in range(N + 1)])
        expected = (1 - times) * X
        result = optimal_execution(EV, X, Lambda, sigma, ADV, eta, T, N)
        np.testing.assert_array_almost_equal(result, expected)

    def test_typical_case_execution(self):
        EV = np.array([0,0.1, 0.4, 0.6, 0.9, 1])
        X = 2000
        Lambda = 0.05
        sigma = 0.03
        ADV = 2000000
        eta = 0.2
        T = 1
        N = 5
        result = optimal_execution(EV, X, Lambda, sigma, ADV, eta, T, N)
        self.assertEqual(len(result), N + 1)
        self.assertTrue(np.all(result >= 0))

    def test_typical_case_cost(self):
        xk = np.array([1000, 800, 600, 400, 200,0])
        sigma = 0.02
        ADV = 1000000
        prices = np.array([10, 10.2, 10.4, 10.6, 10.8])
        volumes = np.array([50000, 50000, 50000, 50000, 50000])
        eta = 0.1
        T = 1
        N = 5
        
        trading_cost, spread = total_cost(xk, sigma, ADV, prices, volumes, eta, T, N)
        
        # Check if the outputs are reasonable
        self.assertGreaterEqual(trading_cost, 0)
        self.assertIsInstance(spread, float)
    
    def test_zero_volatility(self):
        xk = np.array([1000, 800, 600, 400, 200,0])
        sigma = 0  # zero volatility
        ADV = 1000000
        prices = np.array([10, 10.2, 10.4, 10.6, 10.8])
        volumes = np.array([50000, 50000, 50000, 50000, 50000])
        eta = 0.1
        T = 1
        N = 5
        
        trading_cost, spread = total_cost(xk, sigma, ADV, prices, volumes, eta, T, N)
        
        # With zero volatility, trading cost should be zero
        self.assertEqual(trading_cost, 0)
    
    def test_no_positions(self):
        xk = np.array([0, 0, 0, 0, 0, 0])
        sigma = 0.02
        ADV = 1000000
        prices = np.array([10, 10.2, 10.4, 10.6, 10.8])
        volumes = np.array([50000, 50000, 50000, 50000, 50000])
        eta = 0.1
        T = 1
        N = 5
        
        trading_cost, spread = total_cost(xk, sigma, ADV, prices, volumes, eta, T, N)
        
        # With no positions, both trading cost and spread should be zero
        self.assertEqual(trading_cost, 0)
        self.assertEqual(spread, 0)

    def test_single_period(self):
        xk = np.array([1000, 0])
        sigma = 0.02
        ADV = 1000000
        prices = np.array([10])
        volumes = np.array([50000])
        eta = 0.1
        T = 1
        N = 1
        
        trading_cost, spread = total_cost(xk, sigma, ADV, prices, volumes, eta, T, N)
        
        # Single period liquidation, trading cost should be based on simple calculation
        expected_cost = np.dot([1000], [1.5 * eta * sigma * np.sqrt(1000 / (T / N * ADV))])
        self.assertAlmostEqual(trading_cost, expected_cost)
        self.assertIsInstance(spread, float)

    def test_typical_case_spread(self):
        sigma = 0.02
        X = 1000
        ADV = 1000000
        EVK = np.array([0,0.1, 0.5, 0.9])
        EVK2 = np.array([0,0.01, 0.25, 0.81])
        eta = 0.1
        T = 1
        N = 3
        result = price_spread(sigma, X, ADV, EVK, EVK2, eta, T, N)
        
        # Check if the result is a float
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)
    
    def test_zero_risk_aversion_spread(self):
        sigma = 0.02
        X = 1000
        ADV = 1000000
        EVK = np.array([0,0.1, 0.5, 0.9])
        EVK2 = np.array([0,0.01, 0.25, 0.81])
        eta = 0.1
        T = 1
        N = 3
        Lambda = 0  # zero risk aversion
        result = price_spread(sigma, X, ADV, EVK, EVK2, eta, T, N, Lambda)
        
        # Check if the result is a float
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)
    
    def test_zero_volatility_spread(self):
        sigma = 0
        X = 1000
        ADV = 1000000
        EVK = np.array([0,0.1, 0.5, 0.9])
        EVK2 = np.array([0,0.01, 0.25, 0.81])
        eta = 0.1
        T = 1
        N = 3
        result = price_spread(sigma, X, ADV, EVK, EVK2, eta, T, N)
        
        # With zero volatility, the trading cost should be zero
        self.assertAlmostEqual(result, 0)

    def test_no_positions_spread(self):
        sigma = 0.02
        X = 0  # no positions to liquidate
        ADV = 1000000
        EVK = np.array([0,0.1, 0.5, 0.9])
        EVK2 = np.array([0,0.01, 0.25, 0.81])
        eta = 0.1
        T = 1
        N = 3
        result = price_spread(sigma, X, ADV, EVK, EVK2, eta, T, N)
        
        # With no positions, the risk-adjusted cost should be zero
        self.assertAlmostEqual(result, 0)

if __name__ == '__main__':
    unittest.main()



