import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import pandas as pd
from sklearn.model_selection import train_test_split
import typer
from loguru import logger

from config import PROCESSED_DATA_DIR

app = typer.Typer()

@app.command()
def main(
    input_path: Path = PROCESSED_DATA_DIR / "dataset_processed.pkl",
    output_dir: Path = PROCESSED_DATA_DIR
):
    logger.info("Loading preprocessed data...")
    df = pd.read_pickle(input_path)

    logger.info("Manipulate the data to train test split...")
    data_y = pd.DataFrame(df['y'])
    data_X = df.drop('y', axis=1)
    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, test_size=0.3, random_state=2, stratify=data_y)

    logger.info(f"Saving training and testing data...")
    X_train.to_pickle(output_dir / "X_train.pkl")
    X_test.to_pickle(output_dir / "X_test.pkl")
    y_train.to_pickle(output_dir / "y_train.pkl")
    y_test.to_pickle(output_dir / "y_test.pkl")

    logger.success("Features generation and data split complete.")

if __name__ == "__main__":
    app()
