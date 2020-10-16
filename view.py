from app import app
from flask import render_template
from models import Shablon
from forms import ShablonForm
from flask import request
from app import db
from flask import redirect
from flask import url_for
import traceback


@app.route('/') #главная страница со списком сделок(портфель)...добавить интерфейсное окно Логов?????????????
def index():
    return render_template('index.html')


@app.route('/settings', methods=["POST", "GET"]) #страница создания шаблонов и выбора существующих
def create_shablon():
    if request.method == 'POST':
        title = request.form['title']
        TimeFrom = request.form['TimeFrom']
        TimeTo = request.form['TimeTo']
        triggerStart = request.form['triggerStart']
        triggerStop = request.form['triggerStop']
        orderStopIV = request.form['orderStopIV']
        orderStopObiem = request.form['orderStopObiem']
        risk = request.form['risk']
        timeToClose = request.form['timeToClose']

        try:
            db.session.rollback()
            shablon = Shablon(title=title,
                              TimeFrom=TimeFrom,
                              TimeTo=TimeTo,
                              triggerStart=triggerStart,
                              triggerStop=triggerStop,
                              orderStopIV=orderStopIV,
                              orderStopObiem=orderStopObiem,
                              risk=risk,
                              timeToClose=timeToClose)
            db.session.add(shablon)
            db.session.commit()
        except Exception:
            traceback.print_exc()
        return redirect(url_for('create_shablon'))
    form = ShablonForm()
    shablons = Shablon.query.all()
    return render_template('choice_shablona.html', form=form, shablons=shablons)


@app.route('/delete/<slug>/', methods=['POST'])
def remove(slug):
    db.session.rollback()
    shablon = Shablon.query.filter_by(slug=slug).first()
    db.session.delete(shablon)
    db.session.commit()
    return redirect(url_for('create_shablon'))


@app.route('/settings/<slug>') #страница сохранненого шаблона
def shablon_detail(slug):
    shablon = Shablon.query.filter(Shablon.slug==slug).first()
    return render_template('shablon_detail.html', shablon=shablon)



@app.route('/add') #добавление записей(сделок) в портфель
def add_deal():
    return render_template('add_deal.html')


@app.route('/test')
def test():
    return render_template('test_template.html')
