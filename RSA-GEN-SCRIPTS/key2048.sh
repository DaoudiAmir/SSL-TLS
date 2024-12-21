#!/bin/bash

mkdir -p key2048

for i in {1..10000}; do
    openssl genrsa -out key2048/keys_$i.pem 2048
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la génération de la clé $i"
    else
        echo "Clé $i générée avec succès"
    fi
done