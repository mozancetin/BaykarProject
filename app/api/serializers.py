from rest_framework import serializers
from core.models import CustomUser, Plane, Part

# Bu dosyada objelerimizi kolayca JSON verisine çevirmek için serializer'larımızı tanımlıyoruz.

class EmployeeSerializer(serializers.ModelSerializer):
    # Takım ismini tamamen görebilmek için bir fonksiyon ekliyoruz.
    full_team_type = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'team_type', 'age', 'full_team_type'] # JSON verimizde görünmesi gereken alanları ekliyoruz.

    # Tam takım ismini veren fonksiyon.
    def get_full_team_type(self, obj : CustomUser):
        return obj.get_full_team_type()

class PlaneSerializer(serializers.ModelSerializer):
    # JSON verimizde uçağın ilişkili olduğu personelin bilgilerini de dahil ediyoruz.
    employee = EmployeeSerializer(read_only=True)
    # Uçak tipini tamamen görebilmek için (çünkü model dosyasında 3 harfli olacak şekilde kısaltma kullandık) bir fonksiyon ekliyoruz
    full_plane_type = serializers.SerializerMethodField()
    class Meta:
        model = Plane
        fields = ['id', 'plane_type', 'employee', 'created_at', 'full_plane_type'] # JSON verimizde görünmesi gereken alanları ekliyoruz.

    # Tam uçak tipini veren fonksiyon.
    def get_full_plane_type(self, obj : Plane):
        return obj.get_full_plane_type()

class PartSerializer(serializers.ModelSerializer):
    # JSON verimizde parçanın ilişkili olduğu personelin ve uçağın bilgilerini de dahil ediyoruz.
    employee = EmployeeSerializer(read_only=True)
    plane = PlaneSerializer(read_only=True)
    # Uçak tipini tamamen görebilmek için (çünkü model dosyasında 3 harfli olacak şekilde kısaltma kullandık) bir fonksiyon ekliyoruz
    full_plane_type = serializers.SerializerMethodField()
    class Meta:
        model = Part
        fields = ['id', 'part_type', 'plane', 'plane_type', 'employee', 'mounted', 'created_at', 'full_plane_type'] # JSON verimizde görünmesi gereken alanları ekliyoruz.

    # Tam uçak tipini veren fonksiyon.
    def get_full_plane_type(self, obj : Part):
        return obj.get_full_plane_type()