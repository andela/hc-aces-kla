from hc.test import BaseTestCase
from mock import patch


class AddShopifyAlertTestCase(BaseTestCase):
    """This class contains tests to handle adding checks"""

    def setUp(self):
        super(AddShopifyAlertTestCase, self).setUp()
        self.api_key = "84895nfjdufer0n5jnru553jdmfi9"
        self.password = "d602f072d117438yjfjfjfu9582ce3"
        self.event = "order/create"
        self.name = "Create Order"
        self.shop_name = "Duuka1"

    def test_it_redirects_add_shopify(self):
        """test it renders add_shopify """

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/integrations/add_shopify/")

        assert response.status_code == 200

    @patch('hc.front.views.shopify')
    def test_it_accepts_connection_to_shopify(self, mock):
        form = {"api_key": self.api_key,
                "password": self.password,
                "event": self.event,
                "name": self.name,
                "shop_name": self.shop_name
                }
        url = "https://%s:%s@%s.myshopify.com/admin" % (
            self.api_key, self.password, self.shop_name)
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(
            "/checks/create_shopify_alert/", form)
        mock.ShopifyResource.set_site.assert_called_with(url)
        self.assertEqual(response.status_code, 302)

    @patch('hc.front.views.shopify.ShopifyResource')
    @patch('hc.front.views.shopify')
    def test_it_doesnot_accept_wrong_details(self, mock, mock_hook):
        form = {"api_key": self.api_key,
                "password": self.password,
                "event": self.event,
                "name": self.name,
                "shop_name": self.shop_name
                }
        mock_hook.set_site.side_effect = Exception
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(
            "/checks/create_shopify_alert/", form)
        self.assertEqual(response.status_code, 403)

    @patch('hc.front.views.shopify.Webhook')
    @patch('hc.front.views.shopify')
    def test_it_creates_alert_and_redirects(self, mock, mock_hook):
        form = {"api_key": self.api_key,
                "password": self.password,
                "event": self.event,
                "name": self.name,
                "shop_name": self.shop_name
                }
        mock_hook.find.return_value = []
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(
            "/checks/create_shopify_alert/", form)
        self.assertEqual(response.status_code, 302)

    @patch('hc.front.views.shopify.Webhook')
    @patch('hc.front.views.shopify')
    def test_doesnt_create_event_twice(self, mock, mock_hook):
        form = {"api_key": self.api_key,
                "password": self.password,
                "event": self.event,
                "name": self.name,
                "shop_name": self.shop_name
                }
        mock_hook.find.return_value = [4, 5]
        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(
            "/checks/create_shopify_alert/", form)
        self.assertEqual(response.status_code, 400)
