import os
import xml.etree.ElementTree as Etree
import pandas as pd
from lxml import etree as Etree
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import sys
import time
import requests

# cross-platform 'downloads' directory 
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")    

def download_xml(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # check for errors
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"XML file downloaded successfully from {url} to {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        print(f"error downloading the XML file: {e}")
        sys.exit(1)

def choose_input_method():
    def local_file():
        root.choice = "local"
        root.quit()

    def enter_link():
        root.choice = "link"
        root.quit()

    root = tk.Tk()
    root.title("select input method")
    root.geometry("300x150")
    root.choice = None

    label = tk.Label(root, text="choose an XML input method:")
    label.pack(pady=10)

    local_button = tk.Button(root, text="local XML File", command=local_file)
    local_button.pack(pady=5)

    link_button = tk.Button(root, text="enter XML Link", command=enter_link)
    link_button.pack(pady=5)

    root.mainloop()
    return root.choice

def main():
    try:
        # Choose input method
        choice = choose_input_method()

        if choice == "local":
            root = tk.Tk()
            root.withdraw()  # Hide the main tkinter window
            xml_file_path = filedialog.askopenfilename(title="Select your XML file", filetypes=[("XML files", "*.xml")])
            if not xml_file_path:
                print("no file selected. exiting...")
                sys.exit(1)
        elif choice == "link":
            xml_url = simpledialog.askstring("XML URL", "enter the XML URL:")
            if not xml_url:
                print("no URL provided. byeee...")
                sys.exit(1)
            
            xml_file_path = os.path.join(os.getcwd(), "downloaded_xml.xml")
            xml_file_path = download_xml(xml_url, xml_file_path)
        else:
            print("no selection made. byeee...")
            sys.exit(1)

        # ask user for the output name
        output_name = simpledialog.askstring("output Name", "enter the output file name (without extension):")
        if not output_name:
            print("no output name entered. byeee...")
            sys.exit(1)

        # parse the XML
        parser = Etree.XMLParser(recover=True)
        tree = Etree.parse(xml_file_path, parser)
        root = tree.getroot()

        A = []
        tags_to_try = ['product', 'item', 'post', 'PRODUCT', 'ITEM', 'POST']

        found_tag = None
        for tag in tags_to_try:
            products = root.findall(f'.//{tag}')
            if products:
                found_tag = tag
                break

        if not found_tag:
            found_tag = simpledialog.askstring("tag NOT found", "common XML main-tags not found. enter the main tag manually:")

        if not found_tag:
            print("no valid tag entered. byeee...")
            sys.exit(1)

        for product in root.findall(f'.//{found_tag}'):
            B = {}
            for elem in product:
                B[elem.tag.lower()] = elem.text
            A.append(B)

        df = pd.DataFrame(A)
        df.drop_duplicates(keep='first', inplace=True)

        output_dir = os.path.dirname(xml_file_path)

        xlsx_output_path = os.path.join(output_dir, f"{output_name}.xlsx")
        writer = pd.ExcelWriter(xlsx_output_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        worksheet = writer.sheets['Sheet1']
        worksheet.set_column('A:Z', 30)
        writer._save()

        csv_output_path = os.path.join(output_dir, f"{output_name}.csv")
        df.to_csv(csv_output_path, index=False)

        print(f"files saved successfully:\n{xlsx_output_path}\n{csv_output_path}")

        print("script finished. waiting for 30 seconds before closing...")
        time.sleep(30)

    except Etree.ParseError as e:
        print(f"XML Parse Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
