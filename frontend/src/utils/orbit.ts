import { Cartesian3 } from 'cesium';
import * as satellite from 'satellite.js';

export const getCesiumPositionFromSatrec = (
  satrec: satellite.SatRec,
  date: Date
): Cartesian3 | null => {
  const result = satellite.propagate(satrec, date);

  if (!result) {
    return null;
  }

  const gmst = satellite.gstime(date);
  const geodetic = satellite.eciToGeodetic(result.position, gmst);

  const longitude = satellite.degreesLong(geodetic.longitude);
  const latitude = satellite.degreesLat(geodetic.latitude);
  const altitudeMeters = geodetic.height * 1000;

  return Cartesian3.fromDegrees(longitude, latitude, altitudeMeters);
}