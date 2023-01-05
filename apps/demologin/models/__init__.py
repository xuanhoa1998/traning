import importlib 


__all__ = [
    'user',
]

prefix = 'apps.demologin.models'

for i in __all__:
    importlib.import_module(f'{prefix}.{i}')
