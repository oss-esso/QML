#ifndef BLACK_SCHOLES_HPP
#define BLACK_SCHOLES_HPP

#include <cmath>
#include <iostream>

namespace FinancialMath {

class BlackScholes {

private:

    static double norm_cdf(double x) {
        return 0.5 * (1+std::erf(x/M_SQRT2));
    }

    static double norm_pdf(double x){
        return std::exp(-0.5 * x*x) / std::sqrt(2 * M_PI);
    }

public:
    
    static double call_price(double S, double K, double T, double r, double sigma){
        double d1 = (std::log(S/K) + (r+0.5 * sigma*sigma)*T) / (sigma * std::sqrt(T));
        double d2 = d1 - sigma * std::sqrt(T);
        return S * norm_cdf(d1) - K * std::exp(-r * T) * norm_cdf(d2);
    }
    static double put_price(double S, double K, double T, double r, double sigma){
        double d1 = (std::log(S/K) + (r+0.5 * sigma*sigma)*T) / (sigma * std::sqrt(T));
        double d2 = d1 - sigma * std::sqrt(T);
        return K * std::exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1);
    }
};
}

#endif