import yfinance as yf  
import pandas as pd   
import pytz
from datetime import datetime, timedelta

def to_utc_ny(datetime):
    """Convert a datetime object to New York time, handling both naive and timezone-aware datetime objects."""
    utc_zone = pytz.utc
    ny_zone = pytz.timezone('America/New_York')

    if datetime.tzinfo is None:
        datetime = utc_zone.localize(datetime)  
    else:
        datetime = datetime.astimezone(utc_zone)  

    return datetime.astimezone(ny_zone)  



def get_current_day(symb:str="MNQ=F"):
    """Fetch the current day's OHLC data for MNQ futures and return specific metrics."""
    # Get Trading Day starting from yesterday's 18:00
    data = _get_data(symb)

    df = pd.DataFrame(data)
    df['Datetime'] = df['Datetime'].apply(lambda x: to_utc_ny(x))
    
    return _find_highest(df)


def get_rth(str_strt:str='09:30:00', str_end:str='16:30:00', symb:str="MNQ=F"):
    
    # GET DATA FROM API
    data = _get_data(symb)
    temp = pd.DataFrame(data)
    
    # GET DATA SLICE FROM TIME A to B
    temp['Datetime'] = temp['Datetime'].apply(lambda x: to_utc_ny(x))
    
    pt_strt = datetime.strptime(str_strt, "%H:%M:%S")
    pt_end = datetime.strptime(str_end, "%H:%M:%S")

    temp_date = datetime.now(tz=pytz.timezone('America/New_York'))
    start_time = temp_date.replace(hour=pt_strt.hour, minute=pt_strt.min, second=0)
    end_time = temp_date.replace(hour=pt_end.hour, minute=pt_end.min, second=0)
    
    df = temp[temp['Datetime'].dt.time.between(start_time, end_time)]
    
    # INSTANTIATE RESPONSE and FIND BULLISH BEARISH
    return _find_highest(df)



### HELPERS ###

def _find_highest(df:pd.DataFrame):
    o = df.iloc[0]['Open']
    c = df.iloc[-1]['Close']
    bullish = True
    if (float(o.item()) > float(c.item())): bullish = False

    res = {
        'Date':df.iloc[0].Datetime.item().strftime('%Y-%m-%d'),
        'OHLC (HOD)':None,
        'OHLC (LOD)':None,
        'OLHC (HOD)':None,
        'OLHC (LOD)':None,
    }


    # GET HIGHEST AND LOWEST IN THE SLICE
    max = df['High'].idxmax()
    min = df['Low'].idxmin()

    if(bullish):
        res['OLHC (HOD)'] = df.loc[max,'Datetime'].item().strftime('%H:%M:%S')
        res['OLHC (LOD)'] = df.loc[min,'Datetime'].item().strftime('%H:%M:%S')
    else:
        res['OHLC (HOD)'] = df.loc[max,'Datetime'].item().strftime('%H:%M:%S')
        res['OHLC (LOD)'] = df.loc[min,'Datetime'].item().strftime('%H:%M:%S')
    return res

def _get_data(symb):
    end_time = datetime.now(tz=pytz.timezone('America/New_York'))
    start_time = end_time - timedelta(days=1)  # Go back one day
    start_time = start_time.replace(hour=18, minute=0, second=0, microsecond=0)

    # Get symbol OHLC data
    data = yf.download(symb, start=start_time, end=end_time, interval='1m')
    data = data.reset_index()
    return data