from config import PROJ_ROOT, MODELS_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR, Path
import typer
from loguru import logger
import pandas as pd
import xgboost as xgb


app = typer.Typer()

@app.command()
def predict(
    features_path: Path = PROCESSED_DATA_DIR / "X_test.pkl",
    model_path: Path = MODELS_DIR / "XGB_Model.json",
    predictions_path: Path = EXTERNAL_DATA_DIR / "predictions.json"
):
    logger.info("Loading test data and model...")
    X_test = pd.read_pickle(features_path)
    dtest = xgb.DMatrix(X_test)

    XGB_Model = xgb.Booster()
    XGB_Model.load_model(model_path)

    logger.info("Making predictions...")
    predictions = XGB_Model.predict(dtest)

    predictions_df = pd.DataFrame({
        'id': X_test.index,
        'deposit_predict': predictions[:, 1],
    })
    predictions_df.to_json(predictions_path, orient='records')
    
    logger.success("Predictions made and saved.")

if __name__ == "__main__":
    app()