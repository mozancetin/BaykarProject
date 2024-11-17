from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import CustomUser, Plane, Part

class APITestCase(TestCase):
    def setUp(self):
        """API'yi test etmek için client oluşturuyoruz"""
        self.client = APIClient()

        # Test kullanıcısını oluşturuyoruz
        self.user = CustomUser.objects.create_user(
            full_name="Test User",
            team_type="Kanat",
            email="test@gmail.com",
            password="test1234",
            age=34
        )

        # Test kullanıcısını giriş yapmaya zorluyoruz. Çünkü API fonksiyonlarımız giriş yapılmış personellerde çalışıyor.
        self.client.force_authenticate(user=self.user)

        # Test uçağı ve parçası oluşturuyoruz.
        self.plane = Plane.objects.create(
            plane_type="AKI",
            employee=self.user,
        )

        self.part = Part.objects.create(
            part_type="Kanat",
            plane=self.plane,
            plane_type="AKI",
            employee=self.user,
            mounted=False,
        )

    def test_list_employee(self):
        """Personel listesini alma testi"""

        response = self.client.get("/api/v1/employee/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test User", response.data[0]["full_name"])

    def test_list_plane(self):
        """Uçak listesini alma testi"""

        response = self.client.get("/api/v1/plane/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("AKI", response.data[0]["plane_type"])

    def test_list_part(self):
        """Parça listesini giriş yapmış kullanıcının takımına göre alma testi"""

        response = self.client.get("/api/v1/part/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Kanat", response.data[0]["part_type"])

    def test_get_employee_by_id(self):
        """ID ile kullanıcı bilgisi alma testi"""

        response = self.client.get(f"/api/v1/employee/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], "Test User")

    def test_get_plane_by_id(self):
        """ID ile uçak bilgisi alma testi"""

        response = self.client.get(f"/api/v1/plane/{self.plane.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["plane_type"], "AKI")

    def test_get_part_by_id(self):
        """ID ile parça bilgisi alma testi"""

        response = self.client.get(f"/api/v1/part/{self.part.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["part_type"], "Kanat")

    def test_get_employee_by_team(self):
        """Aynı takımdaki personellerin listesini alma testi"""

        response = self.client.get("/api/v1/employee/by-team/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["team_type"], "Kanat")

    def test_get_grouped_part(self):
        """Parça listesini uçak tipi ve parça tipine göre gruplandırılmış biçimde alma testi"""

        response = self.client.get("/api/v1/part/grouped/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("AKI", response.data)

    def test_generate_part(self):
        """Rastgele parça oluşturma testi"""

        response = self.client.get("/api/v1/generate/part/10/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)

    def test_create_part(self):
        """Yeni parça oluşturma testi"""

        data = {"plane_type": "TB2"}
        response = self.client.post("/api/v1/part/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("success", response.data)

    def test_create_plane(self):
        """
        Yeni uçak oluşturma testi
        
        Yeterince parçamız olmadığı için HTTP[400] Bad Request dönmeli
        """

        data = {"plane_type": "TB2"}
        response = self.client.post("/api/v1/plane/create/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_delete_part(self):
        """Parça silme testi"""

        data = {"part_id": self.part.id}
        response = self.client.delete("/api/v1/part/delete/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)