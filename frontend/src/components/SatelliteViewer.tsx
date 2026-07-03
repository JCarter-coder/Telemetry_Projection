import { useEffect, useMemo, useState } from 'react';
import {
  Entity,
  EntityDescription,
  Moon,
  PointGraphics,
  PolygonGraphics,
  Sun,
  Viewer
} from 'resium';
import {
  Cartesian3,
  Clock,
  ClockRange,
  ClockStep,
  ClockViewModel,
  Color,
  createWorldTerrainAsync,
  JulianDate,
} from 'cesium';
import { SatelliteEntity } from './SatelliteEntity';
// import { kuiperSats } from '../data/...'
import * as satellite from 'satellite.js';

type OmmJson = Parameters<typeof satellite.json2satrec>[0];

const createClockViewModel = (startDate: Date, minutes = 120): ClockViewModel => {
  const start = JulianDate.fromDate(startDate);
  const stop = JulianDate.addMinutes(start, minutes, new JulianDate());

  const clock = new Clock({
    startTime: start.clone(),
    currentTime: start.clone(),
    stopTime: stop.clone(),
    clockRange: ClockRange.LOOP_STOP,
    clockStep: ClockStep.SYSTEM_CLOCK_MULTIPLIER,
    multiplier: 1,
    shouldAnimate: true,
  });

  return new ClockViewModel(clock);
}

export const SatelliteViewer = () => {
  const [ommRecords, setOmmRecords] = useState<OmmJson[]>([]);
  //const [kuiperOmm, setKuiperOmm] = useState<OmmJson[]>([]);

  const startDate = useMemo(() => new Date(), []);

  const clockViewModel = useMemo(() => {
    return createClockViewModel(startDate, 120);
  }, [startDate]);

  useEffect(() => {
    const loadSatellites = async () => {
      try {
        const ommData: OmmJson[] = [
          {
            "OBJECT_NAME": "KUIPER-00008",
            "OBJECT_ID": "2025-088A",
            "EPOCH": "2026-07-01T01:13:34.200192",
            "MEAN_MOTION": 14.79922108,
            "ECCENTRICITY": 7.625e-5,
            "INCLINATION": 51.9018,
            "RA_OF_ASC_NODE": 306.7242,
            "ARG_OF_PERICENTER": 105.1798,
            "MEAN_ANOMALY": 254.9249,
            "EPHEMERIS_TYPE": 0,
            "CLASSIFICATION_TYPE": "U",
            "NORAD_CAT_ID": 63724,
            "ELEMENT_SET_NO": 999,
            "REV_AT_EPOCH": 6483,
            "BSTAR": -0.00011397759,
            "MEAN_MOTION_DOT": -1.09e-5,
            "MEAN_MOTION_DDOT": 0
          },
        ]
        //setKuiperOmm(ommData);

        setOmmRecords(ommData);
      } catch (error) {
        console.error(error);
      }
    };

    loadSatellites();
  }, []);

  const terrainProvider = createWorldTerrainAsync();

  const city = Cartesian3.fromDegrees(-104.8212, 41.1347, 100); // Cheyenne, WY

  const wyoming = {
    hierarchy: Cartesian3.fromDegreesArray([
      -109.080842, 45.002073, -105.91517, 45.002073, -104.058488, 44.996596,
      -104.053011, 43.002989, -104.053011, 41.003906, -105.728954, 40.998429,
      -107.919731, 41.003906, -109.04798, 40.998429, -111.047063, 40.998429,
      -111.047063, 42.000709, -111.047063, 44.476286, -111.05254, 45.002073,
    ]),
    material: Color.WHITE.withAlpha(0.2),
    outline: true,
    outlineColor: Color.BLACK,
  };

  return (
    <Viewer
      full terrainProvider={terrainProvider}
      timeline
      animation
      clockViewModel={clockViewModel}
    >
      {ommRecords.slice(0,1).map((omm) => (
        <SatelliteEntity
          key={omm.NORAD_CAT_ID}
          omm={omm}
          startDate={startDate}
          minutes={120}
          stepSeconds={30}
        />
      ))}
      <Sun glowFactor={1.0} />
      <Moon show={true} />
      <Entity position={city} name='Cheyenne' description='Capitol of Wyoming'>
        <PointGraphics pixelSize={10} />
        <EntityDescription>
          <h1>Cheyenne, WY</h1>
          <p>Capitol of Wyoming</p>
        </EntityDescription>
      </Entity>
      <Entity name='Wyoming' {...wyoming}>
        <PolygonGraphics {...wyoming} />
      </Entity>
    </Viewer>
  )
}