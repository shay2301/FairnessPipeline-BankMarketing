import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pandas as pd
from sklearn.model_selection import train_test_split
from loguru import logger
import typer
from config import PROCESSED_DATA_DIR
from data.raw.load_data import load_data

app = typer.Typer()

@app.command()
def main(
    output_dir: Path = PROCESSED_DATA_DIR
):
    logger.info(f"Output directory: {output_dir}")
    logger.info("Starting data processing...")
    
    df = load_data(repo_id=222)
    
    df = pd.get_dummies(df, columns=[
        'job', 'marital', 'education', 'default', 
        'housing', 'loan', 'contact', 'month', 'poutcome'
    ])
    
    df.y.replace(('yes', 'no'), (1, 0), inplace=True)
    
    data_y = pd.DataFrame(df['y'])
    data_X = df.drop(['y'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, test_size=0.3, random_state=2, stratify=data_y)
    
    logger.info(f"Features: {list(data_X.columns)}")

    df.to_pickle(output_dir / "dataset_processed.pkl")
    X_train.to_pickle(output_dir / "X_train.pkl")
    X_test.to_pickle(output_dir / "X_test.pkl")
    y_train.to_pickle(output_dir / "y_train.pkl")
    y_test.to_pickle(output_dir / "y_test.pkl")
    
    logger.success("Data processing and saving complete.")

if __name__ == "__main__":
    app()
