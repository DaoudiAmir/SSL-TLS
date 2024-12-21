"""
Module d'analyse des GCD (Greatest Common Divisor)
Auteurs : Daoudi Amir, Heloui Youssef, Baye Diop Cheikh

Ce module identifie les certificats ayant des facteurs communs dans leurs moduli publics
en analysant directement les fichiers `.pem`.

Fonctionnalités :
- Calcul du GCD entre les moduli des clés.
- Traitement basé sur la taille des clés.
- Enregistrement des résultats dans des fichiers texte.
"""

import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import math

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

def gcd(a, b):
    """
    Fonction pour calculer le plus grand commun diviseur (GCD) entre deux entiers.
    Args:
        a (int): Premier entier.
        b (int): Deuxième entier.
    Returns:
        int: Le GCD de a et b.
    """
    while b:
        a, b = b, a % b
    return a

def findGCD(size):
    """
    Fonction pour analyser les GCD dans les certificats d'une taille spécifique.
    Args:
        size (str): La taille des clés (ex : "512", "1024", "2048").
    """
    print(f"Analyse des GCD pour les clés de taille : {size}")

    key_dir = f"./key{size}/"
    files = os.listdir(key_dir)

    # Parcours de toutes les paires possibles de fichiers PEM
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            try:
                file1 = os.path.join(key_dir, files[i])
                file2 = os.path.join(key_dir, files[j])

                modulus1 = extract_modulus(file1)
                modulus2 = extract_modulus(file2)

                gcd_result = gcd(modulus1, modulus2)

                # Si le GCD est différent de 1, il y a une vulnérabilité
                if gcd_result != 1:
                    print(f"GCD trouvé entre {files[i]} et {files[j]}: {gcd_result}")
                    with open(f"./GCD/{size}_gcd.txt", "a") as gcd_file:
                        gcd_file.write(f"{files[i]},{files[j]},{gcd_result}\n")
            except Exception as e:
                print(f"Erreur lors du traitement des fichiers {files[i]} et {files[j]}: {e}")

if __name__ == "__main__":
    try:
        # Liste des tailles de clés disponibles
        cert_sizes = ["512", "1024", "2048"]

        # Parcours de chaque taille de clé
        for size in cert_sizes:
            findGCD(size)

    except Exception as e:
        print(f"Erreur : {e}")
    