# Building Efficient Portfolios

## Overview

This repo contains the code and data used to generate the results in the article "Building Efficient Portfolios." The project explores three fundamental concepts in modern portfolio theory: the Capital Asset Pricing Model (CAPM), Markowitz Mean-Variance Optimization (MVO), and Arbitrage Pricing Theory (APT).

## File Structure

The repo is structured as:
- `data/` contains financial data including:
  - S&P 500 constituent stock price history
  - Risk-free rate (1-month Treasury Bill Yield)
  - Market index data
  - Fama-French factors data
- `figs/` contains LaTeX tables and figures generated for the paper
- `paper/` contains the LaTeX files and PDF of the paper
- `scripts/` contains Python scripts and Jupyter notebooks:
  - `0.0.data_download.py` - downloads financial data from Global Financial Data API
  - `1.0.markowitz_efficient_frontier.ipynb` - implements MVO and efficient frontier analysis
  - `2.0.arbitrage_portfolio_theory.ipynb` - implements APT multi-factor analysis
  - `config.py` - stores API credentials (actual credentials not committed to git)
  - `utils.py` - contains utility functions for data handling Finaeon API data.

## Key Features

- Implementation of CAPM to estimate systematic risk (beta) and expected returns
- Construction of the efficient frontier using Markowitz portfolio optimization
- Analysis of multiple risk factors using Arbitrage Pricing Theory
- Visualization of portfolio performance and risk metrics
- Tables of factor returns, betas, and other portfolio statistics

## Development Environment

- Python 3.x with pandas, numpy, matplotlib, and statsmodels
- Jupyter notebooks for interactive analysis
- LaTeX for paper preparation and visualization

## Statement on LLM usage

Aspects of the code were written with the help of the auto-complete tool, GitHub copilot. Examples include plotting functions, Latex tables, and autocomplete for simpler expressions.

ChatGPT was used in a final review of the paper and to help generate parts of the README file.

## Contact

I can be reached at aman.rana@mail.utoronto.ca
This repo was created for an assignment for the course ECO358 taught by Louis Bélisle in Winter 2025.