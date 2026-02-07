# donstuAPI

API для работы с <a href="edu.donstu.ru">edu.donstu.ru</a>


<h2>Авторизация</h2>

```python
from donstuapi import DonstuAPI

donstu = DonstuAPI()
donstu.auth(
    username="username",
    password="password"
)

```

<h2>Доступные методы</h2>
<h3>Работа с аккаунтом</h3>

`account.info` Получение информации об аккаунте <br>
`account.feed()` Получение уведомлений <br>
`account.payments()` Получение информации об оплатах <br>
`account.statistics_marks_count()` Получение статистики оценок за семестр <br>
`account.get_important_message()` Получение важных сообщений

<h3>Работа с журналом</h3>

`journal.list` Получение списка дисциплин
`journal.`