#!/bin/bash

mkdir -p key512

for i in {1..100}; do
    openssl genrsa -out key512/keys_$i.pem 512
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la génération de la clé $i"
    else
        echo "Clé $i générée avec succès"
    fi
done