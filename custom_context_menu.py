from PyQt5.QtWidgets import QMenu, QAction  # Import QMenu and QAction classes
from currencies import currencies  # Import currency data
from functools import partial  # Import partial for callback functions
from info import show_info  # Import the show_info function

class CustomContextMenu:
    def __init__(self, main_window):
        """Initializes the custom context menu with a reference to the main window."""
        self.main_window = main_window

    def create_context_menu(self, pos):
        """Creates the context menu at the specified position."""
        context_menu = QMenu(self.main_window)  # Create a new context menu

        # Add currency submenu
        context_menu.addMenu(self.create_currency_menu())  # Add the currency menu

        # Add general actions
        self.add_action(context_menu, "Show Options", self.main_window.open_settings)  # Add Show Options action
        self.add_action(context_menu, "Font Size", self.main_window.change_font_size)  # Add Font Size action
        self.add_action(context_menu, "Font Color", self.main_window.change_text_color)  # Add Font Color action
        self.add_action(context_menu, "Background", self.main_window.change_background_color)  # Add Background action
        self.add_action(context_menu, "Transparency", self.main_window.change_transparency)  # Add Transparency action
        self.add_action(context_menu, "Info", lambda: show_info(self.main_window))  # Add Info action
        self.add_action(context_menu, "Close", self.main_window.close)  # Add Close action

        context_menu.exec_(self.main_window.mapToGlobal(pos))  # Execute the context menu at the specified position

    def create_currency_menu(self):
        """Creates the submenu for currency selection."""
        currency_menu = QMenu("Currencies", self.main_window)  # Create a currency menu
        for code, name in currencies.items():  # Iterate through available currencies
            action = QAction(name, self.main_window)  # Create an action for each currency
            action.triggered.connect(partial(self.main_window.set_currency, code))  # Connect action to set currency
            currency_menu.addAction(action)  # Add action to the currency menu
        return currency_menu  # Return the completed currency menu

    def add_action(self, menu, name, callback):
        """Helper method to add actions to a menu."""
        action = QAction(name, self.main_window)  # Create a new action with the specified name
        action.triggered.connect(callback)  # Connect the action to the provided callback
        menu.addAction(action)  # Add action to the specified menu

