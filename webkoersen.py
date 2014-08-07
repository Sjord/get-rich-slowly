from time import strptime, strftime
import urllib
from xml.dom import minidom

class KoersenSource:
    def get_prices(self, startdate, enddate, isincode):
        try:
            start = startdate.strftime("%Y-%m-%d")
        except AttributeError:
            start = startdate

        try:
            end = enddate.strftime("%Y-%m-%d")
        except AttributeError:
            end = enddate

        url = 'http://tools.morningstar.nl/api/rest.svc/timeseries_price/8qe8f2nger?id=%(isincode)s&currencyId=EUR&idtype=Isin&frequency=daily&startDate=%(start)s&endDate=%(end)s&outputType=XML' % {'isincode' : isincode, 'start': start, 'end' : end }
        handle = urllib.urlopen(url)
        dom = minidom.parse(handle)
        koersen = self.xmlToObj(dom)
        return koersen
        
    def xmlToObj(self, dom):
        koersen = []
        details = dom.getElementsByTagName('HistoryDetail')
        for detail in details:
            datestr = detail.getElementsByTagName('EndDate')[0].childNodes[0].nodeValue
            pricestr = detail.getElementsByTagName('Value')[0].childNodes[0].nodeValue
            datum = strptime(datestr, '%Y-%m-%d')
            price = float(pricestr)
            koersen.append({'date': datestr, 'price': price})
        return koersen


if __name__ == "__main__":
    start = strptime('2014-04-01', '%Y-%m-%d')
    end = strptime('2014-04-25', '%Y-%m-%d')
    k = KoersenSource()
    print k.getKoersen(start, end, 'LU0837977205')

