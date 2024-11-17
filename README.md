<h1>Django ile İHA Kiralama Projesi | Hava Aracı Üretim Uygulaması</h1>

Django ile yazılmış basit bir hava aracı üretim uygulaması.

# İndirme
- <h3>1. Projeyi indirin.</h3>

```cmd
git clone https://github.com/mozancetin/BaykarProject.git
```

```cmd
cd BaykarProject
```

- <h3>2. Gereksinimleri indirin.</h3>

```cmd
pip install -r requirements.txt
```

- <h3>3. Docker'ı başlatın.</h3>

```cmd
docker-compose up --build
```

- <h3>4. Veritabanını kurun.</h3>

```cmd
docker-compose exec web python manage.py migrate
```

Site kullanıma hazır! <br>
<h3>API DÖKÜMANTASYONU: /api/v1/swagger/</h3>

# Sayfalar

- <h3>Personel Giriş Ekranı (/)</h3>

![Personel Giriş Ekranı](https://github.com/mozancetin/BaykarProject/blob/main/images/login.png)

- <h3>Personel Kayıt Ekranı (/register/)</h3>

![Personel Kayıt Ekranı](https://github.com/mozancetin/BaykarProject/blob/main/images/register.png)

- <h3>Personel Paneli (/dashboard/)</h3>

![Personel Paneli](https://github.com/mozancetin/BaykarProject/blob/main/images/dashboard.png)

- <h3>Personel Paneli [Montaj Takımı] (/dashboard/)</h3>

![Personel Paneli Montaj Takımı](https://github.com/mozancetin/BaykarProject/blob/main/images/montaj1.png)

- <h3>Personelin Takımı (/dashboard/team/)</h3>

![Personelin Takımı](https://github.com/mozancetin/BaykarProject/blob/main/images/takımım.png)

- <h3>Personel Çıkış (/logout/)</h3>

# Yardımcılar

- <h3>Rastgele Parça Oluşturucu</h3>

![Rastgele Parça Oluşturucu](https://github.com/mozancetin/BaykarProject/blob/main/images/rastgele_parca.png)

# API URL'leri
**Dökümantasyon için: _/api/v1/swagger/_ veya _/api/v1/redoc/_**
<br>
API kullanımı için hesap oluşturulup giriş yapılması gerekmektedir.

<hr>

- <h3>Personel Listesi</h3>

```/api/v1/employee/list/ (GET)```

<hr>

- <h3>Uçak Listesi</h3>

```/api/v1/plane/list/ (GET)```

<hr>

- <h3>Parça Listesi</h3>

```/api/v1/part/list/ (GET)```

<hr>

- <h3>ID ile Personel Bilgisi Alma</h3>

```/api/v1/employee/<int:id>/ (GET)```

<hr>

- <h3>ID ile Uçak Bilgisi Alma</h3>

```/api/v1/plane/<int:id>/ (GET)```

<hr>

- <h3>ID ile Parça Bilgisi Alma</h3>

```/api/v1/part/<int:id>/ (GET)```

<hr>

- <h3>Giriş Yapmış Kullanıcının Takımdaki Personel Listesi</h3>

```/api/v1/employee/by-team/ (GET)```

<hr>

- <h3>Uçak Tipine ve Parça Tipine Göre Gruplandırılmış Parça Listesi</h3>

```/api/v1/part/grouped/ (GET)```

<hr>

- <h3>Uçak Üretimi</h3>

```/api/v1/plane/create/ (POST)```

**Body Parametresi:** plane_type (str) ["TB2", "TB3", "AKI", "KIZ"]
<br>
**Uçak üretilebilmesi için gerekli parçalar bulunmalı:** Kanat (2), Gövde (1), Kuyruk (1), Aviyonik (1)

<hr>

- <h3>Parça Oluşturma</h3>

```/api/v1/part/create/ (POST)```

**Body Parametresi:** plane_type (str) ["TB2", "TB3", "AKI", "KIZ"]

<hr>

- <h3>Parça Geri Dönüştürme</h3>

```/api/v1/part/delete/ (DELETE)```

**Body Parametresi:** part_id
<br>
**Kural:** Parçanın geri dönüştürülebilmesi için parçayı üreten takımın bu çağrıyı yapması gerekir. 

<hr>

- <h3>Rastgele Parça Oluşturur</h3>

```/api/v1/generate/part/<int:count>/ (GET)```

<hr>

- <h3>API Dökümantasyonu 1</h3>

```/api/v1/swagger/ (GET)```

<hr>

- <h3>API Dökümantasyonu 2</h3>

```/api/v1/redoc/ (GET)```
