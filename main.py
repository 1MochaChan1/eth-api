from fastapi import FastAPI
from mangum import Mangum
from trading_data import get_current_day, get_rth


app = FastAPI()
handler = Mangum(app=app)

@app.get("/")
def get_root():
    return {"msg": "Hello World!"}

@app.get("/curr_day/{symbol}")
def read_item(symbol:str):
    res = get_current_day(symb=symbol)
    return res

@app.get("/rth_day/{symbol}")
def read_item(symbol:str):
    res = get_rth(symb=symbol)
    return res


@app.get("/rth_day_4/{symbol}")
def read_item(symbol:str):
    res = get_rth(str_start_time="10:00:00", str_end_time="14:00:00", symb=symbol)
    return res
