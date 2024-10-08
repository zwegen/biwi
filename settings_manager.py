import json
from PyQt5.QtGui import QColor


class SettingsManager:
    def __init__(self, filename="settings.json"):
        """Initializes the SettingsManager with a filename for the JSON file."""
        self.filename = filename

    def save_settings(self, settings):
        """Saves the current settings to a JSON file.
        
        Args:
            settings (dict): A dictionary containing the settings.
        """
        with open(self.filename, "w") as f:
            json.dump(settings, f, indent=4)  # indent=4 for better readability

    def load_settings(self):
        """Loads saved settings from a JSON file.
        
        Returns:
            dict: A dictionary with the loaded settings or default values if the file is not found.
        """
        try:
            with open(self.filename, "r") as f:
                settings = json.load(f)
                return settings
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default values if the file does not exist or is invalid
            return {
                "background_color": [0, 0, 0, 200],  # Default background color (Black with 200 Alpha)
                "font_color": [255, 255, 255],  # Default font color (White)
                "transparency": 200,  # Default transparency
                "font_size": 10,  # Default font size
                "currency": "USD",  # Default currency
                "label_visibility": {
                    "Price": True,  # Visibility of the Price label
                    "Change (24h)": True,  # Visibility of the Change (24h) label
                    "High": True,  # Visibility of the High label
                    "Low": True,   # Visibility of the Low label
                    "Market Cap": True,  # Visibility of the Market Cap label
                    "Volume": True,  # Visibility of the Volume label
                    "Mined": True,  # Visibility of the Mined label
                    "Unmined": True,  # Visibility of the Remaining Bitcoins label
                    "Unmined %": True,  # Visibility of the Remaining percentage label
                    "Block Height": True,  # Visibility of the Block Height label
                    "Hashrate": True,  # Visibility of the Hashrate label
                    "Unconfirmed TX": True,  # Visibility of the Unconfirmed Transactions label
                    "ATH": True,  # Visibility of the All-Time High label
                    "Fees": True,  # Visibility of the Fees label
                }
            }
