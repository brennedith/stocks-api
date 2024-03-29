import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

from .base_source import BaseSource

class WallStreeSurvivorSource(BaseSource):


  _fqdn = 'https://app.wallstreetsurvivor.com'
  _default_headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': _fqdn,
  }
  _cookie_name = '.FASTRAKMVC'
  _header_keys = [
    'actions',
    'transaction_type',
    'symbol',
    'quantity',
    'type',
    'price_status',
    'fee',
    'date_time',
  ]
  identifier = 'wallstreetsurvivor'

  def authenticate(self, username, password):
    url = f'{self._fqdn}/login'
    headers = self._default_headers
    data = f'UserName={username}&Password={password}'

    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    auth_cookie = response.cookies.get(self._cookie_name)

    return auth_cookie

  def fetch(self, auth, start_date, end_date):
    base_url = f'{self._fqdn}/account/gettransactions?'
    querys = {
      'transactionType': 1,
      'startDate': start_date,
      'endDate': end_date,
      'pageIndex': 0,
      'pageSize': 12,
      'sortField': 'CreateDate',
      'sortDirection': 'DESC',
    }
    url = base_url + urlencode(querys)
    headers = {
      **self._default_headers,
      'Cookie': f'{self._cookie_name}={auth}'
    }
    response = requests.get(url, headers=headers)
    html = response.json().get('Html')
    return html

  def parse(self, html):
    soup = BeautifulSoup(html, 'html.parser')
    # create a 2d array with table content
    table_rows = soup.find_all('tr')
    transactions = []

    for row in table_rows:
      row_cells = list(row.find_all('td'))
      transaction = {}

      for index, cell in enumerate(row_cells):
        table_header = self._header_keys[index]

        if(table_header != None):
          transaction[table_header] = self._cleanText(cell.text)
      
      transactions.append(transaction)
    
    return transactions
