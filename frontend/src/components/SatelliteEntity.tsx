import { useMemo } from 'react';
import { Entity } from 'resium';
import {
  Color,
  JulianDate,
  SampledPositionProperty,
  TimeInterval,
  TimeIntervalCollection,
  VelocityOrientationProperty,
} from 'cesium';
import * as satellite from 'satellite.js';
import { getCesiumPositionFromSatrec } from '../utils/orbit';

type OmmJson = Parameters<typeof satellite.json2satrec>[0];

type SatelliteEntityProps = {
  omm: OmmJson;
  startDate?: Date;
  minutes?: number;
  stepSeconds?: number;
};

export const SatelliteEntity = ({
  omm,
  startDate = new Date(),
  minutes = 120,
  stepSeconds = 30,
}: SatelliteEntityProps) => {
  const { positionProperty, availability } = useMemo(() => {
    const satrec = satellite.json2satrec(omm);

    const sampledPosition = new SampledPositionProperty();

    const start = JulianDate.fromDate(startDate);
    const stopDate = new Date(startDate.getTime() + minutes * 60 * 1000);
    const stop = JulianDate.fromDate(stopDate);

    for (let seconds = 0; seconds <= minutes * 60; seconds += stepSeconds) {
      const sampleDate = new Date(startDate.getTime() + seconds * 1000);
      const julianDate = JulianDate.fromDate(sampleDate);

      const cesiumPosition = getCesiumPositionFromSatrec(satrec, sampleDate);

      if (!cesiumPosition) {
        continue;
      }

      sampledPosition.addSample(julianDate, cesiumPosition);
    }

    return {
      positionProperty: sampledPosition,
      availability: new TimeIntervalCollection([
        new TimeInterval({ start, stop }),
      ]),
    };
  }, [omm, startDate, minutes, stepSeconds]);

  return (
    <Entity
      name={omm.OBJECT_NAME ?? omm.OBJECT_ID ?? "Satellite"}
      availability={availability}
      position={positionProperty}
      orientation={new VelocityOrientationProperty(positionProperty)}
      point={{ 
        pixelSize: 10,
        color: Color.CYAN,
        outlineColor: Color.WHITE,
        outlineWidth: 1,
      }}
      path={{
        show: true,
        leadTime: 45 * 60,
        trailTime: 45 * 60,
        width: 4,
        material: Color.CYAN,
      }}
    />
  );
}