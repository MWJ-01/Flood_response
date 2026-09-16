# web/ — browser prototype

Two self-contained HTML pages. No build step and no server required: open either
file directly in a browser.

| File | What it is |
| --- | --- |
| `operations_map.html` | Operations map. National state view, drill-in to state and gauge, cursor coordinate readout in degrees/minutes/seconds, timeline replay, collapsed dispatch-recommendation panel. |
| `flood_over_time.html` | Scroll-driven narrative. Six views over the same gauge records: chronological, magnitude, exceedance, event share, record parity, rainfall. |

The two pages cross-link in the top-right corner, so keep them in the same directory.

## Relationship to `src/decision_support.py`

The pages are a **design prototype of the interface**, not a front end for the
Python module. They do not import, call, or read anything from `src/`, `data/`,
or `outputs/`. The dispatch panel in `operations_map.html` reimplements the same
idea the Python prototype tests — rank team-to-area assignments, present them for
a human decision, accept/modify/reject — in JavaScript, so that the interaction
can be reviewed without a running backend.

If the two are to be joined later, the natural seam is `outputs/recommendations.csv`:
`renderDispatch()` in `operations_map.html` builds its list from an in-page array
and could instead read that CSV.

## Data status

Gauge heights, rainfall totals, dam storages, dwelling counts and previous records
are **published figures**, each tagged in the interface with the source it was read
from; the full list with links is at the foot of both pages. Where a cited source
publishes no figure for a field, the interface prints `not published` rather than
an estimate.

Everything else is **modelled for the prototype** and tagged `MOD`:

- inundation polygons and depth-at-cursor;
- interpolation between published observations along the timeline;
- all dispatch recommendations, routes, arrival times and exposure indices.

The inundation shapes are **not official flood extents**. As with the Python
prototype, this is not for real emergency operations.

## External dependencies

Both pages fetch from CDNs at run time, so first load needs a network connection:

- d3 v7.9.0 (unpkg)
- IBM Plex Sans / Mono / Serif (Google Fonts)
- Natural Earth vector geometry, public domain (jsDelivr, with a raw.githubusercontent
  fallback): 1:50m admin-1 state boundaries for the national view; 1:10m coastline and
  river centrelines loaded on drill-in.

To run fully offline, vendor those four files locally and repoint the
`<script src>`, the stylesheet `<link>`, and the `U_STATES50` / `U_COAST10` /
`U_RIVERS10` URL arrays near the top of the script block in `operations_map.html`.
