from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from functools import wraps
import random

# إنشاء تطبيق Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hatha-waste-collection-app-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hatha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إعداد قاعدة البيانات
db = SQLAlchemy(app)

# إعداد Bootstrap
bootstrap = Bootstrap(app)

@app.template_filter('nl2br')
def nl2br(value):
    return value.replace('\n', '<br>')

# نموذج طلب جمع النفايات
class WasteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    preferred_time = db.Column(db.String(50))
    contact_method = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

# نموذج طلبات التوظيف
class EmploymentApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    birth_place = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    education = db.Column(db.String(50))
    experience = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

# نموذج الاشتراك للمؤسسات
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200), nullable=False)
    subscription_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

# نموذج المستخدم
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    pin = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

# نموذج الرسائل
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    sender_deleted = db.Column(db.Boolean, default=False)
    recipient_deleted = db.Column(db.Boolean, default=False)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# صفحة حول التطبيق
@app.route('/about')
def about():
    return render_template('about.html')

# صفحة الخدمات
@app.route('/services')
def services():
    return render_template('services.html')

# صفحة طلب جمع النفايات
@app.route('/request_service', methods=['GET', 'POST'])
def request_service():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        waste_type = request.form.get('waste_type')
        notes = request.form.get('notes')
        preferred_time = request.form.get('preferred_time')
        contact_method = request.form.get('contact_method')
        
        new_request = WasteRequest(
            name=name,
            phone=phone,
            address=address,
            waste_type=waste_type,
            notes=notes,
            preferred_time=preferred_time,
            contact_method=contact_method
        )
        
        try:
            db.session.add(new_request)
            db.session.commit()
            flash('تم إرسال طلبك بنجاح! سنتواصل معك قريباً.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('حدث خطأ أثناء إرسال طلبك. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('request_service.html')

# صفحة الاشتراك للمؤسسات
@app.route('/business_subscription', methods=['GET', 'POST'])
def business_subscription():
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        contact_person = request.form.get('contact_person')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        subscription_type = request.form.get('subscription_type')
        
        new_subscription = Subscription(
            business_name=business_name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            subscription_type=subscription_type
        )
        
        try:
            db.session.add(new_subscription)
            db.session.commit()
            flash('تم تسجيل اشتراكك بنجاح! سنتواصل معك قريباً.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('حدث خطأ أثناء تسجيل اشتراكك. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('business_subscription.html')

# صفحة اتصل بنا 
@app.route('/contact')
def contact():
    return render_template('contact.html')

# صفحة التوظيف
@app.route('/employment', methods=['GET', 'POST'])
def employment():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d')
        birth_place = request.form.get('birth_place')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        address = request.form.get('address')
        education = request.form.get('education')
        experience = request.form.get('experience')
        
        new_application = EmploymentApplication(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            birth_place=birth_place,
            gender=gender,
            phone=phone,
            address=address,
            education=education,
            experience=experience
        )
        
        try:
            db.session.add(new_application)
            db.session.commit()
            flash('تم إرسال طلب التوظيف بنجاح! سنتواصل معك قريباً.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('حدث خطأ أثناء إرسال طلبك. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('employment.html')

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        pin = request.form.get('pin')
        
        user = User.query.filter_by(phone=phone).first()
        
        if user and user.pin == pin and user.is_active:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_phone'] = user.phone
            
            # تحديث وقت آخر تسجيل دخول
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash('تم تسجيل الدخول بنجاح!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('فشل تسجيل الدخول. يرجى التحقق من رقم الهاتف ورمز PIN.', 'danger')
    
    return render_template('login.html')

# صفحة التسجيل
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        # التحقق من عدم وجود مستخدم بنفس رقم الهاتف
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            flash('رقم الهاتف مسجل بالفعل. يرجى تسجيل الدخول.', 'warning')
            return redirect(url_for('login'))
        
        # إنشاء رمز PIN عشوائي (في التطبيق الحقيقي، يجب إرسال هذا الرمز عبر SMS)
        import random
        pin = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        new_user = User(name=name, phone=phone, pin=pin)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'تم التسجيل بنجاح! رمز PIN الخاص بك هو: {pin}', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('حدث خطأ أثناء التسجيل. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('register.html')

# صفحة إعادة تعيين رمز PIN
@app.route('/reset_pin', methods=['GET', 'POST'])
def reset_pin():
    if request.method == 'POST':
        phone = request.form.get('phone')
        
        user = User.query.filter_by(phone=phone).first()
        
        if user:
            # إنشاء رمز PIN جديد (في التطبيق الحقيقي، يجب إرسال هذا الرمز عبر SMS)
            import random
            new_pin = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            user.pin = new_pin
            db.session.commit()
            
            flash(f'تم إعادة تعيين رمز PIN بنجاح! رمز PIN الجديد هو: {new_pin}', 'success')
            return redirect(url_for('login'))
        else:
            flash('لم يتم العثور على مستخدم بهذا الرقم.', 'danger')
    
    return render_template('reset_pin.html')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_phone', None)
    flash('تم تسجيل الخروج بنجاح!', 'success')
    return redirect(url_for('index'))

# دالة للتحقق من تسجيل الدخول
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('يرجى تسجيل الدخول للوصول إلى هذه الصفحة', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# صفحة صندوق الوارد
@app.route('/inbox')
@login_required
def inbox():
    # هنا يمكنك استرجاع الرسائل الواردة من قاعدة البيانات
    # في هذا المثال، نفترض أن المستخدم الحالي هو 'admin'
    messages = Message.query.filter_by(recipient='admin', recipient_deleted=False).order_by(Message.created_at.desc()).all()
    return render_template('inbox.html', messages=messages)

# صفحة صندوق الصادر
@app.route('/outbox')
@login_required
def outbox():
    # هنا يمكنك استرجاع الرسائل الصادرة من قاعدة البيانات
    # في هذا المثال، نفترض أن المستخدم الحالي هو 'admin'
    messages = Message.query.filter_by(sender='admin', sender_deleted=False).order_by(Message.created_at.desc()).all()
    return render_template('outbox.html', messages=messages)

# صفحة إنشاء رسالة جديدة
@app.route('/new_message', methods=['GET', 'POST'])
@login_required
def new_message():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        content = request.form.get('content')
        
        new_msg = Message(
            sender='admin',  # في هذا المثال، نفترض أن المستخدم الحالي هو 'admin'
            recipient=recipient,
            subject=subject,
            content=content
        )
        
        try:
            db.session.add(new_msg)
            db.session.commit()
            flash('تم إرسال الرسالة بنجاح!', 'success')
            return redirect(url_for('outbox'))
        except Exception as e:
            flash('حدث خطأ أثناء إرسال الرسالة. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('new_message.html')

# عرض رسالة محددة
@app.route('/view_message/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    # تحديث حالة القراءة إذا كان المستخدم هو المستلم
    if message.recipient == 'admin' and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('view_message.html', message=message)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة صفحة حذف الرسائل
@app.route('/delete_message/<int:message_id>')
@login_required
def delete_message(message_id):
    with app.app_context():
        message = Message.query.get_or_404(message_id)
        
        if message.recipient == 'admin':
            message.recipient_deleted = True
        elif message.sender == 'admin':
            message.sender_deleted = True
            
        db.session.commit()
    
    return redirect(url_for('inbox'))

# إنشاء تطبيق Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hatha-waste-collection-app-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hatha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# إعداد قاعدة البيانات
db = SQLAlchemy(app)

# إعداد Bootstrap
bootstrap = Bootstrap(app)

# نموذج طلب جمع النفايات
class WasteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    preferred_time = db.Column(db.String(50))
    contact_method = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

# نموذج الاشتراك للمؤسسات
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200), nullable=False)
    subscription_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

# نموذج الرسائل
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    sender_deleted = db.Column(db.Boolean, default=False)
    recipient_deleted = db.Column(db.Boolean, default=False)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# صفحة حول التطبيق
@app.route('/about')
def about():
    return render_template('about.html')

# صفحة الخدمات
@app.route('/services')
def services():
    return render_template('services.html')

# صفحة طلب جمع النفايات
@app.route('/request_service', methods=['GET', 'POST'])
def request_service():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        waste_type = request.form.get('waste_type')
        notes = request.form.get('notes')
        preferred_time = request.form.get('preferred_time')
        contact_method = request.form.get('contact_method')
        
        new_request = WasteRequest(
            name=name,
            phone=phone,
            address=address,
            waste_type=waste_type,
            notes=notes,
            preferred_time=preferred_time,
            contact_method=contact_method
        )
        
        try:
            db.session.add(new_request)
            db.session.commit()
            flash('تم إرسال طلبك بنجاح! سنتواصل معك قريباً.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('حدث خطأ أثناء إرسال طلبك. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('request_service.html')

# صفحة الاشتراك للمؤسسات
@app.route('/business_subscription', methods=['GET', 'POST'])
def business_subscription():
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        contact_person = request.form.get('contact_person')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        subscription_type = request.form.get('subscription_type')
        
        new_subscription = Subscription(
            business_name=business_name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            subscription_type=subscription_type
        )
        
        try:
            db.session.add(new_subscription)
            db.session.commit()
            flash('تم تسجيل اشتراكك بنجاح! سنتواصل معك قريباً.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('حدث خطأ أثناء تسجيل اشتراكك. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('business_subscription.html')

# صفحة اتصل بنا
@app.route('/contact')
def contact():
    return render_template('contact.html')

# صفحة صندوق الوارد
@app.route('/inbox')
def inbox():
    # هنا يمكنك استرجاع الرسائل الواردة من قاعدة البيانات
    # في هذا المثال، نفترض أن المستخدم الحالي هو 'admin'
    messages = Message.query.filter_by(recipient='admin', recipient_deleted=False).order_by(Message.created_at.desc()).all()
    return render_template('inbox.html', messages=messages)

# صفحة صندوق الصادر
@app.route('/outbox')
def outbox():
    # هنا يمكنك استرجاع الرسائل الصادرة من قاعدة البيانات
    # في هذا المثال، نفترض أن المستخدم الحالي هو 'admin'
    messages = Message.query.filter_by(sender='admin', sender_deleted=False).order_by(Message.created_at.desc()).all()
    return render_template('outbox.html', messages=messages)

# صفحة إنشاء رسالة جديدة
@app.route('/new_message', methods=['GET', 'POST'])
def new_message():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        content = request.form.get('content')
        
        new_msg = Message(
            sender='admin',  # في هذا المثال، نفترض أن المستخدم الحالي هو 'admin'
            recipient=recipient,
            subject=subject,
            content=content
        )
        
        try:
            db.session.add(new_msg)
            db.session.commit()
            flash('تم إرسال الرسالة بنجاح!', 'success')
            return redirect(url_for('outbox'))
        except Exception as e:
            flash('حدث خطأ أثناء إرسال الرسالة. يرجى المحاولة مرة أخرى.', 'danger')
            print(e)
    
    return render_template('new_message.html')

# عرض رسالة محددة
@app.route('/view_message/<int:message_id>')
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    
    # تحديث حالة القراءة إذا كان المستخدم هو المستلم
    if message.recipient == 'admin' and not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('view_message.html', message=message)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القوالب
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# إنشاء قاعدة البيانات
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

# إضافة متغير now لجميع القو