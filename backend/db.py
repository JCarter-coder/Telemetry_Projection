import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def get_satellites():
  async with asyncpg.create_pool(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("TARGET_DB")
  ) as pool:
    query = await pool.fetch(
      '''
      SELECT * FROM satellites;
      '''
    )

    await pool.close()
    return query
  
async def get_satellite(q):
  async with asyncpg.create_pool(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("TARGET_DB")
  ) as pool:
    query = await pool.fetchrow(
      '''
      SELECT 
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
        mean_motion_ddot
      FROM satellites
      WHERE object_id=$1;
      ''', q
    )

    await pool.close()

    print(type(query))
    
    return query