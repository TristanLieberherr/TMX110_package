from .tmx110 import TMX110, Keys, ValuesStruct, StatusBits


try:
    from . import version
    __version__ = version.version
except ImportError:
    __version__ = None

__copyright__ = 'Copyright 2020 HEIG-VD'