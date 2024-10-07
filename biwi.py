import sys
import json
import os
from bitcoin_data import get_formatted_data  # Import function to fetch data from an external source
from data_processing import process_data, handle_error  # Import data processing functions
from settings_dialog import SettingsDialog
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QColorDialog, QInputDialog
)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QTimer, Qt, QPoint
from ui_components import UIComponents  # Import external UI components
from custom_context_menu import CustomContextMenu  # Import the custom context menu class
from currencies import currencies  # Import currency data
from settings_manager import SettingsManager  # Import the SettingsManager class

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class RoundedWidget(QWidget):
    def __init__(self):
        """Initializes the main application window with rounded corners and transparent background."""
        super().__init__()

        # Set window flags to hide the window from the taskbar
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)  # Hide window from taskbar

        self.setAttribute(Qt.WA_TranslucentBackground)  # Set the window background to transparent
        self.setWindowTitle("Bitcoin Data")  # Set the window title
        self.setGeometry(100, 100, 400, 400)  # Set the initial position and size of the window

        # Load settings
        self.settings_manager = SettingsManager()  # Instantiate the SettingsManager
        settings = self.settings_manager.load_settings()  # Load the settings

        # Load background color with transparency
        self.background_color = QColor(*settings["background_color"], settings["transparency"])  # Include transparency
        self.font_color = QColor(*settings["font_color"])  # Set font color
        self.font_size = settings["font_size"]  # Set font size
        self.currency = settings["currency"]  # Set currency

        # Load window position
        if "position" in settings:
            self.move(*settings["position"])  # Set the window position

        # Instantiate UI components
        self.ui_components = UIComponents(self.font_color, self.font_size)  # Pass font color and size
        self.layout = QVBoxLayout()  # Create a vertical layout
        self.layout.addWidget(self.ui_components)  # Add UI components to the layout
        self.setLayout(self.layout)  # Set the layout for the main widget

        # Initialize label visibility based on settings
        for label_name, is_visible in settings.get("label_visibility", {}).items():
            if label_name in self.ui_components.output_labels:  # Check if the label exists
                self.ui_components.output_labels[label_name].setVisible(is_visible)  # Set visibility

        # Timer for automatic data fetching
        self.timer = QTimer(self)  # Create a timer
        self.timer.setInterval(600000)  # Set interval to 10 minutes in milliseconds
        self.timer.timeout.connect(self.fetch_data)  # Connect timeout signal to fetch data
        self.timer.start()  # Start the timer

        # Initial data fetching
        self.fetch_data()

        # Automatically adjust window size
        self.adjustSize()  # Adjust the window size

        # Initialize context menu
        self.context_menu = CustomContextMenu(self)  # Create a context menu

        # Bind the context menu to the custom method
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)  # Show context menu on request

        # Variables for moving the window
        self.drag_position = QPoint(0, 0)  # Initialize drag position

    def paintEvent(self, event):
        """Paints the window with rounded corners and the specified background color."""
        painter = QPainter(self)
        rect = self.rect()  # Get the rectangle of the widget
        painter.setBrush(self.background_color)  # Use the selected background color
        painter.setPen(Qt.NoPen)  # Set no border
        painter.drawRoundedRect(rect, 20, 20)  # Draw rounded corners

    def show_context_menu(self, pos):
        """Displays the context menu at the specified position."""
        self.context_menu.create_context_menu(pos)  # Show the context menu

    def mouseDoubleClickEvent(self, event):
        """Updates the data on double-click."""
        self.fetch_data()  # Fetch new data

    def set_currency(self, currency):
        """Sets the currency and updates the data."""
        self.currency = currency  # Set the currency
        self.fetch_data()  # Fetch data
        self.save_settings()  # Save settings after currency change

    def open_settings(self):
        """Opens the settings dialog and updates label visibility."""
        settings_dialog = SettingsDialog(self.ui_components.output_labels, self)  # Pass the main window to the dialog
        if settings_dialog.exec_():  # Only save if the dialog is accepted
            self.save_settings()  # Save current settings when the dialog is accepted

            # Update label visibility based on new settings
            for label_name, is_visible in self.settings_manager.load_settings().get("label_visibility", {}).items():
                if label_name in self.ui_components.output_labels:  # Check if the label exists
                    self.ui_components.output_labels[label_name].setVisible(is_visible)  # Set visibility

            # Adjust window size after visibility changes
            self.adjustSize()  # Adjust window size

    def change_text_color(self):
        """Changes the text color of all labels."""
        color = QColorDialog.getColor()  # Open color dialog to select a color
        if color.isValid():  # Check if the selected color is valid
            for label in self.ui_components.output_labels.values():  # Update all labels
                label.setStyleSheet(f"background: transparent; color: {color.name()};")  # Set the new text color
            self.font_color = color  # Update the font color
            self.save_settings()  # Save settings

    def change_background_color(self):
        """Changes the background color of the window."""
        color = QColorDialog.getColor()  # Open color dialog to select a color
        if color.isValid():  # Check if the selected color is valid
            self.background_color.setRed(color.red())  # Update red component
            self.background_color.setGreen(color.green())  # Update green component
            self.background_color.setBlue(color.blue())  # Update blue component
            self.update()  # Update the widget to reflect changes
            self.save_settings()  # Save settings

    def change_transparency(self):
        """Changes the transparency of the window."""
        transparency, ok = QInputDialog.getInt(self, "Change Transparency", "Select transparency (0-255):", value=self.background_color.alpha(), min=0, max=255)  # Open input dialog for transparency
        if ok:  # Check if the user confirmed the input
            self.background_color.setAlpha(transparency)  # Set new transparency
            self.update()  # Update the widget
            self.save_settings()  # Save settings

    def change_font_size(self):
        """Changes the font size of the labels."""
        font_size, ok = QInputDialog.getInt(self, "Change Font Size", "Select font size:", value=self.ui_components.monospace_font.pointSize(), min=6, max=72)  # Open input dialog for font size
        if ok:  # Check if the user confirmed the input
            self.ui_components.monospace_font.setPointSize(font_size)  # Update font size
            for label in self.ui_components.output_labels.values():  # Update all labels
                label.setFont(self.ui_components.monospace_font)  # Set the new font
                label.setMinimumSize(0, 0)  # Remove minimum size to allow window to shrink

            # Adjust window size after font size change
            self.ui_components.updateGeometry()  # Recalculate layout
            self.adjustSize()  # Recalculate window size
            self.save_settings()  # Save new settings

    def fetch_data(self):
        """Fetches Bitcoin data and updates the output labels."""
        data = get_formatted_data(self.currency)  # Fetch data for the selected currency
        if data:  # Check if data is available
            processed_data = process_data(data)  # Process the fetched data
            self.ui_components.update_labels(processed_data)  # Update the labels with processed data

            # Adjust window size after data update
            self.ui_components.updateGeometry()  # Recalculate layout
            self.adjustSize()  # Recalculate window size
        else:
            handle_error()  # Handle error if data fetching fails

    def save_settings(self):
        """Saves the current settings to a JSON file and updates data."""
        settings = {
            "background_color": self.background_color.getRgb()[:3],  # Save RGB components of background color
            "font_color": self.font_color.getRgb()[:3],  # Save RGB components of font color
            "transparency": self.background_color.alpha(),  # Save transparency
            "font_size": self.ui_components.monospace_font.pointSize(),  # Save font size
            "currency": self.currency,  # Save currency
            "label_visibility": {label_name: label.isVisible() for label_name, label in self.ui_components.output_labels.items()},  # Save visibility state of each label
            "position": (self.pos().x(), self.pos().y())  # Save current position of the widget as a tuple
        }
        print(f"Saving settings: {settings}")  # Debug output
        self.settings_manager.save_settings(settings)  # Use the SettingsManager to save settings
    
        # Update data after saving settings
        self.fetch_data()  # Fetch data after saving settings

    def closeEvent(self, event):
        """Handles the event when the window is closed."""
        self.save_settings()  # Save settings upon closing
        event.accept()  # Accept the event to close the window

    # Methods for moving the window
    def mousePressEvent(self, event):
        """Handles mouse press events for dragging the window."""
        if event.button() == Qt.LeftButton:  # Check if left mouse button is pressed
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()  # Calculate drag position
            event.accept()  # Accept the event

    def mouseMoveEvent(self, event):
        """Handles mouse move events for dragging the window."""
        if event.buttons() & Qt.LeftButton:  # Check if left mouse button is held down
            self.move(event.globalPos() - self.drag_position)  # Move the window according to mouse movement
            event.accept()  # Accept the event

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    window = RoundedWidget()  # Create the main window
    window.show()  # Show the main window
    sys.exit(app.exec_())  # Execute the application

