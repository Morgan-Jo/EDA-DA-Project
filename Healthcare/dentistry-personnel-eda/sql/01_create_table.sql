DROP TABLE dentistry_personnel;

CREATE TABLE dentistry_personnel (
    IndicatorCode TEXT,
    Indicator TEXT,
    ValueType TEXT,
    ParentLocationCode TEXT,
    ParentLocation TEXT,
    LocationType TEXT,
    SpatialDimValueCode TEXT,
    Location TEXT,
    PeriodType TEXT,
    Period INTEGER,
    IsLatestYear BOOLEAN,
    FactValueNumeric INTEGER
    Value REAL,
    FactComments TEXT,
    Language TEXT,
    DateModified TEXT
);

.mode csv
.headers on
.import data\raw\dentistry-personnel.csv dentistry_personnel
