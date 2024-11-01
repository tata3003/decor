import os
from datetime import datetime

def logger(old_function):
    def new_function(*args, **kwargs):
        # Получаем текущее время для логирования
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Выполняем исходную функцию и сохраняем результат
        result = old_function(*args, **kwargs)
        
        # Создаем строку с деталями вызова функции
        log_message = (
            f"{current_time} - Function '{old_function.__name__}' "
            f"called with args: {args}, kwargs: {kwargs}, returned: {result}\n"
        )
        
        # Записываем лог в файл
        with open('main.log', 'a') as log_file:
            log_file.write(log_message)
        
        return result

    return new_function

# Тестовая функция
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    print("Тест пройден успешно!")
