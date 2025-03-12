from utils import *
from config import GFD_USERNAME, GFD_PASSWORD

if __name__ == '__main__':
    main_dir = '../data'
    ## GET SP500 Constituents
    df = pd.read_csv(f'{main_dir}/current_sp500_membership.csv')

    df['Symbol'] = df['Symbol'].astype(str)

    tickers = list(set(df['Symbol']))
    tickers = [ticker for ticker in tickers if str(ticker) != 'nan']

    token = gfd_auth(GFD_USERNAME, GFD_PASSWORD)['token'].strip('"')
    sp500_directory = f'{main_dir}/sp500'
    os.makedirs(sp500_directory, exist_ok=True)

    missed = []
    for ticker in tickers:
        if not os.path.exists(f'{sp500_directory}/{ticker}.csv'):
            save_series_to_csv(token, ticker, "Daily", f'{sp500_directory}/{ticker}')
            if not os.path.exists(f'{sp500_directory}/{ticker}.csv'):
                missed.append(ticker)
        else:
            print(f'{ticker} already exists')

    #Get the risk-free rate
    ticker = 'ITUSA1D' # USA 1-month Constant Maturity Treasury Bill Yield
    save_series_to_csv(token, ticker, "Daily", f'{main_dir}/{ticker}')

    #Get the market index
    ticker = '_SPXD'
    save_series_to_csv(token, ticker, "Daily", f'{main_dir}/{ticker}')

    print(f'Missed: {missed}')