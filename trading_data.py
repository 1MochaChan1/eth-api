import yfinance as yf  
import pandas as pd   
import pytz

def to_utc_ny(datetime):
    """Convert a datetime object to New York time, handling both naive and timezone-aware datetime objects."""
    utc_zone = pytz.utc
    ny_zone = pytz.timezone('America/New_York')

    if datetime.tzinfo is None:
        datetime = utc_zone.localize(datetime)  
    else:
        datetime = datetime.astimezone(utc_zone)  

    return datetime.astimezone(ny_zone)  

def get_current_day():
    """Fetch the current day's OHLC data for MNQ futures and return specific metrics."""
    symb = "MNQ=F"  


    # Get symbol OHLC data
    data = yf.download(symb, period='1d', interval='1m')
    data = data.reset_index()
    data



    df = pd.DataFrame(data)
    df['Datetime'] = df['Datetime'].apply(lambda x: to_utc_ny(x))
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


    # Get Highest Lowest
    max = df['High'].idxmax()
    min = df['Low'].idxmin()

    if(bullish):
        res['OLHC (HOD)'] = df.loc[max,'Datetime'].item().strftime('%H:%M:%S')
        res['OLHC (LOD)'] = df.loc[min,'Datetime'].item().strftime('%H:%M:%S')
    else:
        res['OHLC (HOD)'] = df.loc[max,'Datetime'].item().strftime('%H:%M:%S')
        res['OHLC (LOD)'] = df.loc[min,'Datetime'].item().strftime('%H:%M:%S')

    return res  


def get_rth(start_date:str='09:30:00', end_date:str='16:30:00'):
    # GET DATA FROM API
    symb = "MNQ=F"
    data = yf.download(symb, period='1d', interval='1m')
    data = data.reset_index()
    temp = pd.DataFrame(data)
    
    # GET DATA SLICE FROM TIME A to B
    temp['Datetime'] = temp['Datetime'].apply(lambda x: to_utc_ny(x))
    start_time = pd.to_datetime(start_date).time()
    end_time = pd.to_datetime(end_date).time()
    df = temp[temp['Datetime'].dt.time.between(start_time, end_time)]
    
    # INSTANTIATE RESPONSE and FIND BULLISH BEARISH
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