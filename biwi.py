#!/usr/bin/env python3

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
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)  # Set the window background to transparent
        self.setWindowFlags(Qt.FramelessWindowHint)  # Window without borders
        self.setWindowTitle("Bitcoin Data")
        self.setGeometry(100, 100, 400, 400)

        # Load settings
        self.settings_manager = SettingsManager()  # Instantiate the SettingsManager
        settings = self.settings_manager.load_settings()  # Load the settings

        # Load background color with transparency
        self.background_color = QColor(*settings["background_color"], settings["transparency"])  # Add transparency here
        self.font_color = QColor(*settings["font_color"])  # Font color
        self.font_size = settings["font_size"]  # Font size
        self.currency = settings["currency"]  # Currency

        # Load window position
        if "position" in settings:
            self.move(*settings["position"])  # Set window position

        # Instantiate UI components
        self.ui_components = UIComponents(self.font_color, self.font_size)  # Pass colors and font size
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.ui_components)
        self.setLayout(self.layout)

        # Initialize label visibility
        for label_name, is_visible in settings.get("label_visibility", {}).items():
            if label_name in self.ui_components.output_labels:  # Check if the label exists
                self.ui_components.output_labels[label_name].setVisible(is_visible)

        # Timer for automatically fetching data
        self.timer = QTimer(self)
        self.timer.setInterval(600000)  # 10 minutes in milliseconds
        self.timer.timeout.connect(self.fetch_data)
        self.timer.start()

        # Initial data fetch
        self.fetch_data()

        # Automatically adjust window size
        self.adjustSize()  # Adjust the window size here

        # Initialize context menu
        self.context_menu = CustomContextMenu(self)  # Create context menu

        # Bind the context menu to the custom method
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        # Variables for moving the window
        self.drag_position = QPoint(0, 0)

    def paintEvent(self, event):
        """Paints the window with rounded corners and the background color."""
        painter = QPainter(self)
        rect = self.rect()
        painter.setBrush(self.background_color)  # Use the chosen background color
        painter.setPen(Qt.NoPen)  # No border
        painter.drawRoundedRect(rect, 20, 20)  # Round the corners

    def show_context_menu(self, pos):
        """Displays the context menu at the specified position."""
        self.context_menu.create_context_menu(pos)  # Show context menu

    def mouseDoubleClickEvent(self, event):
        """Updates the data on double-click."""
        self.fetch_data()

    def set_currency(self, currency):
        """Sets the currency and updates the data."""
        self.currency = currency
        self.fetch_data()
        self.save_settings()

    def open_settings(self):
        """Opens the settings dialog and updates visibility."""
        settings_dialog = SettingsDialog(self.ui_components.output_labels, self)  # Pass the main window
        if settings_dialog.exec_():  # Save only if the dialog is accepted
            self.save_settings()  # Save the current settings if dialog is accepted
        
            # Update only the visibility of labels based on the new settings
            for label_name, is_visible in self.settings_manager.load_settings().get("label_visibility", {}).items():
                if label_name in self.ui_components.output_labels:  # Check if the label exists
                    self.ui_components.output_labels[label_name].setVisible(is_visible)

            # Adjust window size after visibility changes
            self.adjustSize()  # Adjust the window size

    def change_text_color(self):
        """Changes the font color of all labels."""
        color = QColorDialog.getColor()
        if color.isValid():
            for label in self.ui_components.output_labels.values():
                label.setStyleSheet(f"background: transparent; color: {color.name()};")
            self.font_color = color
            self.save_settings()

    def change_background_color(self):
        """Changes the background color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_color.setRed(color.red())
            self.background_color.setGreen(color.green())
            self.background_color.setBlue(color.blue())
            self.update()  # Updates the widget
            self.save_settings()

    def change_transparency(self):
        """Changes the transparency."""
        transparency, ok = QInputDialog.getInt(self, "Change Transparency", "Select transparency (0-255):", value=self.background_color.alpha(), min=0, max=255)
        if ok:
            self.background_color.setAlpha(transparency)
            self.update()
            self.save_settings()

    def change_font_size(self):
        """Changes the font size."""
        font_size, ok = QInputDialog.getInt(self, "Change Font Size", "Select font size:", value=self.ui_components.monospace_font.pointSize(), min=6, max=72)
        if ok:
            self.ui_components.monospace_font.setPointSize(font_size)
            for label in self.ui_components.output_labels.values():
                label.setFont(self.ui_components.monospace_font)
                label.setMinimumSize(0, 0)  # Remove minimum size so the window can be resized

            # Adjust window size
            self.ui_components.updateGeometry()  # Recalculate layout
            self.adjustSize()  # Recalculate the window size
            self.save_settings()  # Save the new settings

    def fetch_data(self):
        """Fetches the Bitcoin data and updates the output."""
        data = get_formatted_data(self.currency)
        if data:
            processed_data = process_data(data)
            self.ui_components.update_labels(processed_data)  # Update the labels

            # Adjust window size after data update
            self.ui_components.updateGeometry()  # Recalculate layout
            self.adjustSize()  # Recalculate the window size
        else:
            handle_error()

    def save_settings(self):
        """Saves the current settings to a JSON file and updates the data."""
        settings = {
            "background_color": self.background_color.getRgb()[:3],
            "font_color": self.font_color.getRgb()[:3],
            "transparency": self.background_color.alpha(),
            "font_size": self.ui_components.monospace_font.pointSize(),
            "currency": self.currency,
            "label_visibility": {label_name: label.isVisible() for label_name, label in self.ui_components.output_labels.items()},
            "position": (self.pos().x(), self.pos().y())  # Save the current widget position as a tuple
        }
        print(f"Saving settings: {settings}")  # Debugging output
        self.settings_manager.save_settings(settings)  # Use the SettingsManager

    def closeEvent(self, event):
        """Event handler when closing the window."""
        self.save_settings()  # Save settings on close
        event.accept()  # Close the window

    # Add methods to move the window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundedWidget()
    window.show()
    sys.exit(app.exec_())
