import multiprocessing
import sys
import os

from threading import Timer
from multiprocessing import Process


from app import app
from flask import render_template, Flask
from models import Shablon
from forms import ShablonForm, DealForm
from flask import request
from app import db
from flask import redirect
from flask import url_for
import traceback
import json
import importlib
import IB




@app.route('/') #главная страница со списком сделок(портфель)...добавить интерфейсное окно Логов?????????????
def index():
    return render_template('index.html')

@app.route('/log')
def get_console_handler():
    trace = open('mylog.txt', 'r', encoding="utf-8")
    return render_template('intro.html', title="Лог", trace=trace.read())




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


@app.route('/add', methods=["POST", "GET"]) #добавление записей(сделок) в портфель
def add_deal():
    if request.method == 'POST':
        # TestApp.tiker = request.form['tiker']
        dictForm = {}
        vtiker = request.form['tiker']
        dictForm['tiker']=vtiker
        vIVvolativ = request.form['IVvolativ']
        dictForm['IVvolativ'] = vIVvolativ
        vriskTrade = request.form['risk']
        dictForm['riskTrade'] = vriskTrade
        vgoodAfterTime = request.form['TimeFrom']
        dictForm['goodAfterTime'] = vgoodAfterTime
        vgoodTillDate = request.form['TimeTo']
        dictForm['goodTillDate'] = vgoodTillDate
        vtimeToClose = request.form['timeToClose'] #?????????????
        dictForm['timeToClose'] = vtimeToClose
        ventryTrigger = request.form['triggerStart']
        dictForm['entryTrigger'] = ventryTrigger
        vexitTrigger = request.form['triggerStop']
        dictForm['exitTrigger'] = vexitTrigger
        vsdvigLimit = request.form['sdvigLimit'] #?????????????
        dictForm['sdvigLimit'] = vsdvigLimit
        vorderStopIV = request.form['orderStopIV'] #?????????????
        dictForm['orderStopIV'] = vorderStopIV
        vorderStopObiem = request.form['orderStopObiem'] #?????????????
        dictForm['orderStopObiem'] = vorderStopObiem
        vBUYorSELL = request.form['BUYorSELL']
        dictForm['BUYorSELL'] = vBUYorSELL
        with open("fileForm.json", 'w') as file_form:
            json.dump(dictForm, file_form, indent=2, ensure_ascii=False)

        # importlib.reload(IB) #перезагрузка модуля IB для записи новой сделки
        appIB = IB.TestApp()
        appIB.nextOrderId = 0
        appIB.connect('127.0.0.1', 7497, 100)

        Timer(3, appIB.stop).start()
        appIB.run()


        return render_template('index.html', tiker=vtiker, BUYorSELL=vBUYorSELL, IVvolativ=vIVvolativ,
                           goodAfterTime=vgoodAfterTime,
                           goodTillDate=vgoodTillDate)
    form = DealForm()
    return render_template('add_deal.html', form=form)

