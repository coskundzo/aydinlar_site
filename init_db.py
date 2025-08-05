from app import app, db
from models import User, Content, Product, Project
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Tabloları oluştur
        db.create_all()
        
        # Admin kullanıcı var mı kontrol et
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Admin kullanıcı oluştur
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin kullanıcı oluşturuldu: admin / admin123")
        else:
            print("Admin kullanıcı zaten mevcut")

if __name__ == '__main__':
    init_database()
