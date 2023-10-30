import unittest
from unittest.mock import patch
from django.test import TestCase

from api.logic.sources.wallstreetsurvivor_source import WallStreeSurvivorSource

class TestWallStreeSurvivorSource(TestCase):
      

    @patch('api.logic.sources.wallstreetsurvivor_source.requests.post')
    def test_authenticate_success(self, mock_post):
        source = WallStreeSurvivorSource()

        mock_response = unittest.mock.Mock()
        mock_cookie_value = 123456
        mock_response.cookies = {}
        mock_response.cookies[source._cookie_name] = mock_cookie_value
        mock_post.return_value = mock_response

        result = source.authenticate('John', 'Snow')

        mock_post.assert_called_once_with(
            source._fqdn + '/login',
            headers=source._default_headers,
            data='UserName=John&Password=Snow',
            allow_redirects=False
        )

        self.assertEqual(result, mock_cookie_value)

    @patch('api.logic.sources.wallstreetsurvivor_source.requests.get')
    def test_request_success(self, mock_get):
        source = WallStreeSurvivorSource()
        cookie_value = 123456
        start_date = '2024-11-1'
        end_date = '2024-12-5'

        mock_response = unittest.mock.Mock()
        mock_html = '<html></html>'
        mock_response.json.return_value = { 'Html': mock_html }
        mock_get.return_value = mock_response

        base_url = f'{source._fqdn}/account/getorderhistory?'
        querys = f'sortField=CreateDate&sortDirection=DESC&pageIndex=0&pageSize=12&startDate={start_date}&endDate={end_date}'
        headers = {
          **source._default_headers,
          'Cookie': f'{source._cookie_name}={cookie_value}'
        }

        result = source.fetch(cookie_value, start_date, end_date)

        mock_get.assert_called_once_with(
            base_url + querys,
            headers=headers,
        )

        self.assertEqual(result, mock_html)

    def test_request_success(self):
        source = WallStreeSurvivorSource()

        mock_html = "\r\n    <tr>\r\n        <td class=\"actions\">\n            \n            <a class=\"fa fa-exchange\" href=\"/trading/Equities?symbol=INTC&amp;exchange=US\"> </a>\n\t\t\t\t\t\t\t\t\t\n                <a data-order-id=\"dac2b008-da40-4339-bccf-a94bcfe6ba2b\" class=\"openModal\" title=\"Trade Notes\"><i class=\"fa fa-sticky-note-o\" aria-hidden=\"true\"></i></a>\r\n\t\t</td>\r\n        <td>Market - Buy</td>\r\n        <td><a href=\"#\">INTC</a></td>\r\n        <td>22</td>\r\n        <td>Equities</td>\r\n        <td>\r\n            $35.3700\r\n        </td>\r\n        <td>1.00</td>\r\n        <td>\r\n            10/30/2023 - 09:33\r\n        </td>\r\n    </tr>\r\n\r\n<script type=\"text/javascript\">\r\n    $(function () {\r\n        $(\".openModal\").on('click', function () {\r\n            var orderConf = this.getAttribute('data-order-id');\r\n            setOrderConfirmation(orderConf);\r\n            var data = {\r\n                pageIndex: currentPageIndex,\r\n                pageSize: pageSize,\r\n                orderConf: orderConf\r\n            };\r\n</script>"

        result = source.parse(mock_html)
        expected = [
          {
            "actions": "",
            "symbol": "INTC",
            "quantity": "22",
            "price_status": "$35.3700",
            "transaction_type": "Market - Buy",
            "type": "Equities",
            "date_time": "10/30/2023 - 09:33",
            "fee": "1.00"
          },
        ]
        self.assertEqual(result, expected)
