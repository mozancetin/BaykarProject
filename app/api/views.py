from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import random
import string
from collections import defaultdict
from core.models import CustomUser, Plane, Part
from .serializers import EmployeeSerializer, PlaneSerializer, PartSerializer

@swagger_auto_schema(
    method="get",
    operation_description="Personel listesini verir.",
    responses={200: "Personel listesi"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_employees(request):
    """Personel listesini verir"""

    employees = CustomUser.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="Üretilmiş uçakların listesini verir.",
    responses={200: "Üretilmiş uçakların listesi"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_planes(request):
    """Üretilmiş uçak listesini verir"""

    planes = Plane.objects.all()
    serializer = PlaneSerializer(planes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="Üretilmiş parçaların listesini verir.",
    responses={200: "Üretilmiş parça listesi"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_parts(request):
    """Giriş yapmış olan kullanıcıya göre belli bir parça tipindeki üretilmiş parçaları verir"""

    # Parçaları üretim tarihine göre yeniden eskiye doğru sıralayarak alıyoruz.
    parts = Part.objects.filter(part_type = request.user.team_type).order_by("-created_at").all()
    serializer = PartSerializer(parts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="Verilen id parametresi ile eşleşen personel bilgilerini verir.",
    responses={200: "{id} ID'li personel bilgileri"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employee_by_id(request, id):
    """
    Verilen id parametresi ile eşleşen personeli verir.
    
    Parametreler:
    - URL Parametreleri:
        - id : int (employee_id)

    ---
    id: Personel ID'si.
    """

    employee = CustomUser.objects.filter(id=id).first()

    if not employee:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="Verilen id parametresi ile eşleşen uçak bilgilerini verir.",
    responses={200: "{id} ID'li uçak bilgileri"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_plane_by_id(request, id):
    """
    Verilen id parametresi ile eşleşen uçağı verir.
    
    Parametreler:
    - URL Parametreleri:
        - id : int (plane_id)

    ---
    id: Uçak ID'si.
    """

    plane = Plane.objects.filter(id=id).first()

    if not plane:
        return Response({"error": "Plane not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PlaneSerializer(plane)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="Verilen id parametresi ile eşleşen parça bilgilerini verir.",
    responses={200: "{id} ID'li parça bilgileri"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_part_by_id(request, id):
    """
    Verilen id parametresi ile eşleşen parçayı verir.
    
    Parametreler:
    - URL Parametreleri:
        - id : int (part_id)

    ---
    id: Parça ID'si.
    """

    part = Part.objects.filter(id=id).first()

    if not part:
        return Response({"error": "Part not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PartSerializer(part)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="İsteği yapan kişinin takımındaki personel listesini verir.",
    responses={200: "Aynı takımdaki personel bilgileri"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_employees_by_team(request):
    """
    İsteği yapan kişinin takımındaki personel listesini verir
    """

    employees = CustomUser.objects.filter(team_type=request.user.team_type)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="Parçaları uçak tipi ve parça tipine göre gruplandırarak verir.",
    responses={200: "Gruplandırılmış parça listesi"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_grouped_parts(request):
    """
    Parçaları uçak tipi ve parça tipine göre gruplandırarak verir.
    
    Bu fonksiyonu bir uçağın üretilebilmesi için hangi parçadan kaç taneye ihtiyacımızın olduğunu görmek için kullanıyoruz.
    """

    # Monte edilmemiş parçaları alır. Böylece uçak üretmek için kaç parçamızın olduğunu anlayacağız.
    parts = Part.objects.filter(mounted=False).all()
    grouped = defaultdict(lambda: defaultdict(list)) # KeyError almamak için içini boş listelerle otomatik dolduracak bir defaultdict tanımlıyoruz.

    # Parçaları uçak tipi ve parça tipine göre gruplandırma
    for part in parts:
        # "TB1": {"Kanat": object, "Gövde": object, ...}, "TB2": {"Kanat": object, "Gövde": object, ...} şeklinde bir yapı oluşturuyoruz
        grouped[part.plane_type][part.part_type].append(PartSerializer(part).data) 

    # defaultdict'i normal dict haline getirme.
    grouped_data = {plane_type: dict(part_types) for plane_type, part_types in grouped.items()}

    return Response(grouped_data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="get",
    operation_description="Rastgele bilgiler ile verilen count parametresi sayısı kadar parça üretir.",
    responses={200: "Başarıyla oluşturuldu. {count} sayıda rastgele parça üretimi"},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_part(request, count):
    """
    Rastgele bilgiler ile verilen count parametresi sayısı kadar parça üretir.
    
    Test amaçlı kullanıyoruz. Personel panelindeki 'Rastgele Parça Üret' butonunu çalıştırıyor. Test ederken tek tek veri girmek zorunda kalmamak için. Production seviyesinde erişimi kısıtlanmalı.
    """

    # 4 dummy user oluşturuyorum ki rastgele oluşturduğumuz parçalara bir personel atayabilelim.
    kanat_user = CustomUser.objects.filter(full_name="random_kanat").first()
    gövde_user = CustomUser.objects.filter(full_name="random_gövde").first()
    kuyruk_user = CustomUser.objects.filter(full_name="random_kuyruk").first()
    aviyonik_user = CustomUser.objects.filter(full_name="random_aviyonik").first()

    # Bu 4 dummy user'ı daha önce oluşturdum mu diye kontrol ediyorum. Oluşturmadıysam bu aşamada oluşturuyorum.
    if kanat_user == None:
        kanat_user = CustomUser.objects.create(
            full_name="random_kanat",
            team_type="Kanat",
            age=random.randint(18, 40),
            email="random_kanat@gmail.com",
            # Bu hesapları giriş yapmak için değil rastgele parça üretmek için kullanacağız bu yüzden rastgele şifre atıyorum
            password=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)) 
        )

    if gövde_user == None:
        gövde_user = CustomUser.objects.create(
            full_name="random_gövde",
            team_type="Gövde",
            age=random.randint(18, 40),
            email="random_gövde@gmail.com",
            # Bu hesapları giriş yapmak için değil rastgele parça üretmek için kullanacağız bu yüzden rastgele şifre atıyorum
            password=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)) 
        )

    if kuyruk_user == None:
        kuyruk_user = CustomUser.objects.create(
            full_name="random_kuyruk",
            team_type="Kuyruk",
            age=random.randint(18, 40),
            email="random_kuyruk@gmail.com",
            # Bu hesapları giriş yapmak için değil rastgele parça üretmek için kullanacağız bu yüzden rastgele şifre atıyorum
            password=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)) 
        )

    if aviyonik_user == None:
        aviyonik_user = CustomUser.objects.create(
            full_name="random_aviyonik",
            team_type="Aviyonik",
            age=random.randint(18, 40),
            email="random_aviyonik@gmail.com",
            # Bu hesapları giriş yapmak için değil rastgele parça üretmek için kullanacağız bu yüzden rastgele şifre atıyorum
            password=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)) 
        )

    USERS = [kanat_user, gövde_user, kuyruk_user, aviyonik_user]
    PART_TYPES = ["Kanat", "Gövde", "Kuyruk", "Aviyonik"]
    PLANE_TYPES = ["TB2", "TB3", "AKI", "KIZ"]

    for _ in range(count):
        # Parça oluşturmak için parça tipini ve uçak tipini rastgele seçiyorum.
        plane_type = random.choice(PLANE_TYPES)
        part_type = random.choice(PART_TYPES)
        
        # Rastgele parçayı oluşturuyorum.
        p = Part.objects.create(
            part_type=part_type,
            plane=None,
            plane_type=plane_type,
            employee=USERS[PART_TYPES.index(part_type)],
            mounted=False
        )

    return Response({"success": "Successfully generated."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method="post",
    operation_description="Verilen uçak tipine göre ({plane_type}) yeni bir parça üretir.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'plane_type': openapi.Schema(type=openapi.TYPE_STRING, description='Uçak tipi ("TB2", "TB3", "AKI", "KIZ")'),
        },
    ),
    responses={201: "Parça başarıyla oluşturuldu. Parça ID'si: {part_id}", 500: "Hata", 405: "İzin verilmeyen metot"},
)
@csrf_exempt
@api_view(['POST'])
def create_part(request):
    """
    Verilen uçak tipine göre yeni bir parça üretir.

    Parametreler:
    - Body: 
        - plane_type : str ["TB2", "TB3", "AKI", "KIZ"]

    ---
    plane_type: Oluşturulacak parçanın hangi uçak tipine ait olduğunu gösterir.
    """

    # İstek metotunun doğruluğunu kontrol ediyoruz. POST olmalı.
    if request.method == 'POST':
        try:
            # Verilen uçak tipini body'den çekerek parçamızı bu uçak tipine göre oluşturuyoruz.
            plane_type = request.data.get('plane_type')
            part = Part.objects.create(
                # Takım tipi etiketleri ile parça tipi etiketleri aynı. Bu yüzden parça tipini direkt olarak giriş yapmış kullanıcının takım tipi olarak verebiliriz
                part_type=request.user.team_type, 
                plane=None,
                plane_type=plane_type,
                employee=request.user,
                mounted=False
            )

            return Response({"success": "Part created successfully!", "part_id": part.id}, status=201)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response({"error": "Method not allowed."}, status=405)

@swagger_auto_schema(
    method="delete",
    operation_description="Verilen parça id'si ({part_id}) ile eşleşen parçayı geri dönüştürür.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'part_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Geri dönüştürülecek olan parçanın ID'si"),
        },
    ),
    responses={201: "Part created successfully"},
)
@api_view(['DELETE'])
def delete_part(request):
    """
    Verilen id ile eşleşen parçayı geri dönüştürür.

    Parametreler:
    - Body: 
        - part_id : int

    ---
    part_id: Geri dönüştürülecek parçanın ID'si.
    """

    # İstek metotunun doğruluğunu kontrol ediyoruz. DELETE olmalı.
    if request.method == 'DELETE':
        try:
            # Verilen parça id'sini body'den çekerek silinecek parçamızı buluyoruz.
            part_id = request.data.get('part_id')
            part = Part.objects.filter(id=part_id).first()
            if part != None: # Parçayı bulduysak devam ediyoruz
                if part.part_type == request.user.team_type: # Parçayı silmek isteyen kişi parçayı üreten takımdan mı onu kontrol ediyoruz.
                    if not part.mounted: # Parça bir uçağa monte edilmiş mi onu kontrol ediyoruz.
                        deleted = part.delete()
                        if deleted[0] > 0:
                            return Response({"success": "Part deleted successfully!"}, status=200)
                        else:
                            return Response({"error": "Part couldn't be deleted."}, status=500)
                    else:
                        return Response({"error": "Part is mounted and cannot be deleted."}, status=500)
                else:
                    return Response({"error": "Part doesn't belong to your team."}, status=500)
            else:
                return Response({"error": "Part doesn't exists."}, status=500)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    return Response({"error": "Method not allowed."}, status=405)

@swagger_auto_schema(
    method="post",
    operation_description="Verilen uçak tipine ({plane_type}) sahip bir uçak üretir.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'plane_type': openapi.Schema(type=openapi.TYPE_STRING, description='Üretilecek uçağın tipi ("TB2", "TB3", "AKI", "KIZ").'),
        },
    ),
    responses={201: "Uçak başarıyla üretildi! Uçak ID'si: {plane_id}", 500: "Hata", 405: "İzin verilmeyen metot", 400: "Eksik parçalar var, uçak üretilemiyor"},
)
@csrf_exempt
@api_view(['POST'])
def create_plane(request):
    """
    Parça sayısı kontrollerini yaptıktan sonra verilen uçak tipine göre yeni bir uçak üretir ve parçaları monte edilmiş olarak işaretler.

    Parametreler:
    - Body: 
        - plane_type : str ["TB2", "TB3", "AKI", "KIZ"]

    ---
    plane_type: Oluşturulacak parçanın hangi uçak tipine ait olduğunu gösterir.
    """

    # İstek metotunun doğruluğunu kontrol ediyoruz. POST olmalı.
    if request.method == 'POST':
        plane_type = request.data.get('plane_type')
        # Burası karışık görünebilir. Bir uçak oluşturmak için gerekli parça sayısı envanterimizde var mı diye kontrol ediyoruz. Aksi belirtilmediği için parça sayılarını kendim belirledim ve yazılıma gömdüm.
        if Part.objects.filter(part_type="Kanat").filter(plane_type=plane_type).filter(mounted=False).count() < 2 or \
        Part.objects.filter(part_type="Gövde").filter(plane_type=plane_type).filter(mounted=False).count() < 1 or \
        Part.objects.filter(part_type="Kuyruk").filter(plane_type=plane_type).filter(mounted=False).count() < 1 or \
        Part.objects.filter(part_type="Aviyonik").filter(plane_type=plane_type).filter(mounted=False).count() < 1:
            return Response({"error": "Missing parts"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verilen uçak tipini body'den çekerek uçağımızı bu uçak tipinde oluşturuyoruz.
            plane = Plane.objects.create(
                plane_type=plane_type,
                employee=request.user
            )

            # Uçağımızı oluşturduktan sonra kullandığımız parçaları monte edilmiş olarak işaretleyerek ve hangi uçağa monte edildiği bilgisini vererek envanterden kaldırıyoruz.
            for _ in range(2):
                kanat = Part.objects.filter(part_type="Kanat").filter(plane_type=plane_type).filter(mounted=False).first()
                kanat.mounted = True
                kanat.plane = plane
                kanat.save()

            gövde = Part.objects.filter(part_type="Gövde").filter(plane_type=plane_type).filter(mounted=False).first()
            kuyruk = Part.objects.filter(part_type="Kuyruk").filter(plane_type=plane_type).filter(mounted=False).first()
            aviyonik = Part.objects.filter(part_type="Aviyonik").filter(plane_type=plane_type).filter(mounted=False).first()

            gövde.mounted = True
            kuyruk.mounted = True
            aviyonik.mounted = True

            gövde.plane = plane
            kuyruk.plane = plane
            aviyonik.plane = plane
            
            gövde.save()
            kuyruk.save()
            aviyonik.save()

            return Response({"success": "Plane created successfully!", "plane_id": plane.id}, status=201)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    return Response({"error": "Method not allowed."}, status=405)