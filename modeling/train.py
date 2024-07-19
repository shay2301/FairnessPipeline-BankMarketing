from config import PROJ_ROOT, PROCESSED_DATA_DIR, MODELS_DIR, Path
import typer
from loguru import logger
import pandas as pd
import xgboost as xgb
from fairlearn.reductions import ExponentiatedGradient, DemographicParity
import pickle

app = typer.Typer()

@app.command()
def train_model(
    features_path: Path = PROCESSED_DATA_DIR / "X_train.pkl",
    labels_path: Path = PROCESSED_DATA_DIR / "y_train.pkl",
    model_path: Path = MODELS_DIR / "XGB_Model.json"
):

    MITIGATE = True
           
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
    
    
    if MITIGATE:
        print("Training to mitigate fairnsee")
        mitigator = ExponentiatedGradient(XGB_Model,
                                  constraints=DemographicParity(),
                                  eps=0.07,
                                  )
        mitigator.fit(X_train, y_train, sensitive_features=X_train['age'])
        with open(model_path, 'wb') as f:
            pickle.dump(mitigator, f)
    else:
        XGB_Model.save_model(model_path)
    
    logger.success("Model training complete and model saved.")

if __name__ == "__main__":
    app()
