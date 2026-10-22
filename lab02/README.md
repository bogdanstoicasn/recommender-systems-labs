# Lab 2 – Recombee Recommendation System

## Dataset

This project uses the MovieLens 100K dataset, which contains movie information
and user ratings. For this laboratory, only the movie catalog is used.

Link: [MovieLens] (https://grouplens.org/datasets/movielens/)

The `movies.csv` file contains 1,681 movies.

## Dataset Preparation

The `prepare_data.py` script processes the original MovieLens `u.item` file
and generates `movies.csv`.

The CSV contains the following columns:

| Column | Description | Type |
|---|---|---|
| `movieId` | Unique movie identifier | Integer |
| `title` | Movie title | String |
| `release_year` | Movie release year | Integer |
| `genres` | Movie genres separated by `|` | String |

The `movieId` column is used as the item identifier and is not registered
as a descriptive item property in Recombee.

## Recombee Item Properties

The `recombee_properties.py` script registers the following item properties:

| Property | Recombee type | Description |
|---|---|---|
| `title` | `string` | Movie title |
| `release_year` | `int` | Movie release year |
| `genres` | `string` | Movie genres |

The script also lists the registered properties to verify the configuration.

## Requirements

- Python 3
- pandas
- recombee-api-client

## Execution

Generate the dataset:

```bash
python3 prepare_data.py