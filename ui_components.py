from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QFont


class UIComponents(QWidget):
    def __init__(self, font_color, font_size):
        """Initializes the UIComponents class, setting up the layout and labels.
        
        Args:
            font_color (QColor): The color of the font for the labels.
            font_size (int): The size of the font for the labels.
        """
        super().__init__()

        # Layout configuration
        self.layout = QVBoxLayout()  # Create a vertical box layout
        self.layout.setSpacing(0)  # Set the spacing between rows to 0 pixels
        self.layout.setContentsMargins(5, 5, 5, 5)  # Set 5px margin on all sides

        # Labels for displaying output data
        self.output_labels = {}
        for label_name in [
            "Price", "Change", "Low", "High",  # Removed (24h)
            "ATH", "Market Cap", "Volume", "Mined", 
            "Remaining", "Remaining %", "Block Height", 
            "Hashrate", "Unconfirmed TX", "Fees"
        ]:
            # Create a QLabel for each output label
            self.output_labels[label_name] = QLabel(self)
            # Set the label's stylesheet for transparency and font color
            self.output_labels[label_name].setStyleSheet(f"background: transparent; color: {font_color.name()};")
            # Add the label to the layout
            self.layout.addWidget(self.output_labels[label_name])

        # Apply the layout to the widget
        self.setLayout(self.layout)

        # Set the font for all labels to Monospace
        self.monospace_font = QFont("Liberation Mono", font_size)
        for label in self.output_labels.values():
            label.setFont(self.monospace_font)

    def update_labels(self, processed_data):
        """Updates the labels with formatted data.

        Args:
            processed_data (dict): A dictionary containing formatted strings for each label.
        """
        for label_name, text in processed_data.items():
            # Update the text for each label with the corresponding formatted data
            label = self.output_labels[label_name]
            label.setText(text)
            label.setMinimumSize(0, 0)  # Remove minimum size constraints to allow window resizing

