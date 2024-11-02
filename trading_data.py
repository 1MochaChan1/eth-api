import pandas as pd
import pytz
import yfinance as yf

class Trading:
    
    @staticmethod
    def to_utc_ny(dt):
        """Convert a datetime object to New York time, handling both naive and timezone-aware datetime objects."""
        utc_zone = pytz.utc
        ny_zone = pytz.timezone('America/New_York')

        if dt.tzinfo is None:
            dt = utc_zone.localize(dt)  
        else:
            dt = dt.astimezone(utc_zone)  

        return dt.astimezone(ny_zone)  

    @staticmethod
    def get_current_day():
        """Fetch the current day's OHLC data for MNQ futures and return specific metrics."""
        symb = "MNQ=F"  

        # Get symbol OHLC data
        data = yf.download(symb, period='1d', interval='1m')
        data = data.reset_index()
        df = pd.DataFrame(data)
        
        # Convert datetime to New York timezone
        df['Datetime'] = df['Datetime'].apply(lambda x: Trading.to_utc_ny(x))

        # Determine bullish or bearish
        o = df.iloc[0]['Open']
        c = df.iloc[-1]['Close']
        bullish = float(o) < float(c)

        # Prepare the response dictionary
        res = {
            'Date': df.iloc[0].Datetime.strftime('%Y-%m-%d'),
            'OHLC (HOD)': None,
            'OHLC (LOD)': None,
            'OLHC (HOD)': None,
            'OLHC (LOD)': None,
        }

        # Get Highest and Lowest
        max_idx = df['High'].idxmax()
        min_idx = df['Low'].idxmin()

        if bullish:
            res['OLHC (HOD)'] = df.loc[max_idx, 'Datetime'].strftime('%H:%M:%S')
            res['OLHC (LOD)'] = df.loc[min_idx, 'Datetime'].strftime('%H:%M:%S')
        else:
            res['OHLC (HOD)'] = df.loc[max_idx, 'Datetime'].strftime('%H:%M:%S')
            res['OHLC (LOD)'] = df.loc[min_idx, 'Datetime'].strftime('%H:%M:%S')

        return res

    @staticmethod
    def get_rth(start_date='09:30:00', end_date='16:30:00'):
        """Fetch regular trading hours (RTH) data and return OHLC metrics."""
        symb = "MNQ=F"
        data = yf.download(symb, period='1d', interval='1m')
        data = data.reset_index()
        temp = pd.DataFrame(data)
        
        # Convert datetime to New York timezone
        temp['Datetime'] = temp['Datetime'].apply(lambda x: Trading.to_utc_ny(x))

        # Define start and end times
        start_time = pd.to_datetime(start_date).time()
        end_time = pd.to_datetime(end_date).time()

        # Filter the data between the given times
        df = temp[temp['Datetime'].dt.time.between(start_time, end_time)]
        
        # Determine bullish or bearish
        o = df.iloc[0]['Open']
        c = df.iloc[-1]['Close']
        bullish = float(o) < float(c)

        # Prepare the response dictionary
        res = {
            'Date': df.iloc[0].Datetime.strftime('%Y-%m-%d'),
            'OHLC (HOD)': None,
            'OHLC (LOD)': None,
            'OLHC (HOD)': None,
            'OLHC (LOD)': None,
        }

        # Get Highest and Lowest within RTH
        max_idx = df['High'].idxmax()
        min_idx = df['Low'].idxmin()

        if bullish:
            res['OLHC (HOD)'] = df.loc[max_idx, 'Datetime'].strftime('%H:%M:%S')
            res['OLHC (LOD)'] = df.loc[min_idx, 'Datetime'].strftime('%H:%M:%S')
        else:
            res['OHLC (HOD)'] = df.loc[max_idx, 'Datetime'].strftime('%H:%M:%S')
            res['OHLC (LOD)'] = df.loc[min_idx, 'Datetime'].strftime('%H:%M:%S')

        return res
