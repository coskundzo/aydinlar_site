# Aydınlar İnşaat Web Sitesi

Bu proje, Aydınlar İnşaat şirketi için geliştirilmiş Flask tabanlı bir web uygulamasıdır.

## Özellikler

- 🏠 Ana sayfa slider ve kart yönetimi
- 🏗️ Proje yönetimi (Mekanik, Elektrik, Su, Doğal Gaz kategorileri)
- 📦 Ürün yönetimi
- 👥 Kullanıcı kayıt ve giriş sistemi
- 🔐 Admin panel (sadece admin kullanıcılar için)
- 📱 Responsive tasarım

## Teknolojiler

- **Backend:** Flask, SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Authentication:** Werkzeug Security

## Kurulum

### Gereksinimler
- Python 3.7+
- pip

### 1. Projeyi İndir
```bash
git clone https://github.com/coskundzo/aydinlar_site.git
cd aydinlar_site
```

### 2. Sanal Ortam Oluştur
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# veya
source venv/bin/activate  # Linux/Mac
```

### 3. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 4. Veritabanını Başlat
```bash
python init_db.py
```

### 5. Uygulamayı Çalıştır
```bash
python app.py
```

Uygulama http://localhost:5000 adresinde çalışacaktır.

## Admin Girişi

Varsayılan admin bilgileri:
- **Kullanıcı adı:** admin
- **Şifre:** admin123

## Proje Yapısı

```
insaat_web/
├── app.py              # Ana uygulama dosyası
├── models.py           # Veritabanı modelleri
├── requirements.txt    # Python bağımlılıkları
├── init_db.py         # Veritabanı başlatma scripti
├── static/            # Statik dosyalar (CSS, JS, resimler)
├── templates/         # HTML şablonları
├── instance/          # Veritabanı dosyası
└── migrations/        # Veritabanı migration dosyaları
```

## Kullanım

### Admin Panel
- `/admin` adresinden admin paneline erişebilirsiniz
- Ana sayfa kartları, slider, ürün ve proje yönetimi yapabilirsiniz

### Projeler
- Projeler 4 kategoride yönetilebilir: Mekanik, Elektrik, SU, Doğal gaz
- Her proje "Devam Eden" veya "Tamamlanan" durumuna sahip olabilir

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik ekle'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Proje ile ilgili sorularınız için: [coskundzo@gmail.com](mailto:coskundzo@gmail.com)
