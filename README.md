# Trading System

## Setup

```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

## Run on websocket

```bash
python trading/main.py
```

The websocket server is running on port `8765`.

## Run the main file
```bash
cd path/to/TradingSystem
python -m trading.main

```

## Test

```bash
cd path/to/TradingSystem
pytest
```
To test using vscode Debugger and pytests 
Example test file tests\test_live_order_matching.py
```bash
cd path/to/TradingSystem
py.test --vscodedebug .\trading\tests\test_live_order_matching.py
```



TradingSystem/
├── trading/
│   ├── diagrams/       # Architecture diagrams and visual documentation
│   ├── models/         # Core trading system models
│   ├── tests/          # Test suite for the trading system
│   ├── main_connection.py  # Connection handler script
│   └── main.py         # Main entry point for WebSocket server
└── requirements.txt    # Dependencies for the project
