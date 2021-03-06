# -*- coding: utf-8 -*-

import pandas as pd
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from etfs.utils.helpers import standard_date_format, todays_date


def read_treasury_csv(path=None, startdate='2000-01-01', enddate=None):
    """
    Read locally stored csv with data from US Deparment of the Treasury.

    """
    if enddate == None:
        enddate = todays_date()

    # convert dates to pandas format
    startdate = standard_date_format(startdate)
    enddate = standard_date_format(enddate)

    _df = pd.read_csv(path, index_col='Date', parse_dates=True)

    return _df.loc[(_df.index >= startdate) & (_df.index <= enddate)]


def retrieve_treasury_yield_curve_rates(url='https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldAll',
                                        startdate='20000101', 
                                        enddate=None):
    """
    Download yield curve rates data from  US Deparment of the Treasury.

    """

    if enddate == None:
        enddate = todays_date()

    # convert dates to pandas format
    startdate = standard_date_format(startdate)
    enddate = standard_date_format(enddate)

    _headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
    }

    # use request to retrieve data
    req = urllib.request.Request(url, headers=_headers)
    f = urllib.request.urlopen(req)
    html_data = f.read().decode('utf-8')
    
    soup = BeautifulSoup(html_data,'lxml')
    table = soup.find('table', {'class': 't-chart'})

    _df = pd.read_html(str(table), header=0, index_col='Date', parse_dates=True)[0]

    return _df.loc[(_df.index >= startdate) & (_df.index <= enddate)]

