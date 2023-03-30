# api_yamdb
api_yamdb
## Описание
Проект YaMDb собирает отзывы пользователей на различные произведения.
## Установка
1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone
```
2. Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
3. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python manage.py migrate
```
5. Запустить проект:
```
python manage.py runserver
```
## Примеры
### Категории произведений
   - Запросы: GET, POST, DELETE
```
{
  "name": "string",
  "slug": "string"
}
```
### Категории жанров
   - Запросы: GET, POST, DELETE
```
{
"name": "string",
"slug": "string"
}
```
### Произведения
   - Запросы: GET, POST, PATCH, DELETE
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
### Отзывы
   - Запросы: GET, POST, PATCH, DELETE
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
### Комментарии к отзывам
   - Запросы: GET, POST, PACTH, DELETE
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```