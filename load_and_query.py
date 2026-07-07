"""Phase 0 smoke test: CSV -> Postgres -> query back."""

import pandas as pd
import psycopg

CONN = "host=localhost port=5432 dbname=sandbox user=mrtro password=localdev"

def main() -> None:
    df = pd.read_csv("data/stations.csv")
    print(f"Read {len(df)} rows from CSV")

    with psycopg.connect(CONN) as conn, conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS stations;")
        cur.execute("""
            CREATE TABLE stations (
                station_id integer PRIMARY KEY,
                name text NOT NULL,
                state text NOT NULL,
                annual_rainfall_mm integer
            );
        """)
        with cur.copy("COPY stations FROM STDIN") as copy:
            for row in df.itertuples(index=False):
                copy.write_row(row)

        cur.execute("""
            SELECT name, annual_rainfall_mm
            FROM stations
            ORDER BY annual_rainfall_mm DESC;
        """)
        print("\nStations by rainfall:")
        for name, rain in cur.fetchall():
            print(f"  {name}: {rain} mm")


if __name__ == "__main__":
    main()