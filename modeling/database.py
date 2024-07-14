from config import PROJ_ROOT, EXTERNAL_DATA_DIR, Path
from loguru import logger
import pandas as pd
import duckdb
import typer

app = typer.Typer()

@app.command()
def main(
    json_path: Path = EXTERNAL_DATA_DIR / "predictions.json", 
    db_path: Path = EXTERNAL_DATA_DIR / "banking_predictions.db"
):
    data = pd.read_json(json_path)
    
    data.columns = ['id', 'deposit_predict']
    
    logger.info("DataFrame loaded from JSON:")
    
    con = duckdb.connect(str(db_path))

    con.execute("""
        CREATE TABLE IF NOT EXISTS banking_predictions (
            id BIGINT,
            deposit_predict DOUBLE
        )
    """)
    
    con.execute("CREATE TEMPORARY TABLE temp_predictions AS SELECT * FROM banking_predictions")

    con.execute("""
        INSERT INTO banking_predictions (id, deposit_predict)
        SELECT id, deposit_predict 
        FROM temp_predictions 
        WHERE id NOT IN (SELECT id FROM banking_predictions)
    """)

    result = con.execute("SELECT * FROM banking_predictions ORDER BY id DESC").fetchdf()
    logger.info(result.head())

    row_count = con.execute("SELECT COUNT(*) FROM banking_predictions").fetchone()[0]
    logger.info(f"Total number of rows: {row_count}")

    con.close()
    logger.success("Banking Predictions saved to DuckDB successfully.")

if __name__ == "__main__":
    main()
