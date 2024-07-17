from config import PROJ_ROOT, PROCESSED_DATA_DIR, Path
import pandas as pd
from loguru import logger
import typer
from data.raw.load_data import load_data

app = typer.Typer()

@app.command()
def create_dataset(
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

    df.to_csv(output_dir / "dataset_processed.csv")

    logger.success("Data processing and saving complete.")

if __name__ == "__main__":
    app()
