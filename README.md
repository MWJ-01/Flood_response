# Flood Response Decision Support Prototype

This is an early thesis prototype for a Brisbane flood case study. It tests one decision:

> Given several affected areas and limited response teams, which team should be sent to which area next, and which route can it use?

The current version is intentionally small. It calculates a priority for each affected area, removes roads above a vehicle's flood-depth limit, finds a route, and ranks possible team-area assignments.

## Run the prototype

```bash
python run_demo.py
python -m unittest discover -s tests -v
```

The demo uses only Python's standard library.

## Data status

All CSV files in `data/` are **synthetic test data**. They are not real emergency calls, real vehicle locations, or current road closures.

The later Brisbane case study is planned to use:

- Brisbane City Council historical flood extent and official flood-study outputs;
- OpenStreetMap road geometry;
- ABS Census area-level vulnerability information; and
- synthetic requests and team availability unless authorised operational data becomes available.

Historical and modelled flood data will not be described as live data. The prototype is not for real emergency operations.

## Folder structure

```text
student-flood-response-dss/
|-- data/                     synthetic test scenario
|-- src/decision_support.py   priority, routing and assignment logic
|-- tests/                    four small unit tests
|-- outputs/                  generated recommendation CSV
|-- run_demo.py               runs the example
`-- README.md
```

## Current limits

The priority weights and vehicle-depth limits are research assumptions. They need sensitivity testing and expert review. A human coordinator must make the final decision.
