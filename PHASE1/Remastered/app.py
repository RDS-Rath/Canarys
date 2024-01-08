from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import PyPDF2
import tabula
import pandas as pd
import os

app = Flask(__name__)

# Define the allowed file extensions for upload
ALLOWED_EXTENSIONS = {'pdf'}

# Define the keywords you want to search for
keywords = ["keyword1", "keyword2", "keyword3"]

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract tables from PDF
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

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)
        
        # If the file is valid
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))  # Save the uploaded file to 'uploads' folder
            output_excel_file = process_pdf(os.path.join('uploads', filename))  # Process the PDF file
            
            if output_excel_file:
                return render_template('done.html', filename=output_excel_file)
            else:
                return render_template('error.html')
    
    return render_template('index.html')

# Function to process the uploaded PDF file
def process_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))
        output_excel_file = os.path.join('uploads', 'output_tables.xlsx')
        
        with pd.ExcelWriter(output_excel_file, engine='openpyxl') as excel_writer:
            for page_num in range(len(pdf_reader.pages)):
                try:
                    tables = tabula.io.read_pdf(pdf_file, pages=page_num + 1, multiple_tables=True)
                    if tables:
                        for table in tables:
                            if search_keywords_in_table(table):
                                table.to_excel(excel_writer, sheet_name=f'Page{page_num + 1}', index=False)
                except Exception as e:
                    print(f"Error processing page {page_num + 1}: {str(e)}")
        
        return output_excel_file
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return None

# Route for downloading the processed Excel file
@app.route('/download/<filename>')
def download_file(filename):
    path_to_file = 'uploads/' + filename  # Assuming the file is in the 'uploads' folder
    return send_file(path_to_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    
