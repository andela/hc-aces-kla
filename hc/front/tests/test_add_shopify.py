from hc.test import BaseTestCase
from django.core.urlresolvers import reverse
from hc.api.models import Check
import os


class AddShopifyAlertTestCase(BaseTestCase):
    """This class contains tests to handle adding checks"""

    def test_it_redirects_add_shopify(self):
        """test it renders add_shopify """

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get("/integrations/add_shopify/")

        assert response.status_code == 200

    def test_it_accepts_connection_to_shopify(self):
        """test it accepts connection to shopify """
        API_KEY = os.environ.get('API_KEY')

        PASSWORD = os.environ.get('PASSWORD')

        EVENT = "order/create"

        NAME = "Create Order"

        SHOP_NAME = "Duuka1"

        form = {"api_key": API_KEY,
                "password": PASSWORD,
                "event": EVENT, "name": NAME,
                "shop_name": SHOP_NAME
                }

        url = reverse("hc-create-shopify-alerts")

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)

        self.assertRedirects(response, "/checks/")

        assert response.status_code == 302

    def test_it_doesnot_accept_wrong_details(self):
        API_KEY = "84895nfjdufer0n5jnru553jdmfi9"

        PASSWORD = "d602f072d117438yjfjfjfu9582ce3"

        EVENT = "order/create"

        NAME = "Create Order"

        SHOP_NAME = "Duuka1"

        form = {"api_key": API_KEY,
                "password": PASSWORD,
                "event": EVENT,
                "name": NAME,
                "shop_name": SHOP_NAME
                }

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(
            "/checks/create_shopify_alert/", form)

        assert response.status_code == 403

    def test_it_creates_alert_for_check_shopify_and_redirects(self):
        API_KEY = os.environ.get('API_KEY')

        PASSWORD = os.environ.get('PASSWORD')

        EVENT = "order/create"

        NAME = "Create Order"

        SHOP_NAME = "Duuka1"

        form = {"api_key": API_KEY,
                "password": PASSWORD,
                "event": EVENT,
                "name": NAME,
                "shop_name": SHOP_NAME
                }

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/checks/create_shopify_alert/", form)

        self.assertRedirects(response, "/checks/")
        self.assertEqual(Check.objects.count(), 1)

        self.client.login(username="alice@example.org", password="password")

        response = self.client.get("/checks/")
        self.assertContains(response, "Create Order", status_code=200)
