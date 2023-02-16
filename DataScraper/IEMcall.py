import urllib.request, urllib.error, urllib.parse
import datetime
import time as t
import pandas as pd


savePath = '/home/snowdaere/PythonProjects/firecast/DataScraper/StationData/'


def call(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('UTF-8')


def callALL(day:datetime.datetime):

    serviceALL = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?data=tmpf&data=dwpf&data=drct&data=sknt&data=mslp&data=p01i&data=gust&data=wxcodes&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=null&trace=0.0001&direct=no&report_type=3&report_type=4'

    date1 = day
    date2 = date1 + datetime.timedelta(hours=24)
    
    # make the url date extension
    extension = f'&year1={date1.year}&month1={date1.month}&day1={date1.day}&year2={date2.year}&month2={date2.month}&day2={date2.day}'
    url = serviceALL + extension

    content = call(url)

    f = open(f'{savePath}{day.year:4}{day.month:02}{day.day:02}.csv', 'w')
    f.write(content)
    f.close


def callSTATION(station, date1, date2, network=''):

    serviceSTATION = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?data=tmpf&data=dwpf&data=drct&data=sknt&data=mslp&data=p01i&data=gust&data=wxcodes&tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=null&trace=0.0001&direct=no&report_type=3&report_type=4'

    # make the url station extension
    stationextension = f'&station={station}'
    url = serviceSTATION + stationextension

    # make the url date extension
    extension = f'&year1={date1.year}&month1={date1.month}&day1={date1.day}&year2={date2.year}&month2={date2.month}&day2={date2.day}'
    url = url + extension

    content = call(url)

    if network != '':
        network = network + '/'


    f = open(f'{savePath}{network}{station}.csv', 'w')
    f.write(content)
    f.close


if __name__ == '__main__':
    # load dataframe of the networks
    networks = pd.read_csv('networks.csv')

    # pick out the ones within the oregon ASOS or COOP network
    # also pick out the ones beginning observations before 1992
    ### NOTE here put the list of networks you wish to search
    networklist = ['CA_ASOS', 'CA_COOP', 'CA_RWIP']
    network = networks.query('iem_network == @networklist and begints <= "1992-01-01"')
    del networks
    length = len(network.index)
    times = [np.nan] * length

    # for each in that list, query and save
    dates = datetime.datetime(1992, 1, 1), datetime.datetime(2015, 12, 31)
    for i, row in network.iterrows():
        print(f'Calling {row.stid}, finished in ', end='')
        time0 = t.time()
        ### NOTE make sure to change the name of the network folder
        callSTATION(row.stid, *dates, network='CA')
        time1 = t.time()
        print(f'{time1 - time0:3} seconds.')
        times[i] = time1 - time0
        # recalculate mean retrieval time
        #
        print(f'Estimated completion in {np.nanmean(times)/3600} hours')
        print()

    print(f'Completed in {np.nansum(times)/3600} hours')
    
