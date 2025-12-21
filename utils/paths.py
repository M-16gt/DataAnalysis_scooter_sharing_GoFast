from pathlib import Path


def joinpath(*paths, _basepath: Path = Path(__file__).resolve().parent.parent) -> Path:
    [_basepath := _basepath / p for p in paths]
    return _basepath
