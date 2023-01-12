import subprocess
import importlib
import os
import tempfile
import urllib.request
import zipfile

# Fonction qui vérifie si pip est installé et qui l'installe si ce n'est pas le cas
def check_and_install_pip():
    try:
        import pip
        print('Pip est déjà installé')
    except ImportError:
        print('pip n\'est pas installé, installation en cours...')
        
        # Créer un fichier temporaire pour stocker le script d'installation de pip
        fd, path = tempfile.mkstemp()
        os.close(fd)
        
        # Télécharger le script d'installation de pip avec curl
        subprocess.run(['curl', 'https://bootstrap.pypa.io/get-pip.py', '-o', path])
        
        # Exécuter le script d'installation de pip avec python
        subprocess.run(['python', path])
        
        # Supprimer le fichier temporaire
        os.remove(path)

# Fonction qui vérifie si une dépendance est installée et qui l'installe avec pip si elle ne l'est pas
def check_and_install_dependency(dependency):
    try:
        importlib.import_module(dependency)
        print(f'{dependency} est déjà installé')
    except ImportError:
        print(f'{dependency} n\'est pas installé, installation en cours...')
        subprocess.run(['pip', 'install', dependency])

# Vérifier et installer pip
check_and_install_pip()

# Liste des dépendances à vérifier
dependencies = ['tkinter', 'csv', 'ttkwidgets', 'ttkthemes']

# Vérifier et installer chaque dépendance
for dependency in dependencies:
    check_and_install_dependency(dependency)

url = "https://github.com/rdbende/Azure-ttk-theme/archive/refs/tags/v2.1.0.zip"
file_name = "v2.1.0.zip"

# Download the zip file
urllib.request.urlretrieve(url, file_name)

# Extract the contents of the zip file to the same directory as the script
script_dir = os.path.dirname(os.path.realpath(__file__))
with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall(script_dir)

# Delete the zip file after it has been extracted
os.remove(file_name)

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'annuaire.csv')

with open(file_path, 'w') as file:
    pass

urllib.request.urlretrieve("https://github.com/SLDDL/Schoolprojets/blob/main/Annusaire3000.py",os.path.join(current_directory, 'Annusaire3000.py'))
