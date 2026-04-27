# Wikipedia Proxy Research

This repository quantifies how editing activity on Wikipedia pages related to Elon Musk and Tesla, Inc. serves as a real-time proxy for public attention and explains variations in Tesla’s stock returns.

## Project Structure

- **`main.py`**: The core of the research. This script contains the primary logic, including:
  - Data processing and econometric modeling.
  - Statistical tests and validations.
  - Comprehensive visualizations of the research findings.
- **`master.csv`**: The central dataset used for the final analysis. This is a joined DataFrame containing the consolidated data from Wikipedia editing rates, Google Trends, and Tesla stock market performance.
- **`data/datasets/`**: Directory containing all raw and intermediate data collected from various sources (Wikipedia API, Yahoo Finance, Google Trends, etc.).
- **`motivating_examples/`**: Supplementary materials or preliminary analyses that illustrate the research context.
- **`reports/`**: Documentation or summaries derived from the research results.

## Getting Started

1. **Prerequisites**: Ensure you have Python installed along with necessary libraries.
2. **Data**: The primary analysis relies on `master.csv`. If you wish to replicate the data collection process, refer to the files in `data/datasets/`.
3. **Execution**: Run `main.py` to generate the models, conduct statistical tests, and view the research visualizations.

## Research Focus
This project tests the correlation between "CEO-driven shocks" (proxied by Wikipedia activity) and stock market volatility, aiming to determine if digital attention metrics can reliably predict or explain stock returns.
