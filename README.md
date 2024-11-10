# Design and Software Architecture: First homework - Data Extraction

This repository contains the first homework, developed as a part of the Design and Software Architecture course. This project focuses on extracting historical stock data using web scraping techniques while adhering to robust software design practices.

## Table of Contents

- This repository contains a project developed for the Design and Software Architecture course.
  
  [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Project Overview

The goal of this project is to scrape financial data from a public financial website and store the data in CSV format for further analysis.

### Main Approach

Our main approach for data extraction is web scraping using `BeautifulSoup` and `requests`. This method provides greater flexibility and improved performance compared to our initial strategy.

### Initial Approach

Initially, we attempted to extract data by downloading XLS files for each company. However, this approach proved to be slow and inefficient, especially when dealing with a large volume of data. Transitioning to web scraping significantly enhanced performance and streamlined the data extraction process.

## Features

- **Web Scraping**: Uses `BeautifulSoup` and `requests` for efficient data extraction from the target website.
- **Retry Logic**: Implements robust retry mechanisms for handling HTTP errors and server downtime to ensure reliable data collection.
- **Data Deduplication**: Ensures that data is not duplicated when updating CSV files.
- **Concurrency**: Utilizes `ThreadPoolExecutor` to scrape multiple issuer codes concurrently, speeding up the process.
- **Data Storage**: Extracted data is saved in CSV format within the `Data` directory, making it easy to access and analyze.
- **Comparison of Approaches**: Demonstrates the transition from XLS file downloading to web scraping, highlighting the performance benefits of the latter.

## Project Structure

```
|-- Домашна 1 [Домашна 1]    # Main project folder
    |-- .venv/                    # Virtual environment (optional, not included in Git)
    |-- Data/                     # Folder containing the extracted data (CSV files)
    |-- mainCodeWithScraping.py   # Main script for web scraping and data extraction
    |-- codeWithDownloading.py    # Initial script for handling data downloading (legacy)
```

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/simonaristovska0/design-software-architecture-data-extraction.git
   cd design-software-architecture-data-extraction
   ```
2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows, use .venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Main Web Scraping Script**:

   ```bash
   python mainCodeWithScraping.py
   ```

   This script will scrape the financial data, process it, and store it in CSV files within the `Data` directory.

## Dependencies

- `requests`
- `beautifulsoup4`
- `pandas`

Make sure to install the dependencies using `pip install -r requirements.txt`.

