from random import choice

from meal.text import dinner_dict


async def get_random_meal() -> str:
    """Get random dinner idea"""
    return (f'Придумал!\n'
            f'Попробуй <u>{choice(dinner_dict["Блюдо"])}</u>,'
            f' а на гарнир пусть будет <u>{choice(dinner_dict["Гарнир"])}</u>. '
            f'К этому блюду очень хорошо подойдет <u>{choice(dinner_dict["Салат"])}</u>!\n'
            f'А на закуску попробуй <u>{choice(dinner_dict["Закуски"])}</u>🥪🍔\n'
            f'Приятного аппетита!😋')
