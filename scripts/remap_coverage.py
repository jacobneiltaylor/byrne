import sys
import sqlite3
from os.path import abspath


SELECT_QUERY = "SELECT * FROM file WHERE path LIKE ?"
UPDATE_QUERY = "UPDATE file SET path = ? WHERE id = ?"


def iterate_files(db: sqlite3.Connection, path: str) -> list:
    cursor = db.cursor()
    cursor.execute(SELECT_QUERY, (f"{path}%",))
    for row in cursor:
        yield row


def update_file(db: sqlite3.Connection, row_id, path):
    print(f"Updating row with ID {row_id} to {path}...")
    cursor = db.cursor()
    cursor.execute(UPDATE_QUERY, (path, row_id))
    db.commit()

def get_connection(path):
    return sqlite3.connect(abspath(path))


def main():
    print("Attempting to remap coverage file info...")
    expect_path = sys.argv[1]
    new_path = sys.argv[2]
    coverage_file = ".coverage"

    try:
        coverage_file = sys.argv[3]
    except:
        print("Using default coverage db...")

    with get_connection(coverage_file) as db:
        for row_id, path in iterate_files(db, expect_path):
            update_file(db, row_id, path.replace(expect_path, new_path))

    print("Done!")

if __name__ == "__main__":
    main()