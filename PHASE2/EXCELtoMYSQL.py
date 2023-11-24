import os
import pandas as pd
from sqlalchemy import create_engine

def import_excel_files_to_mysql(username, password, database, directory_path):
    num = 0

    # Create a SQLAlchemy engine
    engine = create_engine(f'mysql+pymysql://{username}:{password}@localhost:3306/{database}')

    # Get a list of files in the specified directory
    files = os.listdir(directory_path)

    for file_name in files:
        if file_name.lower().endswith('.pdf'):
            # Process PDF file (add your PDF processing logic here)
            print(f"Processing PDF file: {file_name}")
        elif file_name.lower().endswith(('.xls', '.xlsx')):
            # Read Excel file into a DataFrame
            data = pd.read_excel(os.path.join(directory_path, file_name), header=0)

            # Use the Excel file name (without extension) as the table name
            table_name = os.path.splitext(file_name)[0]

            # Write DataFrame to MySQL table
            data.to_sql(name=table_name, con=engine, index=False, if_exists='append')

            # Increment counter
            num += 1

            print('Imported', file_name)

    print('Total imported:', num)

# Example usage:
import_excel_files_to_mysql(username=' ', password=' ', database=' ', directory_path=r' ')
