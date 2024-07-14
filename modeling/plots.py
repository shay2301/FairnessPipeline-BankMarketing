
from config import MODELS_DIR, FIGURES_DIR, Path
import typer
from loguru import logger
from matplotlib import pyplot as plt
import xgboost as xgb
from xgboost import plot_importance

app = typer.Typer()


@app.command()
def main(
    model_path: Path = MODELS_DIR / "XGB_Model.json",
    output_importance: Path = FIGURES_DIR / "feature_importance.png",
    output_tree: Path = FIGURES_DIR / "tree.txt"
):
    logger.info("Loading model...")
    model = xgb.Booster()
    model.load_model(model_path)

    logger.info("Generating feature importance plot...")
    plt.figure(figsize=(10, 8))
    plot_importance(model)
    plt.title("Feature Importance")
    plt.savefig(output_importance)
    plt.close()

    logger.info("Dumping tree as text...")
    with open(output_tree, 'w') as file:
        for tree in model.get_dump():
            file.write(tree + '\n')
    logger.success("Plots generated and saved to {}".format(FIGURES_DIR))

if __name__ == "__main__":
    app()
