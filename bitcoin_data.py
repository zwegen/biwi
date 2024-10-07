import requests
import time  # For delay between retry attempts
import locale
from requests.exceptions import HTTPError
from currencies import currencies, currency_symbols  # Import currency data

# Constants for APIs
CURRENCY = "eur"  # Default currency set to Euro
BITCOIN_ID = "bitcoin"  # Bitcoin ID for API requests
URL_BLOCK = "https://mempool.space/api/blocks/tip/height"  # URL to get the latest block height
HASHRATE_URL = "https://mempool.space/api/v1/mining/hashrate/1w"  # URL to get the hashrate
UNCONFIRMED_TX_URL = "https://mempool.space/api/mempool"  # URL to get unconfirmed transactions

# Automatically set the locale for formatting, this is crucial for correct number formatting
locale.setlocale(locale.LC_ALL, '')

# Retry mechanism to handle potential network errors
def get_with_retries(url, retries=2, delay=10):
    for attempt in range(retries):
        try:
            # Attempt to get the response from the API
            response = requests.get(url, timeout=10)  # Set a timeout of 10 seconds for the request
            response.raise_for_status()  # Raise an error for HTTP error codes
            return response  # Return the response if successful
        except (HTTPError, requests.exceptions.Timeout) as e:
            if attempt < retries - 1:
                # If there's an error, print it and wait before retrying
                print(f"Error: {e}, retrying in {delay} seconds...")
                time.sleep(delay)  # Wait time before retrying
            else:
                # Return None if all attempts fail
                return None  

def get_mempool_fees(retries=2, delay=10):
    """Fetches recommended mempool fees from the API."""
    url = 'https://mempool.space/api/v1/fees/recommended'
    response = get_with_retries(url, retries, delay)
    if response:
        return response.json()  # Return the JSON response
    return f"Error retrieving mempool fees."  # Error message if retrieval fails

def get_bitcoin_data(currency=CURRENCY, retries=2, delay=10):
    """Fetches Bitcoin market data based on the specified currency."""
    url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&ids={BITCOIN_ID}'
    response = get_with_retries(url, retries, delay)
    if response:
        price_data = response.json()  # Parse the JSON response
        return price_data[0]  # Return the first object containing Bitcoin data
    return f"Error retrieving Bitcoin data."  # Error message if retrieval fails

def get_block_height(retries=2, delay=10):
    """Fetches the current block height from the blockchain."""
    response = get_with_retries(URL_BLOCK, retries, delay)
    if response:
        return int(response.text)  # Return block height as an integer
    return f"Error retrieving block height."  # Error message if retrieval fails

def get_hashrate(retries=2, delay=10):
    """Fetches the current Bitcoin network hashrate."""
    response = get_with_retries(HASHRATE_URL, retries, delay)
    if response:
        hashrate_data = response.json()  # Parse the JSON response
        # Convert the hashrate to Exahash/s for easier readability
        return float(hashrate_data['currentHashrate']) / 1_000_000_000_000_000  
    return f"Error retrieving hashrate."  # Error message if retrieval fails

def get_unconfirmed_tx(retries=2, delay=10):
    """Fetches the number of unconfirmed Bitcoin transactions."""
    response = get_with_retries(UNCONFIRMED_TX_URL, retries, delay)
    if response:
        unconf_tx_data = response.json()  # Parse the JSON response
        return unconf_tx_data['count']  # Return the count of unconfirmed transactions
    return f"Error retrieving unconfirmed transactions."  # Error message if retrieval fails

def format_price(price):
    """Formats the price for output with proper thousands separator."""
    return "{:,.0f}".format(price).replace(",", ".")  # Format price with '.' as thousands separator

def format_fees(hour_fee, half_hour_fee, fastest_fee):
    """Formats different fee values for better readability."""
    formatted_hour_fee = locale.format_string('%d', hour_fee, grouping=True)
    formatted_half_hour_fee = locale.format_string('%d', half_hour_fee, grouping=True)
    formatted_fastest_fee = locale.format_string('%d', fastest_fee, grouping=True)
    return formatted_hour_fee, formatted_half_hour_fee, formatted_fastest_fee

def format_bitcoin_price(price, currency):
    """Formats Bitcoin price for output based on the specified currency."""
    formatted_price = "{:,.0f}".format(price).replace(",", "X").replace(".", ",").replace("X", ".")  # Replaces commas with periods and vice versa for formatting
    return f"{formatted_price}"

def format_with_thousands_separator(value):
    """Formats a number with thousands separator for easier readability."""
    return "{:,.0f}".format(value).replace(",", ".")  # Use '.' as thousands separator

def get_formatted_data(currency=CURRENCY):
    """Fetches all required data and returns it formatted for output."""
    bitcoin_data = get_bitcoin_data(currency)  # Fetch Bitcoin data based on the specified currency

    # Check if bitcoin_data is a dictionary (indicating no error)
    if isinstance(bitcoin_data, dict):
        # Fetch additional data needed for output
        mempool_fees = get_mempool_fees()
        block_height = get_block_height()
        hashrate = get_hashrate()
        unconfirmed_tx = get_unconfirmed_tx()

        # Extract relevant Bitcoin data from the fetched data
        bitcoin_price = bitcoin_data['current_price']
        price_change_24h = bitcoin_data['price_change_percentage_24h']
        market_cap = bitcoin_data['market_cap']
        high_24h = bitcoin_data['high_24h']
        low_24h = bitcoin_data['low_24h']
        circulating_supply = bitcoin_data['circulating_supply']
        volume_24h = bitcoin_data['total_volume']

        # New All-Time High (ATH) data
        ath = bitcoin_data['ath']
        ath_change_percentage = bitcoin_data['ath_change_percentage']
        ath_date = bitcoin_data['ath_date']

        # Format prices for output
        formatted_price = format_bitcoin_price(bitcoin_price, currency)
        formatted_high_24h = format_bitcoin_price(high_24h, currency)
        formatted_low_24h = format_bitcoin_price(low_24h, currency)

        # Format market cap with thousands separator
        formatted_market_cap = format_with_thousands_separator(market_cap)

        formatted_volume = format_with_thousands_separator(volume_24h)  # Format volume with thousands separator
        formatted_circulating_supply = format_price(circulating_supply)  # Format circulating supply for output
        formatted_ath = format_bitcoin_price(ath, currency)  # Format ATH for output

        # Calculate the number of missing Bitcoins and the percentage of total supply
        total_bitcoins = 21_000_000  # Total number of Bitcoins that can ever exist
        missing_bitcoins = total_bitcoins - circulating_supply  # Calculate how many Bitcoins are missing
        # Calculate percentage of missing Bitcoins, ensuring we do not divide by zero
        percentage_missing = (missing_bitcoins / total_bitcoins) * 100 if total_bitcoins > 0 else 0  

        # Format the number of missing Bitcoins for output
        formatted_missing_bitcoins = format_with_thousands_separator(missing_bitcoins)

        # Format the mempool fees if available
        if mempool_fees:
            formatted_hour_fee, formatted_half_fee, formatted_fastest_fee = format_fees(
                mempool_fees.get('hourFee'),
                mempool_fees.get('halfHourFee'),
                mempool_fees.get('fastestFee')
            )
            fees_output = f"{formatted_hour_fee}·{formatted_half_fee}·{formatted_fastest_fee}"  # Create output string for fees

        # Add currency symbol and currency code for display
        currency_symbol = currency_symbols[currency]  # Retrieve the currency symbol from currencies.py
        currency_code = currencies[currency]  # Retrieve the currency code

        return {
            'formatted_price': formatted_price,
            'price_change_24h': price_change_24h,
            'formatted_high_24h': formatted_high_24h,
            'formatted_low_24h': formatted_low_24h,
            'block_height': locale.format_string('%d', block_height, grouping=True),  # Format block height for output
            'hashrate': locale.format_string('%d', int(hashrate), grouping=True) if hashrate else None,  # Format hashrate if available
            'unconfirmed_tx': locale.format_string('%d', unconfirmed_tx, grouping=True) if unconfirmed_tx else None,  # Format unconfirmed transactions if available
            'formatted_volume': formatted_volume,
            'formatted_market_cap': formatted_market_cap,  # Return formatted market cap without conversion
            'formatted_circulating_supply': formatted_circulating_supply,
            'formatted_ath': formatted_ath,
            'ath_change_percentage': ath_change_percentage,
            'ath_date': ath_date,
            'formatted_missing_bitcoins': formatted_missing_bitcoins,  # Formatted number of missing Bitcoins
            'percentage_missing': percentage_missing,  # Percentage of missing Bitcoins
            'fees_output': fees_output if mempool_fees else "Error retrieving mempool fees.",  # Output fees or error
            'currency_symbol': currency_symbol,  # Add currency symbol for display
            'currency_code': currency_code  # Add currency code for display
        }
    else:
        # Return None if there was an error retrieving Bitcoin data
        return None

