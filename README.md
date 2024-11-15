# XML to Excel and CSV Converter

## Project Purpose
This Python script converts XML files, commonly used in e-shop and merchant online catalogs, into well-organized Excel (XLSX) and CSV files. Designed with ease-of-use in mind, it supports both local file selection and URL-based XML downloads. The script is especially helpful for e-commerce managers, data analysts, and businesses needing quick, reliable XML data conversion.

## Features
- Supports local XML files and downloads XML from a URL.
- Customizable output file names.
- Compatible with various main XML tags (product, item, post), or users can input a custom tag if necessary.
- Provides both Excel and CSV output files.

## Requirements
- Python 3.12.5
- Libraries specified in `requirements.txt`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/apo-veryk/xml-2-exl.git
   cd xml-2-exl
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
## Usage Instructions
1. **Run the Script**
   Run the script and follow the prompts to select a local XML file or download it from a URL.
   ```bash
   python main.py
   ```
2. **Input Methods**
   - Choose between a local XML file or enter a URL link when prompted.
   - The script will try common XML tags like <product>, <item>, or <post> but will prompt you to enter a custom tag if none are found automatically.

3. **Specify Output File Name**
   - Enter a desired name for the output files (without extension). The script will save the files in the same directory as the source XML file.

## Example of Packaging as a .exe (Optional)
- To make this script an executable (.exe) for easy distribution, you can use PyInstaller:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
2. **Run PyInstaller with the following command:**
   ```bash
   pyinstaller --onefile --noconsole main.py
   ```
- The .exe file will appear in the dist folder. This executable will allow users to run the script without needing Python installed.

## License
- This project is licensed under the [MIT License](https://github.com/apo-veryk/xml-2-exl/blob/main/LICENSE).
