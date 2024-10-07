from PyQt5.QtWidgets import QMessageBox

def show_info(main_window):
    """Displays an information message."""
    message = """
        <p><strong>Bitcoin Widget (BiWi)</strong><br>
        <em>Version 0.1.9</em></p>

        <p><strong>Information:</strong></p>
        <ul>
            <li>Automatic updates every 10 minutes</li>
            <li>Instant update via double-click</li>
            <li>Changes are saved and loaded on next startup</li>
            <li>Drag the window with the left mouse button.</li>
        </ul>
        
        <p><strong>Context Menu (right-click):</strong></p>
        <ul>
            <li>Change currency</li>
            <li>Show/hide specific data points</li>
            <li>Change font size</li>
            <li>Change background color</li>
            <li>Change font color</li>
            <li>Adjust transparency (0-255)</li>
            <li>View info and donation link</li>
            <li>Exit the application</li>
        </ul>
        
        <p><strong>Support us:</strong> 
        <a href='https://coinos.io/Bitcoininfo'>Donate here.</a></p>
    """
    
    QMessageBox.information(main_window, "Information", message, QMessageBox.Ok)


