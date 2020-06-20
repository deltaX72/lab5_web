print("Hello world")
from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
    return " <html><head></head> <body> Hello World! </body></html>"

from flask import render_template

#наша новая функция сайта
@app.route("/data_to")
def data_to():
    #создаем переменные с данными для передачи в шаблон
    some_pars = {'user':'Ivan','color':'red'}
    some_str = 'Hello my dear friends!'
    some_value = 10
    #передаем данные в шаблон и вызываем его
    return render_template('simple.html',some_str = some_str,
    some_value = some_value,some_pars=some_pars)

# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfhxKYZAAAAACkvFUsEiXJO4_xY71P8YUQcK5JF'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfhxKYZAAAAAJTyWH1OrZev3asBT_tNDnvdup-T'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
bootstrap = Bootstrap(app)

# создаем форму для загрузки файла
class NetForm(FlaskForm):
    # поле для введения строки, валидируется наличием данных
    # валидатор проверяет введение данных после нажатия кнопки submit
    # и указывает пользователю ввести данные если они не введены
    # или неверны
    openid = StringField('openid', validators = [DataRequired()])
    # поле загрузки файла
    # здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
    FileRequired(),
    FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # поле формы с capture
    recaptcha = RecaptchaField()
    #кнопка submit, для пользователя отображена как send
    submit = SubmitField('send')

# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
# подключаем наш модуль и переименовываем
# для исключения конфликта имен
import net as neuronet

# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
    # создаем объект формы
    form = NetForm()
    # обнуляем переменные передаваемые в форму
    filename=None
    neurodic = {}
    # проверяем нажатие сабмит и валидацию введенных данных
    if form.validate_on_submit():
        # файлы с изображениями читаются из каталога static
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10,'./static')
        # передаем все изображения в каталоге на классификацию
        # можете изменить немного код и передать только загруженный файл
        decode = neuronet.getresult(fimage)
        # записываем в словарь данные классификации
        for elem in decode:
            neurodic[elem[0][1]] = elem[0][2]
        # сохраняем загруженный файл
        form.upload.data.save(filename)
        # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
        # сети если был нажат сабмит, либо передадим falsy значения
    return render_template('net.html',form=form,image_name=filename,neurodic=neurodic)

from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json
# метод для обработки запроса от пользователя
@app.route("/apinet",methods=['GET', 'POST'])
def apinet():
    # проверяем что в запросе json данные
    if request.mimetype == 'application/json':
        # получаем json данные
        data = request.get_json()
        # берем содержимое по ключу, где хранится файл
        # закодированный строкой base64
        # декодируем строку в массив байт используя кодировку utf-8
        # первые 128 байт ascii и utf-8 совпадают, потому можно
        filebytes = data['imagebin'].encode('utf-8')
        # декодируем массив байт base64 в исходный файл изображение
        cfile = base64.b64decode(filebytes)
        # чтобы считать изображение как файл из памяти используем BytesIO
        img = Image.open(BytesIO(cfile))
        decode = neuronet.getresult([img])
        neurodic = {}
        for elem in decode:
            neurodic[elem[0][1]] = str(elem[0][2])
            print(elem)
        # пример сохранения переданного файла
        # handle = open('./static/f.png','wb')
        # handle.write(cfile)
        # handle.close()
    # преобразуем словарь в json строку
    ret = json.dumps(neurodic)
    # готовим ответ пользователю
    resp = Response(response=ret,
        status=200,
        mimetype="application/json")
    # возвращаем ответ
    return resp

import lxml.etree as ET
@app.route("/apixml",methods=['GET', 'POST'])
def apixml():
    #парсим xml файл в dom
    dom = ET.parse("./static/xml/file.xml")
    #парсим шаблон в dom
    xslt = ET.parse("./static/xml/file.xslt")
    #получаем трансформер
    transform = ET.XSLT(xslt)
    #преобразуем xml с помощью трансформера xslt
    newhtml = transform(dom)
    #преобразуем из памяти dom в строку, возможно, понадобится указать кодировку
    strfile = ET.tostring(newhtml)
    return strfile

@app.route("/drinks",methods=['GET','POST'])
def drinks():
    dom = ET.parse("./static/xml/drinks.xml")
    type = request.args.get('type')
    if type == 'list':
        xslt = ET.parse("./static/xml/list.xslt")
    elif type == 'table':
        xslt = ET.parse("./static/xml/drinks.xslt")
    else:
        resp = Response(status=500)
        return resp
    transform = ET.XSLT(xslt)
    newhtml = transform(dom)
    strfile = ET.tostring(newhtml)
    return strfile

import picture

@app.route("/picture", methods=['GET','POST'])
def picture():
    pic = False
    if request.method == "POST":
        try:
            os.remove('static/result.jpeg')
            os.remove('static/img.jpeg')
        except FileNotFoundError:
            pass
        string = request.form.get('Base64')
        coef = float(request.form.get('coef'))
           
        pic = picture.convert_to_rgb(string)
        pic = Image.open('static/img.jpeg')
        pic = picture.image_resize(pic, coef)
        pic.save('static/result.jpeg')
    return render_template("picture.html", result = pic)

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
