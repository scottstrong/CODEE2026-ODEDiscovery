# Data

`temperatures.csv` is the record every script uses: 116 one-minute samples
(minute 0-115) from two Govee H5075 thermo-hygrometers carried together on
2026-03-30, 21:15-23:10. Columns: minute, sensor_I, sensor_II (degrees F).
Readings sit on the instrument's 0.1 C grid.

`raw/` holds the untouched exports. Note that the export file names are the
reverse of the paper's sensor names:

    Thermo-Hygrometer 2_export_202603302310.csv         -> Sensor I  (left)
    Thermo-Hygrometer 1_export_202603302311.csv         -> Sensor II (right)
    Thermo-Hygrometer 2_export_202603302230_joined.csv  -> both, time-aligned

`temperatures.csv` is the joined export with the columns renamed. Sensor II's
raw export has one extra sample (23:11) that is not in the joined record.

Environments (Table 1 of the paper): minutes 0-11 room, 12-29 sauna,
30-73 refrigerator (Sensor I) / freezer (Sensor II), 74-115 room.
