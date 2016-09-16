# Under MIT License, see LICENSE.txt
"""
    Ce module garde en mémoire les modules intelligents disponibles
"""
class NonExistentModule(Exception):
    """ Est levée si le module intelligent requis n'est pas enregistré. """
    pass

class ModuleManager:
    """
        Gère les modules intelligents (par exemple, le Pathfinder) présents dans le jeu.
    """
    instance = None

    def __new__(cls):
        """
        S'assure qu'il n'y a qu'un seul ModuleManager
        :return: L'instance du ModuleManager
        """
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        self.modules = {}

    def register_module(self, module_name, module_ref):
        """
            Enregistre un module dans la liste des modules intelligents utilisables
            :param module_name: Le nom du module intelligent, celui-ci sera utilisé par la STA
            pour recueillir les modules.
            :param module_ref: La classe associée au module_name
        """
        self.modules[module_name] = module_ref(self)

    def acquire_module(self, module_name):
        """
        Retourne le module intelligent
        :param module_name: Le nom du module intelligent
        :return: La classe du module intelligent
        """
        try:
            return self.modules[module_name]
        except KeyError:
            raise NonExistentModule("Le module " + module_name + " n'existe pas.")
