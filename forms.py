from wtforms import Form, StringField, IntegerField, TimeField
from wtforms.validators import NumberRange


class ShablonForm(Form): #созд шаблона

    title = StringField('Название шаблона')
    TimeFrom = StringField('Время снятия стартовой цены от', default="") #, format='%H:%M'
    TimeTo = StringField('Время снятия стартовой цены до', default="")    # , format='%H:%M'
    triggerStart = IntegerField('Триггер для лимита вход +-, %')  #
    triggerStop = IntegerField('Триггер для лимита выход по стопу +-, %')  #
    orderStopIV = IntegerField('Лимит ордер для выхода по профиту, % к IV')  #
    orderStopObiem = IntegerField('Лимит ордер для выхода по профиту, объем в %')  #
    risk = IntegerField('Риск на сделку, в %')  #
    timeToClose = StringField('Время авто-закрытия сделок', default="") #, format='%H:%M'
