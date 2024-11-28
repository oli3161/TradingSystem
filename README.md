# Trading System

## Overview

## Features


## Project Structure

```plaintext
.
├── README.md
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
├── simple_ui
│   ├── index.html
│   └── index.js
└── trading
    ├── __init__.py
    ├── diagrams
    │   └── exchange_logic.plantuml
    ├── main.py
    ├── models
    │   ├── __init__.py
    │   ├── assets.py
    │   ├── client.py
    │   ├── heaps.py
    │   ├── limit_order.py
    │   ├── market_maker.py
    │   ├── market_order.py
    │   ├── order.py
    │   ├── order_flow.py
    │   ├── order_matching_engine.py
    │   ├── orderbook.py
    │   ├── portfolio.py
    │   ├── portfolio_stock.py
    │   ├── stock_exchange.py
    │   ├── stock_market_listing.py
    │   ├── transaction.py
    │   └── transaction_history.py
    └── tests
        ├── __init__.py
        ├── __pycache__
        │   └── client_tests.cpython-312.pyc
        ├── client_tests.py
        ├── heaps_tests.py
        ├── market_maker_tests.py
        └── order_engine_tests.py
```

- **simple_ui/**: Contains the front-end user interface files.
- **trading/**: Core application modules.
  - **models/**: Contains all the model classes such as `Client`, `Order`, `Portfolio`, etc.
  - **tests/**: Unit and integration tests for the application.
  - **main.py**: Entry point for running the trading system.
  - **diagrams/**: UML diagrams representing system architecture.

## Installation

### Prerequisites

### Setup

**Install Dependencies**

   Install the required packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Trading System

Start the trading system by executing the main application script:

```bash
python trading/main.py
```

**Output:**

```
The websocket server is running on port 8765.
```