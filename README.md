## Приложение является веб-сервисом, реализованным на Python с использованием фреймворка FastAPI. Оно асинхронно взаимодействует с базой данных PostgreSQL посредством SQLAlchemy. Приложение развернуто с помощью Docker и docker-compose на базе сервера Unicorn.

### Функциональность приложения включает в себя следующее:

1. Развёртывание Приложения и СУБД с помощью Docker: В репозитории предоставлены файлы `docker-compose.yml` и `Docker` для создания контейнеров с PostgreSQL и Приложением. Docker-compose позволяет легко настроить и запустить базу данных (миграции осущетвляются с помощью alembic), определить volume для хранения файлов СУБД на хост-машине, а также запустить FastAPI приложение на базе серевера Unicorn

2. POST REST метод: Веб-сервис реализует POST метод, который принимает запросы с содержимым в формате JSON, где указывается количество вопросов (`{"questions_num":integer}`). После получения запроса, сервис отправляет запросы на публичное API jService.io, чтобы получить указанное количество случайных уникальных англоязычных вопросов для викторин. Полученные ответы сохраняются в базе данных PostgreSQL.

3. Сохранение информации о вопросах: Для каждого вопроса в запросе, сохраняется следующая информация: ID вопроса, текст вопроса, текст ответа и дата создания вопроса, номер запроса. SQLAlchemy используется для асинронного взаимодействия с базой данных. Валидация данных получаемых и возвращаемых в POST методе реализована через определение моделей данных (Schemas).

4. Уникальные вопросы: При сохранении нового вопроса, приложение проверяет наличие такого же вопроса в базе данных. Если такой вопрос уже существует, то приложение отправляет дополнительные запросы к публичному API до тех пор, пока не будет получен уникальный вопрос для викторины.

5. Ответ на запрос: В случае, если база данных не пуста, приложение возвращает данные предыдущего сохранённого запроса. В противном случае, ответ содержит пустой список.

-----------------------------

### Требования:
* OS: Linux или LinuxVirtualMachine (приложение написано под OS Linux)
* Docker (развёртывание и запуск осуществляется с помощью docker-compose)



### Запуск приложения на хост-машине
1. Скачать репозиторий


2. [Необязательно] Изменить конфигурацию подключения базы данных:
  - файл `.env` содержит параметры подключения к БД.

  - в файле `docker-compose.yml` определяется начальная конфигурация БД.

3. В терминале перейти в директорию приложения с файлом `docker-compose.yml`
   

    ```
    cd path/to/project/dir
4. Используя Docker, запустить сборку и развёртывание приложения:
  - для запуска в режиме detached mode:


    ```
    docker-compose up -d --build
  - для запуска с выводом логов:


    ```
    docker-compose up --build

-----------------------------

### Доступ к приложению:
Доступ к API приложению на локальной машине реализован по адресу:
    
    
    0.0.0.0:8000/question

Взаимодействие с приложением посредством веб-интерфейса возможно по адресу:


    0.0.0.0:8000/docs
