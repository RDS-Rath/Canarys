import PyPDF2
import tabula
import pandas as pd
import openpyxl

# Define the keywords you want to search for
keywords = ['Eligibility', 'Criteria', 'completed', 'signed', 'Proof', 'Entry', 'Professional', 'ISO', 'insolvency', 'regulations', 'Certification', 'pre-qualification', 'liquidation', 'compliance']

# Open the PDF file
pdf_file = r"Sample_Tenders/RFP_Oct_104/Dokus/TR_02_Leistungsbeschreibung_DDF_23_Los2.pdf"
pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))

# Define the path and name for the output Excel file
output_excel_file = r"output_tables.xlsx"  # Change this to your desired path and name

# extract tables from PDF
def extract_tables_from_pdf(pdf_file):
    tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
    return tables

# Function to search for keywords in a table
def search_keywords_in_table(table):
    found = False
    for keyword in keywords:
        if any(table.apply(lambda row: row.str.contains(keyword, case=False).any(), axis=1)):
            found = True
            break
    return found

# Create an Excel writer to export matching tables
excel_writer = pd.ExcelWriter(output_excel_file, engine='openpyxl')
workbook = excel_writer.book

# Create a Pandas ExcelWriter object for writing to Excel
with pd.ExcelWriter(output_excel_file, engine='openpyxl') as excel_writer:
    for page_num in range(len(pdf_reader.pages)):
        try:
            tables = tabula.read_pdf(pdf_file, pages=page_num + 1, multiple_tables=True)
            if tables:
                for table in tables:
                    if search_keywords_in_table(table):
                        # Export the matching table to Excel
                        table.to_excel(excel_writer, sheet_name=f'Page{page_num + 1}', index=False)
        except Exception as e:
            print(f"Error processing page {page_num + 1}: {str(e)}")
