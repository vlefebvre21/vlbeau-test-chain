import os
from typing import List, Optional

def read_file(path: str) -> str:
    """
    Lit le contenu du fichier à l'emplacement spécifié.

    Args:
        path (str): Chemin vers le fichier à lire.

    Returns:
        str: Contenu du fichier encodé en UTF-8.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        PermissionError: Si pas de permission de lecture.
        IsADirectoryError: Si le chemin pointe vers un répertoire.
        UnicodeDecodeError: Si le fichier ne peut pas être décodé en UTF-8.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Le fichier n'existe pas: {path}")
    if os.path.isdir(path):
        raise IsADirectoryError(f"Le chemin est un répertoire: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except PermissionError:
        raise PermissionError(f"Permission refusée pour lire {path}")

def write_file(path: str, content: str) -> None:
    """
    Écrit le contenu dans le fichier spécifié. Crée les répertoires parents si nécessaire.

    Args:
        path (str): Chemin vers le fichier à écrire/créer.
        content (str): Contenu à écrire (UTF-8).

    Raises:
        PermissionError: Si pas de permission d'écriture.
    """
    dir_path = os.path.dirname(path) or '.'
    os.makedirs(dir_path, exist_ok=True)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    except PermissionError:
        raise PermissionError(f"Permission refusée pour écrire {path}")

def list_files(directory: str = '.') -> List[str]:
    """
    Liste les fichiers et répertoires dans le répertoire spécifié.

    Args:
        directory (str): Chemin du répertoire (défaut: répertoire courant).

    Returns:
        List[str]: Liste des noms de fichiers/répertoires.

    Raises:
        NotADirectoryError: Si le chemin n'est pas un répertoire.
        FileNotFoundError: Si le répertoire n'existe pas.
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Le répertoire n'existe pas: {directory}")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Pas un répertoire: {directory}")
    return os.listdir(directory)

def file_exists(path: str) -> bool:
    """
    Vérifie si le fichier existe et est bien un fichier (pas un répertoire).

    Args:
        path (str): Chemin vers le fichier.

    Returns:
        bool: True si fichier existant, False sinon.
    """
    return os.path.isfile(path)

def get_file_size(path: str) -> Optional[int]:
    """
    Retourne la taille du fichier en octets.

    Args:
        path (str): Chemin vers le fichier.

    Returns:
        Optional[int]: Taille en octets si fichier existe, None sinon.
    """
    if not file_exists(path):
        return None
    return os.path.getsize(path)

if __name__ == "__main__":
    print("Module file_utils.py chargé. Utilisez unittest pour les tests.")
