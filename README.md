## NSE - Securities in Futures and Options Analysis
<img width="928" alt="Screenshot 2024-08-01 at 11 00 21 AM" src="https://github.com/user-attachments/assets/e685bca7-75ec-4fbe-a7f6-24d55d6704fe">


Welcome to the NSE Securities in Futures and Options Analysis project! This project provides a comprehensive data analysis platform for stocks listed in the Futures and Options (F&O) segment of the National Stock Exchange (NSE) of India. It leverages Streamlit for a user-friendly web interface, fetches live data periodically, and provides analysis based on custom metrics.

### Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Detailed Breakdown](#detailed-breakdown)
   - [Data Fetching](#data-fetching)
   - [Data Processing](#data-processing)
   - [User Interface](#user-interface)
7. [Customization](#customization)
8. [Future Enhancements](#future-enhancements)
9. [Contributing](#contributing)
10. [License](#license)
11. [Acknowledgments](#acknowledgments)

## Overview

This project aims to provide real-time and historical analysis of stocks in the F&O segment of the NSE. The primary functionalities include fetching real-time stock data, processing this data to generate actionable insights, and providing a clean and interactive web interface for users to explore the data.

## Features

- **Real-time Data Fetching:** Automatically fetches data from NSE's official site every 30 minutes.
- **Data Processing:** Ranks stocks based on percentage change (%CHNG), identifies trading actions (buy/sell), and checks for 52-week highs and lows.
- **Interactive Interface:** Utilizes Streamlit to display data tables, charts, and provides a downloadable CSV of the processed data.
- **Custom Analysis:** Incorporates custom metrics and logic for in-depth stock analysis.

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.7+
- Pip (Python package installer)

### Steps

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/yourusername/nse-fo-analysis.git
   cd nse-fo-analysis
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```sh
   streamlit run app.py
   ```

## Usage

Upon starting the application, you can navigate to the provided local URL in your browser. The interface will display real-time data fetched from the NSE, along with processed metrics and analysis. The data will refresh every 30 minutes, with a countdown timer indicating the next update.

### Downloading Data

You can download the processed data as a CSV file. The filename will include the current date and time to distinguish between different datasets.

## Project Structure

```
nse-fo-analysis/
├── app.py              # Main application file
├── data/               # Directory for storing analysed csv data (if needed) 
├── requirements.txt    # List of Python dependencies
├── README.md           # Project documentation
```

## Detailed Breakdown

### Data Fetching

The data is fetched using the `requests` library, with a session object to manage cookies and headers required by NSE's API. The fetched data includes various stock metrics such as `symbol`, `open`, `dayHigh`, `dayLow`, `previousClose`, `lastPrice`, `change`, `pChange`, `totalTradedVolume`, `totalTradedValue`, `yearHigh`, `yearLow`, `perChange30d`, and `perChange365d`.

### Data Processing

Data processing is handled by the `StockDataProcessor` class. Key functionalities include:
- **Ranking stocks** based on `%CHNG`.
- **Identifying trading actions** (buy/sell) based on specific conditions.
- **Checking 52-week highs and lows** to provide insights on stock performance.

### User Interface

The interface is built using Streamlit, providing a dynamic and interactive experience. Users can view the processed data, download it, and watch a countdown timer for the next data update.

## Customization

You can customize the data processing logic by modifying the `StockDataProcessor` class. For example, you can add more conditions for trading actions or additional metrics for analysis.

## Future Enhancements

- **Integration with More Data Sources:** Include additional financial data sources for a more comprehensive analysis.
- **Advanced Visualization:** Add more charts and graphs for better data visualization.
- **User Authentication:** Allow users to save their settings and preferences.

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.



## Acknowledgments

Special thanks to the contributors and the open-source community for their invaluable support and tools.

---

*This README file provides a comprehensive guide to the project. For more information, visit the [official documentation](https://github.com/yourusername/nse-fo-analysis).*
