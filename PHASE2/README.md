### Overview
---------------------------------

EXCELtoMYSQL.py reads Excel files from a specified directory, processes them using pandas, and then imports the data into a MySQL database using SQLAlchemy.

ExcelValidator.py checks the Excel file against criteria from a MySQL table, calculating a score based on the percentage of satisfied criteria.

### Dependencies and Installation
---------------------------------
1. Clone the repository in your local machine.
2. Set up a Virtual Environment selecting python 3.11 as the interpreter. 
3. Install the required dependencies by running the following command:
   ```
   pip install SQLAlchemy==2.0.23
   ```
4. Make sure you have a MySQL server installed and running. Create a database and note down the username, password, and database name for later use.
5. Place the Excel files that you want to import into the MySQL database in a specific directory. Note the path to this directory.
6. Update the following parameters with your specific values in both Python files:
   ```
   username: Your MySQL username
   password: Your MySQL password
   database: Your MySQL database name
   directory_path: The path to the directory containing your Excel files
   ```
7. Run the script using
   ```
   python EXCELtoMYSQL.py
   ```
8. Run the script using
   ```
   python ExcelValidator.py
   ```
