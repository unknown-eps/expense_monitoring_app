from fastapi import FastAPI,Request
from datetime import datetime
import pandas as pd
import json 
from fastapi.responses import JSONResponse
app = FastAPI()
data_df=pd.read_excel('data.xlsx')
@app.get("/")
async def root():
    json_str = data_df.to_json(orient="records")
    records = json.loads(json_str)
    return JSONResponse(content=records)
@app.post("/")
async def post_data(request : Request):
    data = await request.json()
    print(data)
    data_df.loc[len(data_df)]={'ID':len(data_df),'TYPE':data['type'],'VALUE':data['value'],'DATE': datetime.now()}
    data_df.to_excel('data.xlsx',index=False)
    return {"message": "Data received successfully!"}
