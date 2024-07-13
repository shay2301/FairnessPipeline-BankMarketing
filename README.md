# FairnessPipeline-BankMarketing

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

End to end mlops pipeline flow for a banking marketing campaign.

# Meet the Team:
Shay Levi

Nadav Ben Itzhak

Niv Leibovitch 

Zack Shipman

## Project Organization

```
├── LICENSE           
├── Makefile           <- commands to run data 'make run_all'
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- MLops Superteam docs
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for fairnesspipeline_bankmarketing
│                         and configuration for tools like black
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── fairnesspipeline_bankmarketing                <- Source code for use in this project.
    │
    ├── __init__.py    
    │
    ├── data           <- Scripts to download or generate data
    │   └── load_data.py
    │
    ├── features       <- Scripts to turn raw data into features for modeling
    │   └── features.py
    │
    ├── modeling         <- Scripts to train models and then use trained models to make
    │   │                 predictions
    │   ├── predict.py
    │   └── train.py
    |   |__ database.py -- this will dump predictions in the duckdb database
    │
    └── visualization  <- Scripts to create exploratory and results oriented visualizations
        └── visualize.py
```

--------

