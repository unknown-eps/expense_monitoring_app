from fastapi import FastAPI
import pandas as pd
import json
from fastapi.responses import JSONResponse
app = FastAPI()
data_df=pd.read_excel('data.xlsx')
@app.get("/")
def root():
    json_str = data_df.to_json(orient="records")
    records = json.loads(json_str)
    return JSONResponse(content=records)
