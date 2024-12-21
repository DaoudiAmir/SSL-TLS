"""
Module de détection de doublons de certificats
Auteurs : Daoudi Amir, Heloui Youssef, Baye Diop Cheikh

Ce module identifie les certificats ayant des moduli publics identiques (doublons)
en analysant directement les fichiers `.pem`.

Fonctionnalités :
- Détection des clés dupliquées (même modulus).
- Traitement basé sur la taille des clés.
- Génération d'un fichier pour les doublons détectés.
"""

import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def extract_modulus(file_path):
    """
    Extrait le modulus d'un fichier PEM contenant une clé RSA.
    Args:
        file_path (str): Chemin vers le fichier PEM.
    Returns:
        int: Le modulus de la clé RSA.
    """
    with open(file_path, "rb") as pem_file:
        private_key = serialization.load_pem_private_key(
            pem_file.read(),
            password=None,
        )
        if isinstance(private_key, rsa.RSAPrivateKey):
            return private_key.public_key().public_numbers().n
    return None

def findDupes(size):
    """
    Fonction pour trouver les doublons dans les certificats d'une taille spécifique.
    Args:
        size (str): La taille des clés (ex : "512", "1024", "2048").
    """
    print(f"Recherche de doublons pour les clés de taille : {size}")

    key_dir = f"./key{size}/"
    moduli = {}
    duplicates = []

    # Parcours de tous les fichiers PEM dans le répertoire
    for file_name in os.listdir(key_dir):
        file_path = os.path.join(key_dir, file_name)
        try:
            modulus = extract_modulus(file_path)
            if modulus in moduli:
                duplicates.append((moduli[modulus], file_name))
            else:
                moduli[modulus] = file_name
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {file_name}: {e}")

    # Sauvegarde des doublons détectés
    with open(f"./DUPES/{size}_dupes.txt", "w") as dupes_file:
        for dup in duplicates:
            dupes_file.write(f"{dup[0]} et {dup[1]} ont le même modulus.\n")

if __name__ == "__main__":
    try:
        # Liste des tailles de clés disponibles
        cert_sizes = ["512", "1024", "2048"]

        # Parcours de chaque taille de clé
        for size in cert_sizes:
            findDupes(size)

    except Exception as e:
        print(f"Erreur : {e}")
