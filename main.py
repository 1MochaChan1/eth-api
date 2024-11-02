from fastapi import FastAPI
from mangum import Mangum
from trading_data import Trading


app = FastAPI()
handler = Mangum(app=app)

@app.get("/")
def get_root():
    return {"msg": "Hello World!"}

@app.get("/curr_day/{code}")
def read_item(code:str):
    if(code=="12345"):
        res = Trading.get_current_day()
        return res
    else:
        return {'err': 'Something went wrong'}

@app.get("/rth_day/{code}")
def read_item(code:str):
    if(code=="12345"):
        res = Trading.get_rth()
        return res
    else:
        return {'err': 'Something went wrong'}

@app.get("/rth_day_4/{code}")
def read_item(code:str):
    if(code=="12345"):
        res = Trading.get_rth("10:00:00", "14:00:00")
        return res
    else:
        return {'err': 'Something went wrong'}