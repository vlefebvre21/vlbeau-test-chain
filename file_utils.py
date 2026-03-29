import os

def read_file(path):
    """Lit le contenu du fichier."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    """Ecrit le contenu dans le fichier."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def list_files(directory='.'):
    """Liste les fichiers dans le répertoire."""
    return os.listdir(directory)

def file_exists(path):
    """Vérifie si le fichier existe."""
    return os.path.exists(path)

def get_file_size(path):
    """Retourne la taille du fichier en octets."""
    if not file_exists(path):
        return 0
    return os.path.getsize(path)

if __name__ == "__main__":
    print("=== Tests simples file_utils.py ===")
    
    test_file = "test.txt"
    
    # Test write_file
    write_file(test_file, "Hello, world!")
    print(f"write_file: fichier {test_file} créé.")
    
    # Test read_file
    content = read_file(test_file)
    print(f"read_file('{test_file}'): '{content}'")
    
    # Test list_files
    files = list_files('.')
    print(f"list_files('.'): {files}")
    
    # Test file_exists
    print(f"file_exists('{test_file}'): {file_exists(test_file)}")
    
    # Test get_file_size
    size = get_file_size(test_file)
    print(f"get_file_size('{test_file}'): {size} bytes")
    
    # Cleanup
    os.remove(test_file)
    print("Tests terminés. Fichier test supprimé.")