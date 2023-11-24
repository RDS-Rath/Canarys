import pandas as pd
from sqlalchemy import create_engine

def check_excel_against_criteria(username, password, database, criteria_table_name, excel_file_path):
    # Create a SQLAlchemy engine
    engine = create_engine(f'mysql+pymysql://{username}:{password}@localhost:3306/{database}')

    # Read criteria from SQL table into DataFrame
    criteria_df = pd.read_sql_table(criteria_table_name, con=engine)

    # Read Excel file into DataFrame
    excel_df = pd.read_excel(excel_file_path, header=0)

    # Check for missing criteria in the Excel DataFrame
    missing_criteria = find_missing_criteria(excel_df, criteria_df)

    # Calculate the score based on the percentage of satisfied criteria
    total_criteria = criteria_df.size
    satisfied_criteria = total_criteria - len(missing_criteria)
    score = (satisfied_criteria / total_criteria) * 100

    print(f"Score: {score:.2f}/100")

    if not missing_criteria:
        print("All criteria satisfied in the Excel file.")
    else:
        print("Missing criteria in the Excel file:")
        for criterion_column, criterion_value in missing_criteria:
            print(f"{criterion_column}: {criterion_value}")

def find_missing_criteria(excel_df, criteria_df):
    # Initialize a list to store missing criteria
    missing_criteria = []

    # Check for missing criteria in each column of the criteria DataFrame
    for criteria_column in criteria_df.columns:
        for criteria_value in criteria_df[criteria_column]:
            # Perform case-insensitive comparison
            if all(criteria_value.casefold() not in value.casefold() for value in excel_df[criteria_column]):
                missing_criteria.append((criteria_column, criteria_value))

    return missing_criteria

# Example usage:
check_excel_against_criteria(username=' ', password=' ', database=' ',
                              criteria_table_name=' ', excel_file_path=r' ')
