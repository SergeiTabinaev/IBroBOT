# IBroBOT

1)сделана заготовка фронта
2)сделана логика выставления ордера покупки и продажи через интерфейс
3)сделана логика выставления стоп-лосс и профит 
4)также осталось сделать логику повторного выставления ордеров при проскальзывании


Описание бота(тестовое задание):

Написать Бота нужно на API Python
Для работы документация http://interactivebrokers.github.io/tws-api/
Для подключения к API с сайта IB нужно сказать демо терминал https://www.interactivebrokers.co.uk/ru/index.php?f=20369&invd=T
Демо – не сможет работать с акциями в API так как нет подписки не поставку данных. Для работы бота можно использовать валюты
Eur.usd
gbp.usd
aud.usd

Основное описание бота:
Бот совершает покупку\продажу при выходе из указанного диапазона цены в указанное время с установкой защитных стоп-приказов, приказов по фиксации прибыли и закрытием основной сделки в указанное время по рыночной цене.
Имеет интерфейс – для занесения шаблонных настроек 
и управления компаниями(записями) с которыми ведется работа.

Визуальная часть(она может быть такой как на скринах, может быть другой – важен функционал):


В основном окне можно добавить акцию(запись) – тикер – через шаблон или полностью в ручном режиме с которой будет работать бот. В текущем примере 6 акций с которыми будет проводиться работа алгоритмом. 

С каждым тикером(записью) можно производить ряд действий:
запустить, остановить, изменить - корректировка – (стоп, профит(тейк) уровней.)



Настройка шаблона переменных – для создания тикера

Создание тикера на основе шаблона -



Основные переменные в шаблоне:
1. Время снятия стартовой цены от хх до хх
2. Триггер для лимита ВХОД -+,%
2.1 Ограничение сдвига лимита -+ % от IV
3. Триггер для ВЫХОДА по стопу +-,%
4. Лимит ордер для выхода по Профиту % к IV 
5. Лимит ордер для выхода по профиту, объем в %
6. Риск на сделку %

Основные параметры при добавлении записи:

0. Выбор профиля счетов

1. Тикер
2. IV-ожидаемая волатильность
3. Риск на сделку
4. время снятия стартовой цены
5. время авто-закрытия сделок
6. Триггер для лимита входа -+%
7. Ограничение сдвига лимита -+, % от IV
8.  Отключение верхнего и нижнего триггера (чек боксы)
9. Триггер лимита выхода по стопу -+%
10. лимит ордер для выхода по профиту (тейк профит) % к IV
11. Лимит ордер для выхода по профиту, объём в %(объем к предыдущему параметру, на ордер)

Более детальный алгоритм работы бота:
Для работы бота нужно внести записи (тикер, iv и т.д.), за которой бот будет следить. Ввод возможен полностью в ручном режиме либо с использованием шаблона для ускорения (заполнения части полей по шаблону).
При запуске бота:
1 – проверка времени снятия первичной цены. Как только указанное время соответствует текущему времени записываем «стартовую цену» - берем ее как торговая сделка. (в API разные цены есть, аск\бид ласт и т.д.)
2- считаем Триггер для лимитного ордера входа и размещаем приказ. 
Для ордера на покупку (тригер на покупку) - «первичная цена» + («первичная цена» * «IV ожидаемая волатильность»*триггер для лимита вход % )
В случае если цена касается цены триггера размещаем лимитный ордер lmt
«первичная цена» + («первичная цена» * «IV ожидаемая волатильность» *1.03 – тип ордера lmt(Limit) с параметрами срабатывания в не торговой сессии. 
Объем ордера считается по формуле: ликвидационные активы * «Риск на сделку»  / (Триггер на покупку) * Триггер для лимита выход по стопу * IV 
Пример
100 000 * 0,03 = 3000 / 20*10%*55%=2400 акций

Проверяем сработал ли ордер, если ордер не сработал модифицируем ордер двигая его к аск:
Новый лимит ордер = Аск*1,03 
 и проверяем находимся ли мы в лимите возможного изменения – параметр, указанный в создании записи «Ограничение сдвига лимита -+ % от IV»
то есть размещаемый ордер на покупку будет иметь ограничения изменения вверх после срабатывания триггера.
Считать как = «первичная цена» + («первичная цена» * «IV ожидаемая волатильность» * ограничение сдвига лимита)
Для ордера на продажу (тригер на продажу) - «первичная цена» - («первичная цена» * «IV ожидаемая волатильность» *триггер для лимита вход %)
В случае если цена касается цены триггера размещаем лимитный ордер lmt
«первичная цена» - («первичная цена» * «IV ожидаемая волатильность» *0.97 – тип ордера lmt(Limit) с параметрами срабатывания в не торговой сессии. 
Объем ордера считается по формуле: ликвидационные активы * «Риск на сделку»  / (Тригер на продажу) * Тригер для лимита выход по стопу * IV 
Проверяем сработал ли ордер, если ордер не сработал модифицируем ордер двигая его к бид пока не выполнится весь:
Новый лимит ордер = бид*0,97
и проверяем находимся ли мы в лимите возможного изменения – параметр, указанный в создании записи «Ограничение сдвига лимита -+ % от IV»
то есть размещаемый ордер на продажу будет иметь ограничения изменения вниз после срабатывания триггера.
Считать как = «первичная цена» - («первичная цена» * «IV ожидаемая волатильность» * ограничение сдвига лимита)
Размещение лимита для выхода по профиту (тейк профит)
после срабатывания ордера покупка/продажа размещаем тей профит:
после покупки – ордер лимитный на продажу – «первичная цена» + («первичная цена» * лимит ордер для выхода по профиту* IV-ожидаемая волатильность)
Объем ставим из «Лимит ордер для выхода по профиту, объём в %» = имеющийся объем * Лимит ордер для выхода по профиту, объём в %»
После продажи – ордер лимитный на покупку - «первичная цена» - («первичная цена» * лимит ордер для выхода по профиту * IV-ожидаемая волатильность)
Объем ставим из «Лимит ордер для выхода по профиту, объём в %» = имеющийся объем * Лимит ордер для выхода по профиту, объём в %»
Размещение ордера стоп
после срабатывания ордера покупка/продажа размещаем стоп ордер:
при покупке размещаем ордер на продажу, тип стоп ордер = «первичная цена» - («первичная цена»* Триггер лимита выхода по стопу * IV-ожидаемая волатильность)
при продаже размещаем ордер на покупку, тип стоп ордер = «первичная цена» + («первичная цена»* Триггер лимита выхода по стопу * IV-ожидаемая волатильность)
Слежение за авто-закрытием сделок
как только наступает время «время авто-закрытия сделок» размещается приказ на закрытие имеющихся сделок:
на покупки – размещается приказ продать по рынку метод pctcange -100% чтоб закрыть 100% имеющегося объема
на продажу – размещается приказ купить по рынку метод pctcange -100% чтоб закрыть 100% имеющегося объема
