/**
 * High-performance option pricing library in C++
 * 
 * This header provides optimized implementations of option pricing
 * algorithms using modern C++17 features.
 * 
 * Compile with: g++ -O3 -std=c++17 -shared -fPIC
 */

#ifndef OPTION_PRICING_HPP
#define OPTION_PRICING_HPP

#include <cmath>
#include <random>
#include <vector>
#include <algorithm>
#include <numeric>

namespace OptionPricing {

/**
 * Black-Scholes formula for European options (analytical solution)
 */
class BlackScholes {
private:
    // Standard normal CDF using error function
    static double norm_cdf(double x) {
        return 0.5 * std::erfc(-x * M_SQRT1_2);
    }
    
    // Standard normal PDF
    static double norm_pdf(double x) {
        return std::exp(-0.5 * x * x) / std::sqrt(2.0 * M_PI);
    }

public:
    /**
     * Calculate d1 parameter for Black-Scholes
     */
    static double calculate_d1(double S, double K, double T, double r, double sigma) {
        return (std::log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * std::sqrt(T));
    }
    
    /**
     * Calculate d2 parameter for Black-Scholes
     */
    static double calculate_d2(double d1, double sigma, double T) {
        return d1 - sigma * std::sqrt(T);
    }
    
    /**
     * Price European call option
     */
    static double call_price(double S, double K, double T, double r, double sigma) {
        double d1 = calculate_d1(S, K, T, r, sigma);
        double d2 = calculate_d2(d1, sigma, T);
        return S * norm_cdf(d1) - K * std::exp(-r * T) * norm_cdf(d2);
    }
    
    /**
     * Price European put option
     */
    static double put_price(double S, double K, double T, double r, double sigma) {
        double d1 = calculate_d1(S, K, T, r, sigma);
        double d2 = calculate_d2(d1, sigma, T);
        return K * std::exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1);
    }
    
    /**
     * Calculate all Greeks at once (cache efficiency)
     */
    struct Greeks {
        double delta;
        double gamma;
        double vega;
        double theta;
        double rho;
    };
    
    static Greeks calculate_greeks(double S, double K, double T, double r, double sigma, bool is_call) {
        Greeks g;
        double d1 = calculate_d1(S, K, T, r, sigma);
        double d2 = calculate_d2(d1, sigma, T);
        double sqrt_T = std::sqrt(T);
        double pdf_d1 = norm_pdf(d1);
        double cdf_d1 = norm_cdf(d1);
        double cdf_d2 = norm_cdf(d2);
        
        if (is_call) {
            g.delta = cdf_d1;
            g.theta = -(S * pdf_d1 * sigma) / (2 * sqrt_T) - r * K * std::exp(-r * T) * cdf_d2;
            g.rho = K * T * std::exp(-r * T) * cdf_d2;
        } else {
            g.delta = cdf_d1 - 1.0;
            g.theta = -(S * pdf_d1 * sigma) / (2 * sqrt_T) + r * K * std::exp(-r * T) * norm_cdf(-d2);
            g.rho = -K * T * std::exp(-r * T) * norm_cdf(-d2);
        }
        
        // Gamma and Vega are same for call and put
        g.gamma = pdf_d1 / (S * sigma * sqrt_T);
        g.vega = S * pdf_d1 * sqrt_T;
        
        return g;
    }
};

/**
 * Monte Carlo option pricing with variance reduction
 */
class MonteCarlo {
private:
    std::mt19937 gen;
    std::normal_distribution<> normal;
    
public:
    MonteCarlo(unsigned seed = 42) : gen(seed), normal(0.0, 1.0) {}
    
    /**
     * Price European option with antithetic variates for variance reduction
     */
    double european_option(double S0, double K, double T, double r, double sigma,
                          int n_simulations, bool is_call) {
        double drift = (r - 0.5 * sigma * sigma) * T;
        double vol = sigma * std::sqrt(T);
        double discount = std::exp(-r * T);
        double payoff_sum = 0.0;
        
        // Use antithetic variates (pairs of Z and -Z)
        for (int i = 0; i < n_simulations / 2; ++i) {
            double Z = normal(gen);
            
            // Positive path
            double ST1 = S0 * std::exp(drift + vol * Z);
            double payoff1 = is_call ? std::max(ST1 - K, 0.0) : std::max(K - ST1, 0.0);
            
            // Antithetic path
            double ST2 = S0 * std::exp(drift - vol * Z);
            double payoff2 = is_call ? std::max(ST2 - K, 0.0) : std::max(K - ST2, 0.0);
            
            payoff_sum += (payoff1 + payoff2) / 2.0;
        }
        
        return discount * payoff_sum / (n_simulations / 2);
    }
    
    /**
     * Price Asian option (path-dependent)
     */
    double asian_option(double S0, double K, double T, double r, double sigma,
                       int n_simulations, int n_steps, bool is_call) {
        double dt = T / n_steps;
        double drift = (r - 0.5 * sigma * sigma) * dt;
        double vol = sigma * std::sqrt(dt);
        double discount = std::exp(-r * T);
        double payoff_sum = 0.0;
        
        for (int i = 0; i < n_simulations; ++i) {
            double S = S0;
            double avg = 0.0;
            
            // Simulate path
            for (int j = 0; j < n_steps; ++j) {
                S *= std::exp(drift + vol * normal(gen));
                avg += S;
            }
            avg /= n_steps;
            
            // Payoff based on average
            double payoff = is_call ? std::max(avg - K, 0.0) : std::max(K - avg, 0.0);
            payoff_sum += payoff;
        }
        
        return discount * payoff_sum / n_simulations;
    }
};

/**
 * Binomial tree for American options
 */
class BinomialTree {
public:
    /**
     * Price American option using Cox-Ross-Rubinstein binomial tree
     */
    static double american_option(double S0, double K, double T, double r, double sigma,
                                 int n_steps, bool is_call) {
        double dt = T / n_steps;
        double u = std::exp(sigma * std::sqrt(dt));  // Up factor
        double d = 1.0 / u;                           // Down factor
        double p = (std::exp(r * dt) - d) / (u - d); // Risk-neutral probability
        double discount = std::exp(-r * dt);
        
        // Build tree forward
        std::vector<double> prices(n_steps + 1);
        for (int i = 0; i <= n_steps; ++i) {
            prices[i] = S0 * std::pow(u, n_steps - i) * std::pow(d, i);
        }
        
        // Calculate option values at maturity
        std::vector<double> values(n_steps + 1);
        for (int i = 0; i <= n_steps; ++i) {
            values[i] = is_call ? std::max(prices[i] - K, 0.0) : std::max(K - prices[i], 0.0);
        }
        
        // Backward induction
        for (int step = n_steps - 1; step >= 0; --step) {
            for (int i = 0; i <= step; ++i) {
                prices[i] = prices[i] / u;  // Update price for this node
                
                // Continuation value
                double continuation = discount * (p * values[i] + (1 - p) * values[i + 1]);
                
                // Exercise value
                double exercise = is_call ? std::max(prices[i] - K, 0.0) : std::max(K - prices[i], 0.0);
                
                // American option: max of continuation and exercise
                values[i] = std::max(continuation, exercise);
            }
        }
        
        return values[0];
    }
};

} // namespace OptionPricing

#endif // OPTION_PRICING_HPP
