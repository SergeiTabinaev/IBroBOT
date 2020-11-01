from wtforms import Form, StringField, FloatField, SubmitField, IntegerField, TimeField, SelectField




class ShablonForm(Form): #созд шаблона

    title = StringField('Название шаблона')
    TimeFrom = StringField('Время снятия стартовой цены от', default="") #, format='%H:%M'
    TimeTo = StringField('Время снятия стартовой цены до', default="")    # , format='%H:%M'
    triggerStart = FloatField('Триггер для лимита вход +-, %')  #
    triggerStop = FloatField('Триггер для лимита выход по стопу +-, %')  #
    orderStopIV = FloatField('Лимит ордер для выхода по профиту, % к IV')  #
    orderStopObiem = FloatField('Лимит ордер для выхода по профиту, объем в %')  #
    risk = FloatField('Риск на сделку, в %')  #
    timeToClose = StringField('Время авто-закрытия сделок', default="") #, format='%H:%M'

class DealForm(Form):
    tiker = SelectField('Тикер сделки', coerce=int, choices=[
        (0, 'EUR.USD'),
        (1, 'GBP.USD')])
    IVvolativ = FloatField('IV, ожидаемая волативность в %')
    risk = IntegerField('Риск на сделку, в %')
    TimeFrom = StringField('Время снятия стартовой цены от', default="")
    TimeTo = StringField('Время снятия стартовой цены до', default="")
    timeToClose = StringField('Время авто-закрытия сделок', default="")
    triggerStart = FloatField('Триггер для лимита вход +-, %')
    triggerStop = FloatField('Триггер для лимита выход по стопу +-, %')
    sdvigLimit = FloatField('Ограничение сдвига лимита +-,% от IV')
    #сделать отключение верхнего и нижнего триггера
    # trig = SelectField('Trigger', coerce=int, choices=[  # cast val as int
    #     (0, 'Выкл верхний'),
    #     (1, 'Выкл нижний')
    orderStopIV = FloatField('Лимит ордер для выхода по профиту, % к IV')
    orderStopObiem = FloatField('Лимит ордер для выхода по профиту, объем в %')
    BUYorSELL = SelectField('BUYorSELL', coerce=int, choices=[
        (0, 'BUY'),
        (1, 'SELL')])

