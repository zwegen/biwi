# BiWi

This widget is a simple and customizable Bitcoin data display tool for Linux users. It fetches real-time information about Bitcoin, providing users with up-to-date data such as price, fees, market capitalization, and more.

The widget is highly customizable, allowing users to adjust font size, font color, background color, and transparency to suit their preferences. Its intuitive interface makes it easy to monitor Bitcoin information at a glance, enhancing the overall user experience.

## Description

This project implements a graphical user interface (GUI) to retrieve and display Bitcoin information. It utilizes the PyQt5 library for the GUI framework. The application allows users to view real-time Bitcoin metrics, such as price, market capitalization, and 24-hour highs and lows. Additionally, users can customize the display settings, including font size, color, background color, and widget transparency. The widget automatically updates the data at regular intervals, providing users with up-to-date information at their fingertips.

## Features

- Displays current Bitcoin data such as price, market capitalization, 24h high/low, and more.
- Adjustable font size and color.
- Customizable background color and widget transparency.
- Option to select different currencies for data display.
- Saves window position and size, restoring it on restart.
- Automatically fetches Bitcoin data at regular intervals.

## Customization

### Change Font Size:

Right-click on the widget to open the context menu and select "Font Size" to adjust the size of the font. A dialog will appear, allowing you to choose a font size between 6 and 72 points.

### Change Font Color:

Right-click on the widget and select "Font Color" to pick a new color from the color dialog. This allows you to customize the text color of all displayed information.

### Background Color and Transparency:

The background color can be adjusted via the context menu by selecting "Background." A color dialog will open, enabling you to choose your preferred background color. Additionally, you can change the transparency of the widget through the "Transparency" option in the context menu. This option allows you to set the transparency level between 0 (completely opaque) and 255 (completely transparent), giving you control over how much of the underlying desktop is visible.

### Select Currency:

To change the currency displayed for Bitcoin data, right-click on the widget and navigate to the "Currencies" submenu. Here, you can choose from a list of supported currencies, ensuring that you see the Bitcoin data in your preferred format.

### Toggle Information Visibility:

You can customize which pieces of information are displayed by accessing the settings dialog through the context menu ("Show Options"). This allows you to toggle the visibility of various data points, ensuring that only the information you want to see is presented on the widget.

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.html) file for details.

  ![Main window](https://github.com/zwegen/biwi/blob/main/screenshots/biwi_screenshot_001.png?raw=true)

