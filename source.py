import xml.etree.ElementTree as Etree
import pandas as pd
from lxml import etree as Etree
import os

# cross-platform 'downloads' directory 
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")    

try:
    parser = Etree.XMLParser(recover=True)  # recover from errors
    input_name = "store.xml"
    initial_xml = os.path.join(downloads_dir, f"{input_name}")
    Tree = Etree.parse(initial_xml)
    root = Tree.getroot()

    A = []
    # εδώ δοκιμάζω διάφορα tags, όπου έχει το κενό --> ('.//_______'.lower()) --> πχ: './/item'.lower() './/product'.lower() './/post'.lower() 
    for product in root.findall('.//product'):      # item / product / post / ITEM / PRODUCT / POST ... 
        B = {}
        for elem in product:
            B[elem.tag.lower()] = elem.text
        A.append(B)

    df = pd.DataFrame(A)
    df.drop_duplicates(keep='first', inplace=True)
    
    # choose output name
    output_name = "whatever u want"
    
    csv_output_path = os.path.join(downloads_dir, f"{output_name}.csv")
    xlsx_output_path = os.path.join(downloads_dir, f"{output_name}.xlsx")
    
    # export to xlsx
    writer = pd.ExcelWriter(xlsx_output_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:Z', 30)
    writer._save()

    # export to csv 
    df.to_csv(csv_output_path, index=False)

    print("yoloo")
except Etree.ParseError as e:
    print(f"XML Parse Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
