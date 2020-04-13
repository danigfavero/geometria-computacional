from . import brute_force
from . import bentley_ottmann

children = [('brute_force', 'Brute_force', 'Forca\nBruta'),
            ('bentley_ottmann', 'Bentley_Ottmann', 'Bentley Ottmann')]

__all__ = [a[0] for a in children]
