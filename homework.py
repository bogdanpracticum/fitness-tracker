from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str    # Название тренировки
    duration: float       # Длительность (в часах)
    distance: float       # Дистанция в (в км)
    speed: float          # Скорость (в км/ч)
    calories: float       # Килокалории

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки.
    Содержит все основные свойства и методы для тренировок.

    Входные переменные:
    - action - количество совершённых действий
    - duration - длительность тренировки
    - weight - вес спортсмена
    """

    # расстояние, которое спортсмен преодолевает
    LEN_STEP = 0.65
    # константа для перевода значений из метров в километры.
    M_IN_KM = 1000
    # константа для перевода времени.
    MIN_IN_H = 60

    action: int      # Количество шагов/гребков
    duration: float  # Продолжительность тренировки
    weight: float    # Вес спортсмена

    def get_distance(self) -> float:
        """Получить дистанцию в км. Которую преодолел пользователь
        за время тренировки."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        # преодоленная_дистанция_за_тренировку / время_тренировки
        # возвращает значение средней скорости движения во время тренировки
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # метод определяется в дочерних классах, расчет калорий отличается
        # в зависимости от тренировки
        raise NotImplementedError("Требуется определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    action: int
    duration: float
    weight: float

    # Получить дистанцию в КМ
    def get_distance(self) -> float:
        return super().get_distance()

    # Получить среднюю скорость движения
    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    # Получить количество затраченных калорий
    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                          / self.M_IN_KM * self.duration * self.MIN_IN_H)
        return spent_calories

    # Вернуть сообщение о выполненной тренировке
    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    Дополнительный параметр height — рост спортсмена
    """

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    action: int       # Действие
    duration: float   # Продолжительность
    weight: float     # Вес спортсмена
    height: float     # Рост спортсмена

    # Получить дистанцию в КМ
    def get_distance(self) -> float:
        return super().get_distance()

    # Получить среднюю скорость движения
    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    # Получить количество затраченных калорий
    def get_spent_calories(self) -> float:
        spent_calories = ((self.CALORIES_WEIGHT_MULTIPLIER
                          * self.weight + ((self.get_mean_speed()
                                           * self.KMH_IN_MSEC)**2
                                           / (self.height
                                           / self.CM_IN_M))
                          * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                          * self.weight) * self.duration * self.MIN_IN_H)
        return spent_calories

    # Вернуть сообщение о выполненной тренировке
    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


@dataclass
class Swimming(Training):
    """Тренировка: плавание.
    Дополнительные входные переменные:
    - length_pool — длина бассейна в метрах;
    - count_pool — сколько раз пользователь переплыл бассейн.

    Переопределённые переменные:
    - LEN_STEP - расстояние за один гребок
    """

    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_MEAN_WEIGHT_MULTIPLIER = 2
    LEN_STEP = 1.38

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    # Получить дистанцию в КМ
    def get_distance(self) -> float:
        return super().get_distance()

    # Получить среднюю скорость движения
    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    # Получить количество затраченных калорий
    def get_spent_calories(self) -> float:
        spent_calories = ((self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.CALORIES_MEAN_WEIGHT_MULTIPLIER
                          * self.weight * self.duration)
        return spent_calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков.
     Входные параметры:
    - Словарь из двух параметров
        - Строка с кодом тренировки
        - Класс обработчик тренировки

    Возвращает:
    - Объект класса тренировки"""
    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in workout:
        raise ValueError(f"Такой тренировки - {workout_type}, не найдено")
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
