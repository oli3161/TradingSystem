## Testing

Ensure that all tests pass to verify the integrity of the trading system.

1. **Activate the Virtual Environment**

   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Run the Test Suite**

   Execute all tests using `pytest`:

   ```bash
   pytest trading/tests/
   ```

   **Example Output:**

   ```
   ============================= test session starts ==============================
   platform darwin -- Python 3.12.0, pytest-7.2.0, pluggy-1.0.0
   collected 10 items

   trading/tests/test_client.py ..........                                [100%]

   ============================== 10 passed in 0.50s ===============================
   ```

3. **Running Specific Tests**

   To run a specific test module or function:

   ```bash
   pytest trading/tests/client_tests.py
   ```

   Or to run a specific test function within a module:

   ```bash
   pytest trading/tests/client_tests.py::test_submit_order
   ```