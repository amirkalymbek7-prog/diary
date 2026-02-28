#Импорт
from flask import Flask, render_template, request, redirect, session
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Задаем секретный ключ для работы session
app.secret_key = 'my_top_secret_123'
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True)
    #Заголовок
    title = db.Column(db.String(100), nullable=False)
    #Описание
    subtitle = db.Column(db.String(300), nullable=False)
    #Текст
    text = db.Column(db.Text, nullable=False)
    #email владельца карточки
    user_email = db.Column(db.String(100), nullable=False)

    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Задание №1. Создать таблицу User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(35), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    
#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        #Задание №4. Реализовать проверку пользователей
        users = User.query.all()
        for u in users:
            if form_login == u.email and form_password == u.password:
                session["user_email"] = u.email
                return redirect("/index")
        return render_template('login.html', error = "Неверные логин или пароль")
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        #Задание №3. Реализовать запись пользователей
        users = User.query.all()
        for u in users:
            if email == u.email:
                return render_template('registration.html', error = "Такой пользователь уже существует")
        user = User(email = email, password = password)
        db.session.add(user)
        db.session.commit()



        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Запуск страницы с контентом
@app.route('/index')
def index():
    #Задание №4. Сделай, чтобы пользователь видел тольуо свои карточки
    cards = Card.query.filter_by(user_email=session["user_email"]).all()
    return render_template('index.html', cards=cards)

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

#Запуск страницы c созданием карты
@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        #Задание №4. Сделай, чтобы создание карточки происходило от имени пользователя
        card = Card(title=title, subtitle=subtitle, text=text, user_email = session["user_email"])

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
