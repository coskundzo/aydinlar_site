from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Content, Product, Project, Contact
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = "gizli_anahtar"  # Güvenli bir anahtar olmalı
db.init_app(app)

# Admin decorator
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        user = User.query.filter_by(username=session['username']).first()
        if not user or not user.is_admin:
            flash('Admin yetkisi gerekli!')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_admin_status():
    is_admin = False
    if session.get('username'):
        user = User.query.filter_by(username=session['username']).first()
        if user and user.is_admin:
            is_admin = True
    return dict(is_admin=is_admin)


@app.route('/')
def index():
    cards = Content.query.filter_by(section='card').order_by(Content.order_index).all()
    sliders = Content.query.filter_by(section='slider').order_by(Content.order_index).all()
    return render_template('index.html', cards=cards, sliders=sliders)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bayilik')
def bayilik():
    return render_template('bayilik.html')



@app.route('/products')
def products():
    products = Content.query.filter_by(section='product').all()
    return render_template('products.html', products=products)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/iletisim', methods=['POST'])
def iletisim():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # İletişim verisini veritabanına kaydet
        try:
            contact = Contact(
                name=name,
                email=email,
                message=message
            )
            db.session.add(contact)
            db.session.commit()
            flash(f'Merhaba {name}, mesajınız başarıyla kaydedildi! En kısa sürede size dönüş yapacağız.')
        except Exception as e:
            db.session.rollback()
            flash('Mesajınız kaydedilirken bir hata oluştu. Lütfen tekrar deneyin.')
            
        return redirect(url_for('contact'))
    
    return redirect(url_for('contact'))

@app.route('/projects')
def projects():
    projects = Content.query.filter_by(section='project').all()
    return render_template('projects.html', projects=projects)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Kullanıcı adı veya şifre hatalı!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Admin Panel Routes
@app.route('/admin')
@admin_required
def admin():
    cards = Content.query.filter_by(section='card').order_by(Content.order_index).all()
    sliders = Content.query.filter_by(section='slider').order_by(Content.order_index).all()
    products = Content.query.filter_by(section='product').all()
    projects = Content.query.filter_by(section='project').all()
    return render_template('admin.html', cards=cards, sliders=sliders, products=products, projects=projects)

@app.route('/admin/add_product', methods=['POST'])
@admin_required
def add_product():
    title = request.form['title']
    description = request.form['description']
    image_url = request.form['image_url']
    
@app.route('/admin/add_project', methods=['POST'])
@admin_required
def add_project():
    title = request.form['title']
    description = request.form['description']
    image_url = request.form['image_url']
    category = request.form['category']
    status = request.form['status']  # Durum bilgisini al

    project = Content(
        title=title,
        description=description,
        image_url=image_url,
        section='project',
        category=category,
        status=status,  # Durum bilgisini kaydet
        order_index=0
    )
    db.session.add(project)
    db.session.commit()
    flash('Proje başarıyla eklendi!')
    return redirect(url_for('admin'))

@app.route('/admin/add_card', methods=['POST'])
@admin_required
def add_card():
    title = request.form['title']
    description = request.form['description']
    image_url = request.form['image_url']
    order_index = request.form.get('order_index', 1, type=int)
    
    card = Content(
        title=title,
        description=description,
        image_url=image_url,
        section='card',
        order_index=order_index
    )
    db.session.add(card)
    db.session.commit()
    flash('Kart başarıyla eklendi!')
    return redirect(url_for('admin'))

@app.route('/admin/add_slider', methods=['POST'])
@admin_required
def add_slider():
    title = request.form['title']
    image_url = request.form['image_url']
    order_index = request.form.get('order_index', 1, type=int)
    
    slider = Content(
        title=title,
        description='',
        image_url=image_url,
        section='slider',
        order_index=order_index
    )
    db.session.add(slider)
    db.session.commit()
    flash('Slider başarıyla eklendi!')
    return redirect(url_for('admin'))

@app.route('/admin/delete_project/<int:id>')
@admin_required
def delete_project(id):
    project = Content.query.filter_by(id=id, section='project').first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash('Proje silindi!')
    return redirect(url_for('admin'))

@app.route('/admin/delete_card/<int:id>')
@admin_required
def delete_card(id):
    card = Content.query.filter_by(id=id, section='card').first_or_404()
    db.session.delete(card)
    db.session.commit()
    flash('Kart silindi!')
    return redirect(url_for('admin'))

@app.route('/admin/delete_slider/<int:id>')
@admin_required
def delete_slider(id):
    slider = Content.query.filter_by(id=id, section='slider').first_or_404()
    db.session.delete(slider)
    db.session.commit()
    flash('Slider silindi!')
    return redirect(url_for('admin'))

@app.route('/detail/<content_type>/<int:item_id>')
def detail(content_type, item_id):
    # Content tablosundan section ve id'ye göre veri çek
    if content_type in ['project', 'product', 'card', 'slider']:
        item = Content.query.filter_by(id=item_id, section=content_type).first_or_404()
    else:
        flash('Geçersiz içerik tipi!')
        return redirect(url_for('index'))
    
    return render_template('detail.html', item=item, content_type=content_type)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        # Tüm içeriklerde arama yap
        results = Content.query.filter(
            Content.title.contains(query) | 
            Content.description.contains(query)
        ).all()
    else:
        results = []
    return render_template('search_result.html', results=results, query=query)

@app.route('/admin/edit_project/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_project(id):
    project = Content.query.filter_by(id=id, section='project').first_or_404()
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.image_url = request.form['image_url']
        project.category = request.form['category']
        project.status = request.form['status']  # Status güncellemeyi aktif hale getirdik
        db.session.commit()
        flash('Proje güncellendi!')
        return redirect(url_for('admin'))
    return render_template('edit_project.html', project=project)

@app.route('/admin/edit_card/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_card(id):
    card = Content.query.filter_by(id=id, section='card').first_or_404()
    if request.method == 'POST':
        card.title = request.form['title']
        card.description = request.form['description']
        card.image_url = request.form['image_url']
        card.order_index = request.form.get('order_index', card.order_index, type=int)
        db.session.commit()
        flash('Kart başarıyla güncellendi!')
        return redirect(url_for('admin'))
    # GET isteği için kart verilerini JSON olarak döndür
    return {
        'id': card.id,
        'title': card.title,
        'description': card.description,
        'image_url': card.image_url,
        'order_index': card.order_index
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
 