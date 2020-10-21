from ibapi import order_condition
from ibapi.client import EClient
from ibapi.order_condition import PriceCondition, OrderCondition
from ibapi.wrapper import EWrapper
import threading
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer
from ibapi.ticktype import TickTypeEnum
# import datetime


# types
from ibapi.common import * # @UnusedWildImport
from ibapi.order_condition import * # @UnusedWildImport
from ibapi.contract import * # @UnusedWildImport
from ibapi.order import * # @UnusedWildImport
from ibapi.order_state import * # @UnusedWildImport
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter
from ibapi.commission_report import CommissionReport
from ibapi.ticktype import * # @UnusedWildImport
from ibapi.tag_value import TagValue

from ibapi.account_summary_tags import *

from samples.ContractSamples import ContractSamples
from samples.OrderSamples import OrderSamples
from samples.AvailableAlgoParams import AvailableAlgoParams
from samples.ScannerSubscriptionSamples import ScannerSubscriptionSamples
from samples.FaAllocationSamples import FaAllocationSamples
from ibapi.scanner import ScanData



class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, " ", errorCode, " ", errorString)


    def tickPrice(self, reqId, tickType, price, attrib):
        # print("TickPrice. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')
        # return price
        if TickTypeEnum.to_str(tickType) == 'BID':
            with open("price.txt", 'w') as file_price:
                file_price.write(str(price))
    #self.reqMarketDataType
    #self.reqMktData

    def contractDetails(self, reqId, contractDetails):
        # print('contractDetails: ', reqId, "", contractDetails)
        pass
    #self.reqContractDetails

    def nextValidId(self, orderId:int):
        self.nextOrderId = orderId
        self.start()

    def orderStatus(self, orderId, status, filled,
                    remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        print('OrderStatus. Id:', orderId, ', Status: ', status, ', Filled', filled,
                    ', Remaining', remaining, ', LastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order,
                  orderState):
        print('OpenOrder. ID:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':',
              order.action, order.orderType, order.totalQuantity,
                  orderState.status)
    #self.placeOrder

    def execDetails(self, reqId, contract, execution):
        print('ExecDetails. ', reqId, contract.symbol, contract.secType, contract.currency,
              execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def start(self):
        contract1 = Contract()

        contract1.symbol = "EUR"  # Контракт на валютную пару EUR.GBP
        contract1.secType = "CASH"
        contract1.currency = "USD"
        contract1.exchange = "IDEALPRO"

        self.reqMarketDataType(4) #if life is not available to switch to delayed-frozen data
        self.reqMktData(1, contract1, '', False, False, [])
        self.reqContractDetails(1, contract1)


        price = open('price.txt', 'r')
        price = price.read()

        order1 = Order()
        order1.action = 'BUY' #SELL
        order1.tif = "GTD"
        order1.goodAfterTime = "20201022 12:31:59"  # util.formatIBDatetime  может   использоваться   для    форматирования даты и    времени.
        order1.goodTillDate = "20201022 14:31:59"
        order1.totalQuantity = 20000 #?????????
        order1.orderType = "LMT"
        order1.lmtPrice = price   #BID price из def tickPrice
        # order1.conditions.append(OrderSamples.TimeCondition("20201022 14:31:59", True, False))
        self.placeOrder(self.nextOrderId, contract1, order1)


    def stop(self):
        self.done = True
        self.disconnect()


def runIB():
    appIB = TestApp()
    appIB.nextOrderId = 0
    appIB.connect('127.0.0.1', 7497, 100)

    #сказать stop() after 3sec. to disconnect
    Timer(3, appIB.stop).start()
    appIB.run()





# done  1.при первом запуске (run) идет только подключение к TWS
# done  2.далее проверка есть ли в списке задач, задача с подходящи временем
# если время подходящее то идет запуск задачи по покупке или продаже тикера по "стартовой цене"


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
















