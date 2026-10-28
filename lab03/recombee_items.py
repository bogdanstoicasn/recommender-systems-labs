import os

import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
# Tokenul se citeste din variabila de mediu ca sa nu ajunga in repository.
DB_NAME = 'bogdan-sr-dev'
PRIVATE_TOKEN = "my-api-key"
REGION = Region.EU_WEST

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=REGION)

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02 (MovieLens)
PATH_DATASET = 'movies.csv'
BATCH_SIZE = 100


def send_batch(requests):
    """Trimite un lot si raporteaza request-urile esuate (Batch nu arunca exceptie pentru ele)."""
    results = client.send(Batch(requests))
    failed = [(req.item_id, res) for req, res in zip(requests, results) if res['code'] >= 300]
    for item_id, res in failed:
        print(f"Eroare la item-ul '{item_id}': {res['json']}")
    return len(requests) - len(failed)


def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    # Anul apare in titlu, ex. "Toy Story (1995)"; lipseste la cateva filme -> null in Recombee
    df['release_year'] = df['title'].str.extract(r'\((\d{4})\)\s*$')[0].astype('Int64')
    print(f"Se trimit {len(df)} item-uri in Recombee...")

    requests = []
    sent_ok = 0
    for _, row in df.iterrows():
        # TODO 3: ID-ul unic al produsului
        item_id = str(row['movieId'])
        # TODO 4: Maparea proprietatilor definite in Lab 02
        properties = {
            "title": str(row['title']),
            "release_year": None if pd.isna(row['release_year']) else int(row['release_year']),
            "genres": str(row['genres']),
        }
        # SetItemValues creeaza automat item-ul daca acesta nu exista
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        if len(requests) == BATCH_SIZE:
            sent_ok += send_batch(requests)
            requests = []
            print(f"Trimise pana acum: {sent_ok}")

    # Restul ramas (daca totalul nu e multiplu de BATCH_SIZE)
    if requests:
        sent_ok += send_batch(requests)

    print(f"Gata: {sent_ok}/{len(df)} item-uri trimise cu succes.")


if __name__ == "__main__":
    try:
        send_items()
    except APIException as e:
        print(f"Eroare API Recombee: {e}")