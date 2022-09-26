from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
        self.training_type = training_type
    TEXT_1: str = "Тип тренировки"
    TEXT_2: str = "Длительность"
    TEXT_3: str = "Дистанция"
    TEXT_4: str = "Ср. скорость"
    TEXT_5: str = "Потрачено ккал"

    def get_message(self) -> str:
        return (
            f'{self.TEXT_1}: {self.training_type}; '
            f'{self.TEXT_2}: {self.duration:0.3f} ч.; '
            f'{self.TEXT_3}: {self.distance:0.3f} км; '
            f'{self.TEXT_4}: {self.speed:0.3f} км/ч; '
            f'{self.TEXT_5}: {self.calories:0.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000.0
    HOUR_TO_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self.__class__.__name__, self.duration,
                                    self.get_distance(), self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""
    С_CAL_1: int = 18
    С_CAL_2: int = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.С_CAL_1
                * self.get_mean_speed()
                - self.С_CAL_2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.HOUR_TO_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    С_CAL_1: float = 0.035
    С_CAL_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (
                self.С_CAL_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.С_CAL_2 * self.weight
            )
            * (self.duration * self.HOUR_TO_MIN)
        )


class Swimming(Training):
    """Тренировка: плавание."""
    С_CAL_1: float = 1.1
    LEN_STEP: float = 1.38

    def __init__(self,
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
        mean_speed = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.С_CAL_1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_data: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    return workout_data[workout_type](*data)


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
