from fastapi import FastAPI
from pydantic import BaseModel
from db import (
  get_satellites,
  get_satellite
)

app = FastAPI()

class SatRec(BaseModel):
  object_name: str # "KUIPER-00008"
  object_id: str # "2025-088A",
  epoch: str # ? "2026-07-01T01:13:34.200192",
  mean_motion: float # 14.79922108,
  eccentricity: float # ? 7.625e-5,
  inclination: float # 51.9018,
  raan: float # 306.7242,
  arg_of_pericenter: float # 105.1798,
  mean_anomaly: float # 254.9249,
  ephemeris_type: int # 0,
  classification_type: str # "U",
  norad_cat_id: int # 63724,
  element_set_no: int # 999,
  rev_at_epoch: int # 6483,
  bstar: float # ? -0.00011397759,
  mean_motion_dot: float # ? -1.09e-5,
  mean_motion_ddot: int # 0

@app.get("/")
def read_root():
  return "Telemetry Projection Landing Page"

@app.get("/satellites")
async def read_satellites() -> list[SatRec] | None:
  satellites = await get_satellites()
  if satellites == None:
    return None
  result = [SatRec(**dict(row)) for row in satellites]
  return result

@app.get("/satellites/{object_id}")
async def read_item(object_id: str) -> SatRec | None:
  satellite = await get_satellite(object_id)
  if satellite == None:
    return None
  result = SatRec(**dict(satellite))
  return result
