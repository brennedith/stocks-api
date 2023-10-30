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

        mock_html = """
<table>
  <thead>
    <tr>
      <th>&nbsp;</th>
      <th>Symbol</th>
      <th>Quantity</th>
      <th>Order</th>
      <th>Order Price</th>
      <th>Price Filled</th>
      <th>Order Date</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody id="order-history-container">
    <tr>
      <td class="actions"> <a data-status="137454734" class="cancelorder" title="Cancel"><i class="fa fa-close"
            aria-hidden="true"></i></a> <a
          href="/trading/Equities?symbol=NKE&amp;quantity=200&amp;exchange=US&amp;edit=True&amp;oldorderid=137454734"
          title="Edit"><i class="fa fa-edit" aria-hidden="true"></i></a> <a data-open="add-view-notes"
          data-order-conf="6bcad04e-6917-493e-b2c5-c2e05f15dce0" class="openModal" title="Trade Notes"><i
            class="fa fa-sticky-note-o" aria-hidden="true"></i></a> </td>
      <td><a href="#">NKE</a></td>
      <td>200</td>
      <td>Market - Buy</td>
      <td>MKT</td>
      <td></td>
      <td>10/29/2023</td>
      <td><span data-tooltip aria-haspopup="true" class="has-tip top" data-disable-hover="false"
          tabindex="2">Open</span></td>
    </tr>
  </tbody>
</table>
<script
  type="text/javascript">        $(function () { $(".openModal").on('click', function () {                //var orderId = this.getAttribute('data-order-id');                var orderConf = this.getAttribute('data-order-conf');                //setOrderId(orderId);                setOrderConfirmation(orderConf);                var data = {                    pageIndex: currentPageIndex,                    pageSize: pageSize,                    orderConf: orderConf                };                $.get('/account/gettradingnotesbyorder', data, function (result) {                    $('#add-view-notes').foundation('open');                    if (result.Count > 0) {                        //$("#tblTradeNotes").show();                        $('#trade-notes').html(result.Html);                    }                    else {                        //$("#tblTradeNotes").hide();                        $('#trade-notes').empty();                        $('#trade-notes').append('<tr id="msg"><td colspan="2" class="text-center">You do not have any notes for this trade. Click "Add Note" to write one.</td></tr>');                    }                });            });        });</script>
"""

        result = source.parse(mock_html)
        expected = [
          {
            "actions": "",
            "symbol": "NKE",
            "quantity": "200",
            "transaction_type": "Market - Buy",
            "type": "",
            "date_time": "10/29/2023",
            "fee": "Open"
          },
        ]
        self.assertEqual(result, expected)
