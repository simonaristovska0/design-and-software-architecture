# Design and Software Architecture: Third Homework - The Web Application

This repository contains the third homework for the **Design and Software Architecture** course. It focuses on implementing the **functional and non-functional requirements** outlined in the SRS document. The homework involves developing a **web application** with three types of analyses:

- **Technical Analysis** (mandatory): Analyze historical stock data using oscillators and moving averages, generate buy/sell/hold signals, and calculate indicators over multiple timeframes (daily, weekly, monthly).
- **Fundamental Analysis**: Perform sentiment analysis on news articles related to companies using NLP techniques to identify positive or negative trends.
- **LSTM-Based Stock Price Prediction**: Utilize machine learning (LSTM) to predict future stock prices based on historical data.

The system demonstrates the ability to meet all specified requirements.
---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Usage](#usage)

---

## Project Overview

The project includes:

1. **Implementation of Functional and Non-Functional Requirements** defined in the SRS document.
2. **Development of Three Types of Analyses**:
   - **Technical Analysis**: Using oscillators and moving averages to analyze stock data and generate trading signals.
   - **Fundamental Analysis**: Performing sentiment analysis on news articles to determine stock trends.
   - **LSTM-Based Stock Price Prediction**: Predicting future stock prices using machine learning.
3. **A Fully Functional Web Application** demonstrating the successful integration of all features.

---

## Features

- **Functional and Non-Functional Requirements**:
  - Implementation of all requirements defined in the SRS document.
- **Analyses**:
  - **Technical Analysis**: Analyze stock data using oscillators and moving averages, generate trading signals, and calculate indicators for daily, weekly, and monthly timeframes.
  - **Fundamental Analysis**: Perform sentiment analysis on news articles using NLP techniques to determine positive or negative trends.
  - **LSTM-Based Stock Price Prediction**: Predict future stock prices using machine learning models.
- **Web Application**:
  - Core functionalities for user interaction (data visualization, search, login, registration, etc.).
- **Video Demonstration**:
  - A video walkthrough showcasing all implemented features and analyses.

## Project Structure

```
Домашна 3/                      # Main project folder
├── .idea/                      # IDE configuration files (optional)
├── proekt/                     # Project source code folder
│   ├── .idea/                  # IDE configuration for subfolder
│   ├── Data/                   # Data-related resources
│   ├── app/                    # Main application logic
│   │   ├── pycache/        # Python bytecode cache
│   │   ├── migrations/         # Django migrations
│   │   │   ├── pycache/    # Cache for migrations
│   │   │   ├── 0001_initial.py # Initial migration
│   │   │   ├── init.py
│   │   ├── static/             # Static files for the app
│   │   ├── templates/app/      # HTML templates for the app
│   │   │   ├── dashboard_page.html
│   │   │   ├── dashboard_page_prvobitno.html
│   │   │   ├── login_form.html
│   │   │   ├── register_form.html
│   │   │   ├── search_result_page-fundamental.html
│   │   │   ├── search_result_page-predviduvanja.html
│   │   │   ├── search_result_page-tehnicka.html
│   │   │   ├── search_result_page-vizuelizacija.html
│   │   │   ├── starting_page.html
│   │   │   ├── test.html
│   │   ├── utils/              # Utility scripts and modules
│   │   │   ├── init.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── forms.py
│   │   │   ├── models.py
│   │   │   ├── tests.py
│   │   │   ├── train_model.py  # LSTM training script
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   ├── vizualizacija.py  # Visualization logic
│   ├── fundamental_analysis/   # Folder for fundamental analysis
│   │   ├── pdf_downloads/      # Downloaded PDFs for analysis
│   │   ├── extracting_issuers.py
│   │   ├── get_the_data.py
│   │   ├── sentiment.py        # Sentiment analysis logic
│   │   ├── summarization.py
│   │   ├── translation_final.py
│   ├── proekt/                 # Django core project files
│   │   ├── pycache/
│   │   ├── init.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   ├── stilovi/                # Static styles and templates
│   │   ├── css_ne.css          # CSS styles
│   │   ├── dobrodojdovte.html  # Welcome page
│   │   ├── index_ne.html       # Index page
│   │   ├── pochetna.html       # Homepage
│   │   ├── user_profile.html   # User profile page
│   │   ├── search_result_moe.html  # Search results
│   │   ├── logo.png            # Logo asset
│   ├── templates/              # Django templates
│   │   ├── base_nenajaven.html # Base template for unauthenticated users
│   ├── za_homepage/            # Scripts for scraping and homepage data
│   │   ├── market_data_tabela_od_mse.py
│   │   ├── market_summary.csv
│   │   ├── mse_table.csv
│   │   ├── scrape_table_from_mse.py
│   │   ├── sei_net_news.py
│   │   ├── sei_net_news_only.csv
├── db.sqlite3                  # SQLite database
├── manage.py                   # Django management script
├── scrape_the_data.py          # Data scraping logic
```

---

