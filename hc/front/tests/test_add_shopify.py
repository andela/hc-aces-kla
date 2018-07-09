from hc.test import BaseTestCase
from shopify_trois import Credentials, Collection
from shopify_trois.models import Shop
from shopify_trois.engines.http import Json as Shopify
from django.core.urlresolvers import reverse
import shopify
import requests
from hc.api.models import Check

class AddShopifyAlertTestCase(BaseTestCase):
    """This class contains tests to handle adding checks"""


    def test_it_redirects_add_shopify(self):
        """test that when the correct authentication keys are given that it returns valid response """

        self.client.login(username="alice@example.org", password="password")
        response = self.client.get( "/integrations/add_shopify/")

        assert response.status_code == 200

    def test_it_accepts_connection_to_shopify(self):
        """test that when the correct authentication keys are given that it returns valid response """
        API_KEY = "2ea13bd64c9c06f5ff5501dd6872ecda"

        PASSWORD = "d602f072d114aceca3c21a2234582ce3"

        EVENT = "order/create"

        NAME = "Create Order"

        SHOP_NAME = "Duuka1"

        form = {"api_key": API_KEY,
                "password": PASSWORD, "event": EVENT, "name": NAME, "shop_name": SHOP_NAME}

        url = reverse("hc-create-shopify-alerts")

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)
        
        self.assertRedirects(response, "/checks/")

        assert response.status_code == 302

    def test_it_doesnot_accept_wrong_details(self):
        API_KEY = "2ea13bd64c9c06f5ff5501dd6872ecda"

        PASSWORD = "d602f072d117438yjfjfjfu9582ce3"

        EVENT = "order/create"

        NAME = "Create Order"

        SHOP_NAME = "Duuka1"

        form = {"api_key": API_KEY,
                "password": PASSWORD, "event": EVENT, "name": NAME, "shop_name": SHOP_NAME}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(
            "/checks/create_shopify_alert/", form)

        assert response.status_code == 403

    def test_it_creates_alert_for_check_shopify_and_redirects(self):
        API_KEY = "2ea13bd64c9c06f5ff5501dd6872ecda"

        PASSWORD = "d602f072d114aceca3c21a2234582ce3"

        EVENT = "order/create"

        NAME = "Create Order"

        SHOP_NAME = "Duuka1"

        form = {"api_key": API_KEY,
                "password": PASSWORD, "event": EVENT, "name": NAME, "shop_name": SHOP_NAME}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post("/checks/create_shopify_alert/", form)

        self.assertRedirects(response, "/checks/")
        self.assertEqual(Check.objects.count(), 1)

        self.client.login(username="alice@example.org", password="password")

        response = self.client.get("/checks/")
        self.assertContains(response, "Create Order", status_code=200)

    # def test_it_cannot_create_alert_for_similar_event(self):
    #     API_KEY = "2ea13bd64c9c06f5ff5501dd6872ecda"

    #     PASSWORD = "d602f072d114aceca3c21a2234582ce3"

    #     EVENT = "products1/create"

    #     NAME = "Create Order"

    #     SHOP_NAME = "Duuka1"

    #     shop_url = "https://%s:%s@duuka1.myshopify.com/admin" % (
    #         API_KEY, PASSWORD)
    #     shopify.ShopifyResource.set_site(shop_url)
    #     shopify.Shop.current
    #     webhook = shopify.Webhook()
    #     webhook.topic = EVENT
    #     webhook.address = "test"
    #     webhook.format = 'json'
    #     webhook.save() 

    #     form = {"api_key": API_KEY,
    #             "password": PASSWORD, "event": EVENT, "name": NAME, "shop_name": SHOP_NAME}


    #     self.client.login(username="alice@example.org", password="password")
    #     response = self.client.post("/checks/create_shopify_alert/", form)
        
    #     shop_url = "https://%s:%s@duuka1.myshopify.com/admin" % (
    #         API_KEY, PASSWORD)
        
    #     assert response.status_code == 400

