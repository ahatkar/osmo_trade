
## README for Osmosis CL Automation Script

### Overview:

This script aims to automate certain operations related to the Osmosis blockchain CL, such as:

1. Fetching pool data.
2. Retrieving account details.
3. Creating, withdrawing, and adding to positions.

### Prerequisites:

- Required libraries: `requests`, `mospy`, `pandas`, `json`, `cosmospy_protobuf`, and `tx_pb2`.
  
  Install these using pip:

  ```bash
  pip install requests mospy pandas cosmospy_protobuf
  ```

  Note: Some libraries might not be available directly via pip and may need to be installed from source or other methods.

### Setup:

1. Ensure that you have a `private_info.json` file in the same directory as the script. The file should contain:

   ```json
   {
       "mnemonic_key": "YOUR_MNEMONIC_KEY",
       "cosmos_address": "YOUR_COSMOS_ADDRESS",
       "stride_address": "YOUR_STRIDE_ADDRESS"
   }
   ```

2. Ensure that you have an `input_data.json` file in the same directory. This file should contain the necessary information to create positions.
### `input_info.json` Format:

This JSON file contains an array of position data that the script uses to create, withdraw, or add to positions. Each object in the array represents a position and has the following properties:

- `pool_id`: The ID of the pool.
- `position_id`: The ID of the position.
- `lower_tick`: The lower tick value.
- `upper_tick`: The upper tick value.
- `amount0`: Amount of the first token.
- `amount1`: Amount of the second token.
- `token_min_amount0`: Minimum amount of the first token.
- `token_min_amount1`: Minimum amount of the second token.

Example:

```json
[
    {
        "pool_id": 1066,
        "position_id": 17706,
        "lower_tick": 100055000,
        "upper_tick": 105079000,
        "amount0": "764213355847087954",
        "amount1": "1000000",
        "token_min_amount0": "975000",
        "token_min_amount1": "745108021950910755"
    }
]
```

Ensure that this file is present in the same directory as the script before executing.


### Execution:

Run the script using:

```bash
python concentrated_liquidity.py
```

Replace `concentrated_liquidity.py` with the name you've saved the script as.


### Functions:

1. `read_input_json(file_path)`: Reads a JSON file from the given file path.
2. `get_pools()`: Fetches pool data from Osmosis API.
3. `fetch_account_data(stride_address)`: Fetches the account number and sequence for the given Stride address.
4. `create_position_transaction(...)`: Constructs a transaction to create a position.
5. `withdraw_position_transaction(...)`: Constructs a transaction to withdraw from a position.
6. `add_to_position_transaction(...)`: Constructs a transaction to add to a position.

### Main Logic:

The main logic of the script is encapsulated within the `createPositionInRange(percent_range)` function. This function automates the process of:

- Fetching account data.
- Reading the input data.
- Calculating the lower and upper ticks based on the current tick and given percentage range.
- Creating position transactions and broadcasting them.

### Notes:

1. The script currently has portions related to withdrawing from and adding to positions commented out. To use these functionalities, uncomment the relevant sections and ensure that the necessary data is present in `input_data.json`.



