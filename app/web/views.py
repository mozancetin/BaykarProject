from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json

# Kendi özel User modelimizi oluşturup Django'nun User modelini kullanmayacağımız için kendi User modelimizi alıyoruz.
User = get_user_model()

def register(request):
    """
    Kayıt sayfasını çalıştıran fonksiyon.

    Request Method:
    - GET: register.html sayfasını verir. (Personel kayıt sayfası)
    - POST: register.html sayfasındaki formun doldurulmasıyla elde edilen bilgileri kullanarak yeni bir personel oluşturur.
    """

    # Zaten bir kullanıcı giriş yapmışsa personel paneline yönlendiriyoruz.
    if request.user.id != None:
        return redirect("dashboard")
    
    # Metot kontrolü.
    if request.method == 'POST':
        # Personel oluşturmak için gerekli bilgileri doldurulan formdan alıyoruz.
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        age = request.POST.get('age')
        team_type = request.POST.get('team_type')

        # Bilgiler geçerliyse aldığımız bilgilerle personel oluşturuyoruz.
        if email and full_name and password and age and team_type:
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                age=age,
                team_type=team_type
            )
            # Kaydın başarılı olup olmadığını kontrol ediyoruz. Eğer başarıyla kayıt olunduysa kayıt olan kullanıcıya giriş yaptırıyoruz ve panele yönlendiriyoruz.
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("dashboard")
            
        # Bilgiler geçersiz ise hata mesajı dönüyoruz.
        messages.error(request, "Geçersiz bilgiler")
        return redirect("register")
    return render(request, "register.html")

def custom_login(request):
    """
    Giriş sayfasını çalıştıran fonksiyon.

    Request Method:
    - GET: login.html sayfasını verir. (Personel giriş ekranı)
    - POST: Giriş bilgilerini kontrol eder ve buna göre panele giriş için yetkilendirir.
    """

    # Zaten bir kullanıcı giriş yapmışsa personel paneline yönlendiriyoruz.
    if request.user.id != None:
        return redirect("dashboard")
    
    # Metot kontrolü.
    if request.method == 'POST':
        try:
            # Giriş formundan verileri alıyoruz.
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        # Aldığımız verilerin doğruluğunu kontrol edip bu verilere sahip olan personele giriş yaptırıyoruz.
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": "Başarıyla giriş yapıldı!"}, status=200)
        else:
            return JsonResponse({"error": "Giriş bilgileri geçersiz"}, status=400)
    return render(request, "login.html")

@login_required(login_url='/')
def dashboard(request):
    """
    Giriş yapılmışsa personel panelini verir. Montaj takımı ve diğer takımlar için 2 ayrı panel verir. Giriş yapılmamışsa giriş sayfasına yönlendirir.
    """
    if request.user.team_type != "Montaj":
        return render(request, "dashboard_parts.html")
    else:
        return render(request, "dashboard_assembly.html")
    
@login_required(login_url='/')
def team(request):
    """
    Giriş yapılmışsa personelin takımının listesinin olduğu sayfayı verir. Giriş yapılmamışsa giriş sayfasına yönlendirir.
    """
    return render(request, "team.html")

def custom_logout(request):
    """
    Giriş yapmış olan kullanıcının çıkış yapmasını sağlar.
    """
    logout(request)
    return redirect('login')