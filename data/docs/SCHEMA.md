# Schema
All timestamps are in UTC.
All identifiers are pseudonymized and consistent across files.
## Common Columns
| Column | Description |
|--------|-------------|
timeUtc | UTC timestamp |
node | pseudonymized node ID |
metric | metric name |
value | numeric value |
gpu | GPU index |
device | GPU device label |
uuid | pseudonymized GPU UUID |
instance | pseudonymized exporter instance |
modelName | GPU model |
driverVersion | driver version |

## Incident Table
incident_events.csv

| Column | Description |
|--------|-------------|
node | pseudonymized node |
incidentDate | incident time |
category | failure category |
collectStart | telemetry start |
collectEnd | telemetry end |

## Manifest
manifest.csv
Per-file statistics and coverage.