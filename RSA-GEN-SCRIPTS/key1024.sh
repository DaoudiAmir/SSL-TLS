#!/bin/bash

mkdir -p key1024

for i in {1..100}; do
    openssl genrsa -out key1024/keys_$i.pem 1024
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la génération de la clé $i"
    else
        echo "Clé $i générée avec succès"
    fi
done