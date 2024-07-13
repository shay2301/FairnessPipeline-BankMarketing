import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import typer
from loguru import logger
import pandas as pd
import xgboost as xgb

from config import MODELS_DIR, PROCESSED_DATA_DIR

app = typer.Typer()

@app.command()
def train_model(
    features_path: Path = PROCESSED_DATA_DIR / "X_train.pkl",
    labels_path: Path = PROCESSED_DATA_DIR / "y_train.pkl",
    model_path: Path = MODELS_DIR / "XGB_Model.json"
):
    logger.info("Loading training data...")
    X_train = pd.read_pickle(features_path)
    y_train = pd.read_pickle(labels_path)

    dtrain = xgb.DMatrix(X_train, label=y_train)
    params = {
        'objective': 'multi:softprob',
        'max_dept': 4,
        'silent': 1,
        'eta': 0.3,
        'gamma': 0,
        'num_class': 2
    }
    num_rounds = 20

    logger.info("Training the model...")
    XGB_Model = xgb.train(params, dtrain, num_rounds)
    XGB_Model.save_model(model_path)
    
    logger.success("Model training complete and model saved.")

if __name__ == "__main__":
    app()
