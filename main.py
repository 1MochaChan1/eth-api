from fastapi import FastAPI
from mangum import Mangum
from trading_data import get_current_day


app = FastAPI()
handler = Mangum(app=app)

@app.get("/")
def get_root():
    return {"msg": "Hello World!"}

@app.get("/curr_day/{code}")
def read_item(code:str):
    if(code=="12345"):
        res = get_current_day()
        return res
    else:
        return {'err': 'Something went wrong'}