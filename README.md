## Сделать календарь низких цен на топ 10 направлений на месяц

­

1. Создать кэш направлений и цен на месяц от текущей даты.­
   Направления (ALA - Алматы), (TSE - Астана), (MOW - Москва), (LED - С-Петербург), (CIT - Шымкент):

- ALA - TSE
- TSE - ALA
- ALA - MOW
- MOW - ALA
- ALA - CIT
- CIT - ALA
- TSE - MOW
- MOW - TSE
- TSE - LED
- LED - TSE

Взаимодействие с API:

1. Чтобы получить данные о стоимости перелета необходимо отправить запрос на поиск в систему:

Ссылка на документацию: https://docs.kiwi.com/#flights-flights-get

1. Поиск авиабилетов
   URL: https://api.skypicker.com/flights
   Request type: GET
   Headers:

- Content-Type: application/json

Query состоит из:
Направления: fly_from=IATA_code, fly_to=IATA_code
(пример: ?fly_from=ALA&fly_to=CIT)
Дата: date_from, date_to в формате %d/%m/%Y
Прочие параметры не обязательны.
Пассажиры: adults, children, infants (пример: adults=1&infants=1)

В результате мы получаем json, где нам надо найти самый дешевый перелет среди всех "data" (data > price).
