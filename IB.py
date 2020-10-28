import os

from flask import request
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import threading
from threading import Timer
from ibapi.ticktype import TickTypeEnum
import datetime
import json

# types
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import * # @UnusedWildImport
from ibapi.ticktype import * # @UnusedWildImport
# from view import vtiker, vIVvolativ, vriskTrade, vgoodAfterTime, vgoodTillDate, vtimeToClose, ventryTrigger, vexitTrigger, vsdvigLimit, vorderStopIV, vorderStopObiem




# buyTrigger. триггер на покупку
# dropAssets. ликвидационные активы. (например 1000000)
# IVvolativ. IV-ожидаемая волатильность %. (например 0.08% eur-usd от0до55 %)
# riskTrade. Риск на сделку. (например 0.03%)
# entryTrigger. Триггер для лимита входа -+%. (например 0.0000001%)
# exitTrigger. Триггер лимита выхода по стопу -+%.  (например 10%)


#триггер на покупку = первичная цена + (первичная цена * IVожидаемая волативность * триггер лимита на вход%)
# buyTrigger = price + (price * IVvolativ * entryTrigger)

# объем ордера = ликвидационные активы * риск на сделку / триггер на покупку * триггер для лимита выход по стопу * IVожидаемая волативность
# 10000 * 0,003 / 20 * 10% * 55% = 240акций
# MyTotalQuantity = dropAssets * riskTrade / buyTrigger * exitTrigger * IVvolativ




class TestApp(EWrapper, EClient):


    # dictForm0 = {'tiker': '', 'IVvolativ': float(),
    #     'riskTrade': float(), 'goodAfterTime': '',
    #     'goodTillDate': '', 'timeToClose': '',
    #     'entryTrigger': float(), 'exitTrigger': float(),
    #     'sdvigLimit': float(), 'orderStopIV': float(), 'orderStopObiem': float()}
    # with open("fileForm.json", 'w') as file_form:
    #     json.dump(dictForm0, file_form, indent=2, ensure_ascii=False)

    try: #таймер ниже по коду очищает fileForm.json(данные для новой записи) чтоб при запуске не было отправки старой записи
        with open("fileForm.json", 'r') as file_form:
            dictForm = json.load(file_form)
    except: #чтоб не выдавало ошибку пустого fileForm.json(данные для новой записи), создаем пустой словарь
        dictForm = {'tiker': '', 'IVvolativ': float(),
            'riskTrade': float(), 'goodAfterTime': '',
            'goodTillDate': '', 'timeToClose': '',
            'entryTrigger': float(), 'exitTrigger': float(),
            'sdvigLimit': float(), 'orderStopIV': float(), 'orderStopObiem': float()}
        with open("fileForm.json", 'w') as file_form:
            json.dump(dictForm, file_form, indent=2, ensure_ascii=False)

    pricer = open('price.txt', 'r')
    price = float(pricer.read())  # bid or ask price from def tickPrice
    tiker = dictForm['tiker']
    print(tiker)
    IVvolativ = float(dictForm['IVvolativ']) #0.08
    entryTrigger = float(dictForm['entryTrigger']) #0.0000001
    dropAssets = 1000000
    riskTrade = float(dictForm['riskTrade']) #0.03
    exitTrigger = float(dictForm['exitTrigger']) #10
    buyTrigger = price + (price * IVvolativ * entryTrigger)
    buyTrigger = round(buyTrigger, 5)
    if buyTrigger != 0:
        if exitTrigger != 0:
            if IVvolativ != 0:
                MyTotalQuantity = int((dropAssets * riskTrade) / (buyTrigger * exitTrigger * IVvolativ))
    goodAfterTime = dictForm['goodAfterTime'] #"20201026 12:31:59"
    goodTillDate = dictForm['goodTillDate'] #"20201026 14:31:59"

    file_log = open("mylog.txt", 'a')
    # file_error = open("checkError.json", 'w')

    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        self.file_log.writelines(errorString + '\n' + '<br />')
        # json.dump(errorCode, self.file_error, indent=2, ensure_ascii=False)
        print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
        # print("TickPrice. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')
        if TickTypeEnum.to_str(tickType) == 'ASK':
            with open("price.txt", 'w') as file_price:
                file_price.write(str(price))
    #self.reqMarketDataType
    #self.reqMktData

    def nextValidId(self, orderId:int):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId, status, filled, remaining,
                    avgFillPrice, permId, parentId, lastFillPrice,
                    clientId, whyHeld, mktCapPrice):
        self.file_log.writelines(status + '\n' + '<br />')
        print('OrderStatus. Id:', orderId, ', Status: ', status, ', Filled', filled,
              ', Remaining', remaining, ', LastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        self.file_log.writelines(order.action + '\n' + '<br />')
        print('OpenOrder. ID:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':',
              order.action, order.orderType, order.totalQuantity, orderState.status)
    #self.placeOrder

    def execDetails(self, reqId, contract, execution):
        print('ExecDetails. ', reqId, contract.symbol, contract.secType, contract.currency,
              execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        contract1 = Contract()

        contract1.symbol = "EUR"
        contract1.secType = "CASH"
        contract1.currency = "USD"
        contract1.exchange = "IDEALPRO"

        self.reqMarketDataType(4) #if life is not available to switch to delayed-frozen data
        self.reqMktData(1, contract1, '', False, False, [])

        # with open("checkError.json", "r") as me:
        #     myError = str(json.load(me))
        # if myError.__contains__('110') == True:
        #     print(myError)


        #price = self.price #float(price.read())
        buyTrigger = self.buyTrigger #price + (price * self.IVvolativ * self.entryTrigger)
        buyTrigger = round(buyTrigger, 5)
        MyTotalQuantity = self.MyTotalQuantity #int((self.dropAssets * self.riskTrade) / (buyTrigger * self.exitTrigger * self.IVvolativ))

        print(buyTrigger)
        print(MyTotalQuantity)

        order1 = Order()
        order1.action = 'BUY' #SELL
        order1.tif = "GTD"
        order1.goodAfterTime = self.goodAfterTime #"20201024 12:31:59"  # util.formatIBDatetime  can be using for  форматирования даты и    времени.
        order1.goodTillDate = self.goodTillDate #"20201024 14:31:59"
        order1.totalQuantity = MyTotalQuantity #20000
        order1.orderType = "LMT"
        order1.lmtPrice = buyTrigger #BID price из def tickPrice
        self.placeOrder(self.nextOrderId, contract1, order1)


    def stop(self):
        self.done = True
        self.disconnect()

    def timerDel(self):
        with open('fileForm.json', 'wb'):
            pass


def runIB():
    appIB = TestApp()
    appIB.nextOrderId = 0
    appIB.connect('127.0.0.1', 7497, 100)
    Timer(2, appIB.timerDel).start()
    #сказать stop() after 3sec. to disconnect
    Timer(3, appIB.stop).start()
    appIB.run()

# def onlyConnect():
#     wrp = EWrapper()
#     cln = EClient(wrp)
#     cln.connect("127.0.0.1", 7497, 100)
#
#     if cln.isConnected():
#         print("Успешно подключились к TWS")
#         cln.th = threading.Thread(target=cln.run)
#         cln.th.start()
#         cln.th.join(timeout=5)





# done  1.при первом запуске (run) идет только подключение к TWS
# done  2.далее проверка есть ли в списке задач, задача с подходящи временем
#         если время подходящее то идет запуск задачи по покупке или продаже тикера по "стартовой цене"
# ордера на покупку (тригер на покупку)


# Основное описание бота:
# Бот совершает покупку\продажу при выходе из указанного диапазона цены в указанное время с установкой защитных стоп-приказов, приказов по фиксации прибыли и закрытием основной сделки в указанное время по рыночной цене.
# 
# С каждым тикером(записью) можно производить ряд действий:
# запустить, остановить, изменить - корректировка – (стоп, профит(тейк) уровней.)
# 
# 0. Выбор профиля счетов
# 
# 1. Тикер
# 2. IV-ожидаемая волатильность
# 3. Риск на сделку
# 4. время снятия стартовой цены
# 5. время авто-закрытия сделок
# 6. Триггер для лимита входа -+%
# 7. Ограничение сдвига лимита -+, % от IV
# 8.  Отключение верхнего и нижнего триггера (чек боксы)
# 9. Триггер лимита выхода по стопу -+%
# 10. лимит ордер для выхода по профиту (тейк профит) % к IV
# 11. Лимит ордер для выхода по профиту, объём в %(объем к предыдущему параметру, на ордер)
# 
# Более детальный алгоритм работы бота:
# Для работы бота нужно внести записи (тикер, iv и т.д.), за которой бот будет следить. Ввод возможен полностью в ручном режиме либо с использованием шаблона для ускорения (заполнения части полей по шаблону).
# При запуске бота:
# 1 – проверка времени снятия первичной цены. Как только указанное время соответствует текущему времени записываем «стартовую цену» - берем ее как торговая сделка. (в API разные цены есть, аск\бид ласт и т.д.)
# 2- считаем Триггер для лимитного ордера входа и размещаем приказ. 
# Для ордера на покупку (тригер на покупку) - «первичная цена» + («первичная цена» * «IV ожидаемая волатильность»*триггер для лимита вход % )
# В случае если цена касается цены триггера размещаем лимитный ордер lmt
# «первичная цена» + («первичная цена» * «IV ожидаемая волатильность» *1.03 – тип ордера lmt(Limit) с параметрами срабатывания в не торговой сессии. 
# Объем ордера считается по формуле: ликвидационные активы * «Риск на сделку»  / (Триггер на покупку) * Триггер для лимита выход по стопу * IV 
# Пример
# 100 000 * 0,03 = 3000 / 20*10%*55%=2400 акций
# 
# Проверяем сработал ли ордер, если ордер не сработал модифицируем ордер двигая его к аск:
# Новый лимит ордер = Аск*1,03 
#  и проверяем находимся ли мы в лимите возможного изменения – параметр, указанный в создании записи «Ограничение сдвига лимита -+ % от IV»
# то есть размещаемый ордер на покупку будет иметь ограничения изменения вверх после срабатывания триггера.
# Считать как = «первичная цена» + («первичная цена» * «IV ожидаемая волатильность» * ограничение сдвига лимита)
# Для ордера на продажу (тригер на продажу) - «первичная цена» - («первичная цена» * «IV ожидаемая волатильность» *триггер для лимита вход %)
# В случае если цена касается цены триггера размещаем лимитный ордер lmt
# «первичная цена» - («первичная цена» * «IV ожидаемая волатильность» *0.97 – тип ордера lmt(Limit) с параметрами срабатывания в не торговой сессии. 
# Объем ордера считается по формуле: ликвидационные активы * «Риск на сделку»  / (Тригер на продажу) * Тригер для лимита выход по стопу * IV 
# Проверяем сработал ли ордер, если ордер не сработал модифицируем ордер двигая его к бид пока не выполнится весь:
# Новый лимит ордер = бид*0,97
# и проверяем находимся ли мы в лимите возможного изменения – параметр, указанный в создании записи «Ограничение сдвига лимита -+ % от IV»
# то есть размещаемый ордер на продажу будет иметь ограничения изменения вниз после срабатывания триггера.
# Считать как = «первичная цена» - («первичная цена» * «IV ожидаемая волатильность» * ограничение сдвига лимита)
# Размещение лимита для выхода по профиту (тейк профит)
# после срабатывания ордера покупка/продажа размещаем тей профит:
# после покупки – ордер лимитный на продажу – «первичная цена» + («первичная цена» * лимит ордер для выхода по профиту* IV-ожидаемая волатильность)
# Объем ставим из «Лимит ордер для выхода по профиту, объём в %» = имеющийся объем * Лимит ордер для выхода по профиту, объём в %»
# После продажи – ордер лимитный на покупку - «первичная цена» - («первичная цена» * лимит ордер для выхода по профиту * IV-ожидаемая волатильность)
# Объем ставим из «Лимит ордер для выхода по профиту, объём в %» = имеющийся объем * Лимит ордер для выхода по профиту, объём в %»
# Размещение ордера стоп
# после срабатывания ордера покупка/продажа размещаем стоп ордер:
# при покупке размещаем ордер на продажу, тип стоп ордер = «первичная цена» - («первичная цена»* Триггер лимита выхода по стопу * IV-ожидаемая волатильность)
# при продаже размещаем ордер на покупку, тип стоп ордер = «первичная цена» + («первичная цена»* Триггер лимита выхода по стопу * IV-ожидаемая волатильность)
# Слежение за авто-закрытием сделок
# как только наступает время «время авто-закрытия сделок» размещается приказ на закрытие имеющихся сделок:
# на покупки – размещается приказ продать по рынку метод pctcange -100% чтоб закрыть 100% имеющегося объема
# на продажу – размещается приказ купить по рынку метод pctcange -100% чтоб закрыть 100% имеющегося объема
















