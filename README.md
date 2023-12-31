# Day 04 – REST API
## Оглавление
1. [Глава I](#глава-i) \
    1.1. [Преамбула](#преамбула)
2. [Глава II](#глава-ii) \
    2.1. [Общая инструкция](#общая-инструкция)
3. [Глава III](#глава-iii) \
    3.1. [Цели](#цели) 
4. [Глава IV](#глава-iv) \
    4.1. [Задание](#задание)
5. [Глава V](#глава-v) \
    5.1. [Сдача работы и проверка](#сдача-работы-и-проверка)

## Глава I
### Преамбула
У любого сервиса есть интерфейс взаимодействия. Как правило, при таком словосочетании нам приходят на ум какие-то формы, 
кнопки, дизайн, стрелки, выпадающее меню. Но это только один из видов интерфейса, и он абсолютно не приспособлен 
для ситуаций, когда нам нужно что-то автоматизировать. 
<img src="misc/images/rest-api.png">

Для таких случаев есть API — программный интерфейс приложения. 
При помощи него мы можем взаимодействовать с сервисом при помощи кода, и сервис будет совершать те же действия, 
что и в стандартном, например, drag-and-drop интерфейсе. 

Умения работать с API дает возможность:
* Получать доступ к большому количеству данных из различных источников, \
что может быть полезно для анализа и моделирования.
* Автоматизировать процесс сбора и обработки данных, что позволяет экономить время и улучшать качество работы.
* Интегрировать свои аналитические решения с другими приложениями и системами.
* И конечно же использовать API для создания собственных приложений и сервисов, основанных на данных.

Последние 2 возможности в этом проекте мы и испробуем.

## Глава II
### Общая инструкция

Методология Школы 21 может быть не похожа на тот образовательный опыт, который случался с тобой ранее. Её отличает высокий уровень автономии: у тебя есть задача, ты должен её выполнить. По большей части тебе нужно будет самому добывать знания для её решения. Второй важный момент — это peer-to-peer обучение. В образовательном процессе нет менторов и экспертов, перед которыми ты защищаешь свой результат. Ты это делаешь перед таким же учащимися, как и ты сам. У них есть чек-лист, который поможет им качественно выполнить приемку вашей работы.

Роль Школы 21 заключается в том, чтобы обеспечить через последовательность заданий и оптимальный уровень поддержки такую траекторию обучения, при которой ты не только освоишь hard skills, но и научишься самообучаться.

- Не доверяй слухам и предположениям о том, как должно быть оформлено ваше решение. Этот документ является единственным источником, к которому стоит обращаться по большинству вопросов;
- твое решение будет оцениваться другими учащимися;
- подлежат оцениванию только те файлы, которые ты выложил в GIT (ветка develop, папка src);
- в твоей папке не должно быть лишних файлов — только те, что были указаны в задании;
- не забывай, что у вас есть доступ к интернету и поисковым системам;
- обсуждение заданий можно вести и в Rocket.Chat;
- будь внимателен к примерам, указанным в этом документе — они могут иметь важные детали, которые не были оговорены другим способом;
- и да пребудет с тобой Сила!

## Глава III
### Цели
Этот проект отличается от предыдущих тем, что представлен не в виде набора упражнений, а в форме целостной настоящей 
командной задачи. Здесь важно не только, чтобы был написан код, но и чтобы всё было интегрировано и работало. Будет интересно!

## Глава IV
### Задание
В этом проекте вы будете взаимодействовать с внешними сервисами. Нужно сделать следующее:

### Task 1
Командой выберите любой бесплатный API в сети. Примеры по [ссылке](https://habr.com/ru/company/macloud/blog/562700). 
Требование одно: чтобы API вам нравился, и вам было интересно с ним работать. 

### Task 2
Напишите класс взаимодействия с API, а в рамках класса методы взаимодействия с ним.
Пример реализации на основе [API Numbers](http://numbersapi.com/) можно посмотреть [тут](code-samples/numbers.py). 
Чем сложнее функционал, тем круче результат. Вы никак не ограничены в своей фантазии :)

### Task 3
После реализации и проверки функциональности напишите небольшой сервис на Flask, FastAPI, или телеграм-бота.
Нужно, чтобы каждый мог пользоваться функциональностью, которую вы заложили в свой сервис.

### Task 4
Запустите ваш сервис во время проверки, чтобы проверяющий мог оценить функционал:)

Будет круто, если у вас получится запустить ваш сервис на каком-либо веб-хостинге. 

## Глава V
### Сдача работы и проверка
1. Сохраните все файлы, которые вам понадобились для запуска сервиса, в папку src.
2. Напишите инструкцию в файл instruction.md. Опишите, как именно работает ваш сервис, и как его можно проверить. 
Файл также поместите в папку src.
3. Загрузите все материалы на Git в ветку develop.

💡 [Нажми здесь](https://forms.gle/eiSnmYd844JkmYbF7) **чтобы отправить обратную связь по проекту**. 
