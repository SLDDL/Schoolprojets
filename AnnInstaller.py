import importlib
import os
import tempfile

# Fonction qui vérifie si pip est installé et qui l'installe si ce n'est pas le cas
def check_and_install_pip():
    try:
        import pip
    except ImportError:
        print('pip n\'est pas installé, installation en cours...')
        
        # Créer un fichier temporaire pour stocker le script d'installation de pip
        fd, path = tempfile.mkstemp()
        os.close(fd)
        
        # Télécharger le script d'installation de pip avec curl
        !curl https://bootstrap.pypa.io/get-pip.py -o {path}
        
        # Exécuter le script d'installation de pip avec python
        !python {path}
        
        # Supprimer le fichier temporaire
        os.remove(path)

# Fonction qui vérifie si une dépendance est installée et qui l'installe avec pip si elle ne l'est pas
def check_and_install_dependency(dependency):
    try:
        importlib.import_module(dependency)
        print(f'{dependency} est déjà installé')
    except ImportError:
        print(f'{dependency} n\'est pas installé, installation en cours...')
        !pip install {dependency}

# Vérifier et installer pip
check_and_install_pip()

# Liste des dépendances à vérifier
dependencies = ['tkinter', 'csv', 'ttkwidgets', 'ttkthemes']

# Vérifier et installer chaque dépendance
for dependency in dependencies:
    check_and_install_dependency(dependency)