from typing import Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        + 'Длительность: {duration:.3f} ч.; '
        + 'Дистанция: {distance:.3f} км; '
        + 'Ср. скорость: {speed:.3f} км/ч; '
        + 'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите калории в %s.' % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEF_CAL_1: int = 18
    COEF_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время плавания."""
        return (
            (self.COEF_CAL_1 * self.get_mean_speed() - self.COEF_CAL_2)
            * self.weight / self.M_IN_KM * self.MIN_IN_HOUR * self.duration
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CAL_1: float = 0.035
    COEF_CAL_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() ** 2 // self.height)
            * self.COEF_CAL_2 * self.weight
            + (self.COEF_CAL_1 * self.weight)
            * self.MIN_IN_HOUR * self.duration
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_CAL_1: float = 1.1
    COEF_CAL_2: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения во время плавания."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.COEF_CAL_1)
            * self.COEF_CAL_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_comparison: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    try:
        return workout_comparison[workout_type](*data)
    except ValueError:
        print('Такой тренировки не существует')


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
