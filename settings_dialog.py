from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton

class SettingsDialog(QDialog):
    def __init__(self, output_labels, parent=None):
        """Initializes the SettingsDialog for adjusting label visibility settings.

        Args:
            output_labels (dict): A dictionary of output labels from the main window.
            parent (QWidget, optional): The parent widget for the dialog. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowTitle("Settings")  # Set the window title to "Settings"
        self.setGeometry(100, 100, 300, 400)  # Set the initial size and position of the dialog

        self.output_labels = output_labels  # Store the output labels from the main window
        self.label_checkboxes = {}  # Dictionary to store the checkboxes for label visibility

        layout = QVBoxLayout()  # Create a vertical box layout for the dialog

        # Create a checkbox for each label to control its visibility
        self.checkbox_layout = QVBoxLayout()  # Layout for checkboxes
        for label_name in output_labels.keys():
            checkbox = QCheckBox(label_name)  # Create a checkbox for the label
            checkbox.setChecked(self.output_labels[label_name].isVisible())  # Set initial visibility based on the label's visibility
            checkbox.toggled.connect(self.update_label_visibility)  # Connect the checkbox toggle signal to update visibility
            self.checkbox_layout.addWidget(checkbox)  # Add the checkbox to the layout
            self.label_checkboxes[label_name] = checkbox  # Store the checkbox for later access

        layout.addLayout(self.checkbox_layout)  # Add the checkbox layout to the main layout

        # Add an OK button to confirm changes
        ok_button = QPushButton("OK")  # Create an OK button
        ok_button.clicked.connect(self.accept)  # Connect the button's click signal to accept the dialog
        layout.addWidget(ok_button)  # Add the button to the main layout

        self.setLayout(layout)  # Set the main layout for the dialog

    def update_label_visibility(self):
        """Updates the visibility of labels based on the checkboxes' state."""
        for label_name, checkbox in self.label_checkboxes.items():
            label = self.output_labels.get(label_name)  # Get the label associated with the checkbox
            if label:
                label.setVisible(checkbox.isChecked())  # Set the label's visibility based on the checkbox state

        # Call the parent method to adjust the size of the main window
        if self.parent():
            self.parent().adjustSize()  # Adjust the size of the parent window

