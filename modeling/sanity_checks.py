import pandas as pd
from loguru import logger
import typer
import numpy as np

app = typer.Typer()

@app.command()
def check_features(features_path: str):
    logger.info("Loading features data...")
    df = pd.read_pickle(features_path)
    
    missing_values_report = {}
    unexpected_columns_report = []
    outliers_report = {}
    out_of_range_report = {}
    inconsistent_loan_report = 0
    
    logger.info("Checking for missing values...")
    missing_values = df.isnull().sum()
    missing_report = missing_values[missing_values > 0]
    if not missing_report.empty:
        missing_values_report = missing_report.to_dict()
    
    logger.info("Checking for unexpected dummy variables...")
    expected_columns = [
        'age', 'balance', 'day_of_week', 'duration', 'campaign', 'pdays',
        'previous', 'y', 'job_admin.', 'job_blue-collar', 'job_entrepreneur',
        'job_housemaid', 'job_management', 'job_retired', 'job_self-employed',
        'job_services', 'job_student', 'job_technician', 'job_unemployed',
        'marital_divorced', 'marital_married', 'marital_single',
        'education_primary', 'education_secondary', 'education_tertiary',
        'default_no', 'default_yes', 'housing_no', 'housing_yes', 'loan_no',
        'loan_yes', 'contact_cellular', 'contact_telephone', 'month_apr',
        'month_aug', 'month_dec', 'month_feb', 'month_jan', 'month_jul',
        'month_jun', 'month_mar', 'month_may', 'month_nov', 'month_oct',
        'month_sep', 'poutcome_failure', 'poutcome_other', 'poutcome_success'
    ]
    unexpected_columns = [col for col in df.columns if col not in expected_columns]
    if unexpected_columns:
        unexpected_columns_report = unexpected_columns
    
    logger.info("Checking for outliers in numerical features...")
    numerical_columns = ['age', 'day_of_week', 'duration', 'campaign', 'pdays', 'previous']
    for col in numerical_columns:
        if col in df.columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            outliers = df[z_scores > 3]
            if not outliers.empty:
                outliers_report[col] = outliers.shape[0]
    
    logger.info("Checking value ranges for numerical features...")
    value_range_checks = {
        'age': (0, 100),
        'day_of_week': (1, 31),  # day of month
        'duration': (0, float('inf')),
        'campaign': (1, float('inf')),
        'pdays': (-1, float('inf')),
        'previous': (0, float('inf'))
    }
    for col, (min_val, max_val) in value_range_checks.items():
        if col in df.columns:
            out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
            if not out_of_range.empty:
                out_of_range_report[col] = out_of_range.shape[0]
    
    logger.info("Checking consistency between related columns...")
    if 'loan_yes' in df.columns and 'loan_no' in df.columns:
        inconsistent_loan = df[(df['loan_yes'] == 1) & (df['loan_no'] == 1)]
        if not inconsistent_loan.empty:
            inconsistent_loan_report = inconsistent_loan.shape[0]

    logger.info("Summary of anomalies found:")
    
    if missing_values_report:
        logger.warning(f"Missing values by column: {missing_values_report}")
    else:
        logger.info("No missing values found.")
    
    if unexpected_columns_report:
        logger.warning(f"Unexpected dummy variables found: {unexpected_columns_report}")
    else:
        logger.info("No unexpected dummy variables found.")
    
    if outliers_report:
        logger.warning(f"Outliers count by column: {outliers_report}")
    else:
        logger.info("No outliers found.")
    
    if out_of_range_report:
        logger.warning(f"Out of range values by column: {out_of_range_report}")
    else:
        logger.info("No out of range values found.")
    
    if inconsistent_loan_report > 0:
        logger.warning(f"Inconsistent loan data found in {inconsistent_loan_report} rows.")
    else:
        logger.info("No inconsistent loan data found.")

if __name__ == "__main__":
    app()
