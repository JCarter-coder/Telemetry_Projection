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