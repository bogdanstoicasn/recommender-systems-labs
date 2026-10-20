
import pandas as pd

INPUT_FILE = "./ml-100k/u.item"
OUTPUT_FILE = "movies.csv"

COLUMNS = [
    "movieId",
    "title",
    "release_date",
    "video_release_date",
    "imdb_url",
    "unknown",
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western",
]


def main():
    df = pd.read_csv(
        INPUT_FILE,
        sep="|",
        encoding="latin-1",
        header=None,
        names=COLUMNS,
        usecols=range(24),
        engine="python",
    )

    # Extract the release year from the release date.
    df["release_year"] = pd.to_datetime(
        df["release_date"],
        format="%d-%b-%Y",
        errors="coerce",
    ).dt.year.astype("Int64")

    # Combine the 19 genre flags into one descriptive string.
    genre_columns = COLUMNS[5:]

    df["genres"] = df.apply(
        lambda row: "|".join(
            genre
            for genre in genre_columns
            if row[genre] == 1
        ),
        axis=1,
    )

    # Keep the ID as an identifier, not as a descriptive property.
    result = df[["movieId", "title", "release_year", "genres"]].copy()

    # Remove MovieLens's placeholder item, not a real movie.
    result = result[result["title"].str.lower() != "unknown"].copy()

    result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Dataset created: {OUTPUT_FILE}")
    print(f"Number of movies: {len(result)}")
    print("\nColumns:")
    print(result.dtypes)
    print("\nFirst five rows:")
    print(result.head().to_string(index=False))

    if not 100 <= len(result) <= 10_000:
        raise ValueError("The dataset must contain between 100 and 10,000 movies.")

    if result["movieId"].duplicated().any():
        raise ValueError("Duplicate movie IDs found.")

    if result["title"].isna().any():
        raise ValueError("Some movies have no title.")


if __name__ == "__main__":
    main()
