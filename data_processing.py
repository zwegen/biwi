import json

def process_data(data):
    """
    Processes the API data and formats it for output.
    
    Returns a dictionary that can be used for the widget's labels.
    
    Args:
        data (dict): The raw data retrieved from the API.
        
    Returns:
        dict: A formatted dictionary for display or None if data is empty.
    """
    if not data:
        return None  # Return None if there's no data to process

    # Load settings from the settings.json file
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    # Filter fields that are set to "true" in the JSON
    label_visibility = settings.get('label_visibility', {})

    # Create a mapping of fields to their corresponding values in the data
    field_mapping = {
        "formatted_price": data['formatted_price'],
        "formatted_high": data['formatted_high_24h'],  # Change the key
        "formatted_low": data['formatted_low_24h'],     # Change the key
        "formatted_market_cap": data['formatted_market_cap'],
        "formatted_volume": data['formatted_volume'],     # Change the key
        "formatted_mined": data['formatted_circulating_supply'],
        "Unmined": data['formatted_missing_bitcoins'],
        "block_height": data['block_height'],
        "hashrate": data['hashrate'],
        "unconfirmed_tx": data['unconfirmed_tx'],
        "formatted_ath": data['formatted_ath'],
        "fees_output": data['fees_output'],
    }

    # Append only values whose associated labels are set to "true" in the settings.json
    values_to_check = []
    for label, value in field_mapping.items():
        # Check if the label should be visible
        if label_visibility.get(label.replace("formatted_", "").replace("_", " ").title(), False):
            values_to_check.append(value)

    # Find the maximum length of the values for formatting
    max_length = max(len(str(value)) for value in values_to_check) if values_to_check else 0

    # Save the maximum length in the settings.json
    save_max_length_to_json(max_length)

    # Use the maximum length to format the output
    processed_data = {
        "Price": f"BTC - {data['currency_code']}       : {data['formatted_price']:>{max_length}} {data['currency_symbol']}",
        "Change": f"Change % (24h)  : {data['price_change_24h']:>{max_length}.3f} %".replace('.', ','),
        "High": f"High (24h)      : {data['formatted_high_24h']:>{max_length}} {data['currency_symbol']}",  # Change the key
        "Low": f"Low (24h)       : {data['formatted_low_24h']:>{max_length}} {data['currency_symbol']}",   # Change the key
        "Market Cap": f"Market Cap      : {data['formatted_market_cap']:>{max_length}} {data['currency_symbol']}",
        "Volume": f"Volume (24h)    : {data['formatted_volume']:>{max_length}} {data['currency_symbol']}",   # Change the key
        "Mined": f"Mined ₿         : {data['formatted_circulating_supply']:>{max_length}} \u20bf",
        "Unmined": f"Unmined ₿       : {data['formatted_missing_bitcoins']:>{max_length}} \u20bf",
        "Unmined %": f"Unmined ₿ (%)   : {data['percentage_missing']:>{max_length}.3f} %".replace('.', ','),
        "Block Height": f"Block Height    : {data['block_height']:>{max_length}}",
        "Hashrate": f"Hashrate (EH/s) : {data['hashrate']:>{max_length}}",
        "Unconfirmed TX": f"Unconfirmed TX  : {data['unconfirmed_tx']:>{max_length}}",
        "ATH": f"All-Time High   : {data['formatted_ath']:>{max_length}} {data['currency_symbol']}",
        "Fees": f"Fees (sat/vB)   : {data['fees_output']:>{max_length}}",
    }
    
    return processed_data  # Return the processed data dictionary

def save_max_length_to_json(max_length):
    """Saves the maximum length to the settings.json file.
    
    This function updates the 'largest_string_length' field in the settings JSON file.

    Args:
        max_length (int): The maximum string length to save.
    """
    # Load current settings
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    # Set the maximum length
    settings['largest_string_length'] = max_length

    # Save the updated settings back to the file
    with open('settings.json', 'w') as f:
        json.dump(settings, f, indent=4)  # Save with indentation for readability

    print(f"The maximum length of {max_length} has been successfully saved to settings.json.")

def handle_error():
    """Returns a standard error message when data retrieval fails.
    
    This function provides a dictionary with error messages for each label in case of failure.
    
    Returns:
        dict: A dictionary with error messages for each relevant label.
    """
    return {label: "Error retrieving Bitcoin data." for label in [
        "Price", "Change", "High", "Low",  # Change the key
        "Market Cap", "Volume", "Mined",  # Change the key
        "Unmined", "Unmined %", "Block Height", 
        "Hashrate", "Unconfirmed TX", "ATH", "Fees"
    ]}
