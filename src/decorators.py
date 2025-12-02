def log(filename=None):
    # filename - куда писать логи (файл или консоль)

    def decorator(func):
        # func - функция которую мы декорируем

        def wrapper(*args, **kwargs):
            # здесь логика логирования
            pass

        return wrapper

    return decorator