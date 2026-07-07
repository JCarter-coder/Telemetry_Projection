import asyncpg
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def create_database_if_not_exists() -> None:
  """Connects to the default template1 database to create the target database."""
  print(f"Checking if database '{os.getenv("TARGET_DB")}' exists...")

  # Connect to a system database to run CREATE DATABASE
  conn = await asyncpg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="template1"
  )

  # Check if database exists
  db_exists = await conn.fetchval(
    "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname = $1)",
    os.getenv("TARGET_DB")
  )

  if not db_exists:
    await conn.execute(f'CREATE DATABASE "{os.getenv("TARGET_DB")}" OWNER {os.getenv("DB_USER")}')
    print(f"Database '{os.getenv("TARGET_DB")}' created sucessfully.")
  else:
    print(f"Database '{os.getenv("TARGET_DB")}' already exists.")

  await conn.close()

async def schema_and_seed() -> None:
  """Connects to the target database to build the schema and seed data."""
  # Connect to target database
  conn = await asyncpg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("TARGET_DB")
  )

  print("Creating tables...")
  await conn.execute('''
    DROP TABLE IF EXISTS satellites;

    CREATE TABLE satellites (
      object_id TEXT PRIMARY KEY,    
      object_name TEXT NOT NULL,
      epoch TEXT NOT NULL,
      mean_motion DOUBLE PRECISION NOT NULL,
      eccentricity REAL NOT NULL,
      inclination REAL NOT NULL,
      raan REAL NOT NULL,
      arg_of_pericenter REAL NOT NULL,
      mean_anomaly REAL NOT NULL,
      ephemeris_type SMALLINT NOT NULL,
      classification_type TEXT NOT NULL,
      norad_cat_id INTEGER NOT NULL,
      element_set_no SMALLINT NOT NULL,
      rev_at_epoch SMALLINT NOT NULL,
      bstar DOUBLE PRECISION NOT NULL,
      mean_motion_dot DOUBLE PRECISION NOT NULL,
      mean_motion_ddot SMALLINT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  ''')

  seed_data = [
    ("2025-088A","KUIPER-00008","2026-07-01T01:13:34.200192",14.79922108,7.625e-5,51.9018,306.7242,105.1798,254.9249,0,"U",63724,999,6483,-0.00011397759,-1.09e-5,0),
    ("2025-088B","KUIPER-00009","2026-07-07T08:18:38.047680",14.79914977,7.07e-5,51.9024,296.5184,78.8651,281.239,0,"U",63725,999,6551,8.9335854e-5,4.6e-6,0),
    ("2025-088C","KUIPER-00010","2026-07-07T05:39:06.294528",14.79927954,6.34e-5,51.9028,274.481,91.3221,268.7814,0,"U",63726,999,6543,-0.00014017727,-1.289e-5,0),
    ("2025-088D","KUIPER-00011","2026-07-06T14:03:39.917088",14.79923371,6.957e-5,51.9017,284.902,115.9511,244.1523, 0,"U",63727,999,6536,-0.00010313432,-1.007e-5,0),
    ("2025-088E","KUIPER-00012","2026-07-07T05:50:45.427776",14.7992216,8.137e-5,51.8998,266.9265,111.4614,248.6435,0,"U",63728,999,6562,-5.8299592e-5,-6.65e-6,0)
  ]

  print(f"Seeding {len(seed_data)} records into 'users' table...")

  await conn.executemany('''
    INSERT INTO satellites (
      object_id,
      object_name,
      epoch,
      mean_motion,
      eccentricity,
      inclination,
      raan,
      arg_of_pericenter,
      mean_anomaly,
      ephemeris_type,
      classification_type,
      norad_cat_id,
      element_set_no,
      rev_at_epoch,
      bstar,
      mean_motion_dot,
      mean_motion_ddot,
      created_at
    )
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, CURRENT_TIMESTAMP)
  ''', seed_data)

  # Verify the insertion
  rows = await conn.fetch("SELECT object_id, object_name, TO_CHAR(created_at, 'MM/DD/YYYY, HH24:MI:SS') AS created FROM satellites;")
  print("\nCurrent verification from 'users' table:")
  for row in rows:
    print(f"ID: {row['object_id']} | Name: {row['object_name']} | Created At: {row['created']}")

  await conn.close()
    
async def main():
  await create_database_if_not_exists()
  await schema_and_seed()

if __name__ == "__main__":
  asyncio.run(main())