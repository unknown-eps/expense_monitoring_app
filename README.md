# basic_finance_tracking_app
## A simple streamlit + fastapi app to track financial spending history

### Setup:

```shell
# This command creates the environment
conda env create -n app_env python=3.9 matplotlib pandas openpyxl streamlit fastapi uvicorn
# Run the streamlit app
python -m streamlit run frontend.py default port 8501

# Run the backend in other terminal default port 8000
uvicorn backend:app --reload
```