import argparse
import holidays
import mysql.connector
from mysql.connector import pooling
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def insert_holidays(conn, country: str, subdiv: str | None, year: int):
    cursor = conn.cursor()
    hol = holidays.country_holidays(country=country, subdiv=subdiv, years=[year])
    rows = [(country, subdiv, year, str(k), v) for k, v in hol.items()]
    cursor.executemany(
        """
        INSERT INTO holidays (country, subdiv, year, date, name)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name)
        """,
        rows
    )
    conn.commit()
    cursor.close()
    return (country, subdiv, year)


def process_task(pool, country: str, subdiv: str | None, year: int):
    conn = pool.get_connection()
    try:
        return insert_holidays(conn, country, subdiv, year)
    finally:
        conn.close()  # releases back to pool


def main():
    parser = argparse.ArgumentParser(
        description="Load holidays into a MySQL database using python-holidays."
    )
    parser.add_argument("-y", "--years", nargs="+", type=int, help="Year(s) to include")
    parser.add_argument("--start", type=int, help="Start year for a range")
    parser.add_argument("--end", type=int, help="End year for a range (inclusive)")
    parser.add_argument("--host", default="localhost", help="MySQL host")
    parser.add_argument("--user", required=True, help="MySQL user")
    parser.add_argument("--password", default='', help="MySQL password")
    parser.add_argument("--database", required=True, help="MySQL database name")
    args = parser.parse_args()

    # determine years
    if args.years:
        years = args.years
    elif args.start is not None and args.end is not None:
        if args.start > args.end:
            parser.error("--start must be <= --end")
        years = list(range(args.start, args.end + 1))
    else:
        parser.error("You must specify either --years or both --start and --end")

    # set up connection pool (reuse connections)
    pool = pooling.MySQLConnectionPool(
        pool_name="holiday_pool",
        pool_size=8,   # <= match ThreadPoolExecutor max_workers
        host=args.host,
        user=args.user,
        password=args.password,
        database=args.database
    )

    countries = holidays.list_supported_countries()
    tasks = [(country, subdiv, year)
             for country, subdivs in countries.items()
             for year in years
             for subdiv in (subdivs or [None])]

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_task, pool, *task) for task in tasks]
        for f in tqdm(as_completed(futures), total=len(futures), desc="Processing Holidays (DB inserts)"):
            try:
                pass
            except Exception as e:
                pass


if __name__ == "__main__":
    main()
