from app import db
import re
from sqlalchemy import Column, String, Integer, DateTime, Time, Float
from datetime import datetime
# timestamp = datetime.today().timestamp()
# print(timestamp)


def slugify(s):  # принимает title и создает имя для слага
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class Shablon(db.Model):   # модель шаблона для заполнения новой сделки.
    __tablename__ = 'Smit_Shablon'

    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    slug = Column(String(140), unique=True)  # типа айди каждого сохраненного шаблона для заполнения
    TimeFrom = Column(String, nullable=False, default=None) # Время снятия стартовой цены от , blank=True
    TimeTo = Column(String, nullable=False, default=None) # Время снятия стартовой цены до
    triggerStart = Column(Float, nullable=False, default=None)  # Триггер для лимита вход +-, %
    triggerStop = Column(Float, nullable=False, default=None)  # Триггер для лимита выход по стопу +-, %
    orderStopIV = Column(Float, nullable=False, default=None)  # Лимит ордер для выхода по профиту, % к IV
    orderStopObiem = Column(Float, nullable=False, default=None)  # Лимит ордер для выхода по профиту, объем в %
    risk = Column(Float, nullable=False, default=None)  # Риск на сделку, в %
    # timeToClose = Column(Time, nullable=False)  # Время авто-закрытия сделок
    timeToClose = Column(String, nullable=False, default=None)


    def __init__(self, *args, **kwargs):   #  конструктор класса. args-список позиц-х аргументов kwargs-словарь именнов-х аргументов
        super(Shablon, self).__init__(*args, **kwargs)   # super(Shablon) вызов конструктора класа предка. предок-classМodel
        self.generate_slug()


    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)


    def __repr__(self):
        return 'Shablon id: {}, title: {}'.format(self.id, self.title)



