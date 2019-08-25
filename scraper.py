import requests, time, re, pickle
from bs4 import BeautifulSoup

class SCRAPER():
    def __init__(self):
        self.s = requests.session()
        self.s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'})
        self.endpoints = ['/monetarypolicy/fomccalendars.htm']
        self.links = []

    def get_links(self, endpoint):
        try:
            resp = self.s.get('https://www.federalreserve.gov{}'.format(endpoint), timeout=5)
        except Exception as e:
            print('Error: {}'.format(str(e)))
            exit()
        if resp.status_code != 200:
            print('Status Code: {}\n Reason: {}'.format(resp.status_code, resp.raise_for_status()))
            exit()
        soup = BeautifulSoup(resp.text, 'html.parser')
        try:
            soup = soup.find_all('a', href=re.compile('^/newsevents/pressreleases/monetary\d{8}a.htm'))
        except:
            soup = soup.findAll('a', text='Statement')
        if len(soup) > 0:
            self.links.extend([statement['href'] for statement in soup])

    def get_endpoints(self):
        try:
            resp = self.s.get('https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm', timeout=5)
        except Exception as e:
            print('Error: {}'.format(str(e)))
            exit()
        if resp.status_code != 200:
            print('Status Code: {}\n Reason: {}'.format(resp.status_code, resp.raise_for_status()))
            exit()

        soup = BeautifulSoup(resp.text, 'html.parser')
        soup = soup.find('div', {'class':'col-xs-12 col-sm-8 col-md-9'})
        self.endpoints.extend([year['href'] for year in soup.findAll('a')])

    def run(self):
        self.get_endpoints()
        for endpoint in self.endpoints:
            time.sleep(10)
            self.get_links(endpoint)
            print('Grabbed {} Links So Far'.format(len(self.links)))
            
if __name__ == '__main__':
    SCRAPER().run()
