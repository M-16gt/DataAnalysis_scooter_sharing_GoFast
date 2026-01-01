from pathlib import Path


def joinpath(*paths, _basepath: Path = Path(__file__).resolve().parent.parent) -> Path:
    """
    Последовательно объединяет пути, начиная от базового каталога.

    Функция принимает произвольное количество строк или объектов Path и последовательно
    присоединяет их к базовому пути, используя оператор деления Path.

    Args:
        *paths: Произвольное количество строк или объектов Path для объединения.
        _basepath (Path, optional): Базовый путь для объединения.
            По умолчанию используется каталог на два уровня выше текущего файла
            (предполагается структура проекта, где текущий файл находится в подкаталоге).

    Returns:
        Path: Полный путь, полученный последовательным объединением всех переданных
        компонентов с базовым путем.

    Note:
        Функция модифицирует `_basepath` в процессе выполнения с помощью оператора
        присваивания в выражении спискового включения. Это идиоматический способ
        последовательного объединения путей в Python.

    Examples:
        >>> # Если текущий файл находится в /home/user/project/src/utils/
        >>> joinpath("data", "raw", "file.csv")
        PosixPath('/home/user/project/data/raw/file.csv')

        >>> # С использованием пользовательского базового пути
        >>> joinpath("config", "settings.yaml", _basepath=Path("/etc/app"))
        PosixPath('/etc/app/config/settings.yaml')

        >>> # Без дополнительных путей (вернется базовый путь)
        >>> joinpath()
        PosixPath('/home/user/project')
    """
    [_basepath := _basepath / p for p in paths]
    return _basepath