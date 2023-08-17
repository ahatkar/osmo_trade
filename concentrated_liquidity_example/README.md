
## README for Osmosis CL Automation Script

### Overview:

This script aims to automate certain operations related to the Osmosis blockchain CL, such as:

1. Fetching pool data.
2. Retrieving account details.
3. Creating, withdrawing, and adding to positions.

### Prerequisites:

- Required libraries: `requests`, `mospy`, `pandas`, `json`, `cosmospy_protobuf`
  
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
- `position_id`: The ID of the position. (this is optional , in case query postion doesn't work you can use this)
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

Concentrated Liquidity Strategy (cl_strat.py)

This script provides an automated strategy for managing concentrated liquidity positions on the Osmosis platform.

Overview
The script performs the following operations:
  Fetches the current pool data.
  Checks user's positions hourly.
  Updates the positions based on the specified percent range. If the current tick is out of the user's range, it withdraws the position and creates a new one.
Requirements
  A private_info.json file containing your mnemonic key, cosmos address, and stride address.
  An input_data.json file containing information about your desired liquidity positions.

Note: refere to below README.md file for tick and amount calculations
https://github.com/osmosis-labs/osmosis/tree/main/x/concentrated-liquidity

