# Модуль фитнес-трекера

## Описание:

Программный модуль фитнес-трекера, который обрабатывает данные для трёх видов тренировок: бега, спортивной ходьбы и плавания.

Этот модуль выполняет следующие функции:

- принимает от блока датчиков информацию о прошедшей тренировке;  
- определяет вид тренировки;  
- рассчитывает результаты тренировки;  
- выводит информационное сообщение о результатах тренировки.  

Информационное сообщение включает такие данные:  

- тип тренировки (бег, ходьба или плавание);  
- длительность тренировки;  
- дистанция, которую преодолел пользователь, в километрах;  
- средняя скорость на дистанции, в км/ч;  
- расход энергии, в килокалориях.  

### Технологии:
Python 3.7

## Запуск проекта:
Клонировать репозиторий и перейти в директорию проекта:  
git clone https://github.com/bogdanpracticum/fitness-tracker.git;  
cd fitness-tracker

## Cоздать и активировать виртуальное окружение:  
python -m venv venv;  
source venv/Scripts/activate

## Установить зависимости из файла requirements.txt:  
python -m pip install --upgrade pip;  
pip install -r requirements.txt

## Запустить проект:  
python homework.py
