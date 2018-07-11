from hc.api.models import Check
from hc.test import BaseTestCase


class UpdateDepartmentTestCase(BaseTestCase):

    def setUp(self):
        super(UpdateDepartmentTestCase, self).setUp()
        self.check = Check(user=self.alice)
        self.check.save()

    def test_department_update_works(self):
        url = "/checks/%s/name/" % self.check.code
        payload = {"department": "Finance"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        self.assertRedirects(response, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.departments == "Finance"

    def test_many_departments_to_check(self):
        url = "/checks/%s/name/" % self.check.code
        payload = {"department": "Finance IT Facilities"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, data=payload)
        self.assertRedirects(response, "/checks/")

        check = Check.objects.get(code=self.check.code)
        self.assertEqual(check.departments, 'Finance IT Facilities')

    def test_department_displays(self):
        url = "/checks/%s/name/" % self.check.code
        payload = {"department": "Finance IT"}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, data=payload)
        res = self.client.get("/checks/")
        self.assertIn("Finance", res.content)
        self.assertIn("IT", res.content)
