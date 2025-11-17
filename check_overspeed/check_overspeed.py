import numpy as np
import pandas as pd
from pyrosm import OSM
from shapely.geometry import LineString, Point
from scipy.spatial import KDTree

# ---------------------------------------------------------
# 1. LOAD OSM ROADS
# ---------------------------------------------------------
osm = OSM("tunisia-latest.osm.pbf")   # <- change if needed

roads = osm.get_data_by_custom_criteria(
    {"highway": True},
    relations=False
)

# Keep only what we need
roads = roads[['geometry', 'highway', 'maxspeed']].dropna(subset=['geometry'])

# Clean maxspeed (convert from strings like '50', '80', '50 mph')
def parse_maxspeed(x):
    if x is None:
        return np.nan
    try:
        # handles "50", "80", "100"
        return float(str(x).split()[0])
    except:
        return np.nan

roads['maxspeed'] = roads['maxspeed'].apply(parse_maxspeed)

# Fill missing speed limits logically (optional)
roads['maxspeed'] = roads['maxspeed'].fillna(50)

# ---------------------------------------------------------
# 2. BUILD SAMPLE POINTS FOR KDTREE
# ---------------------------------------------------------
points = []
point_to_road = []

for idx, row in roads.iterrows():
    geom = row['geometry']
    
    # If geometry is a LineString
    if isinstance(geom, LineString):
        xs, ys = geom.xy
        for i in range(len(xs)):
            points.append((ys[i], xs[i]))   # (lat, lon)
            point_to_road.append(idx)
    
    # If MultiLineString
    else:
        try:
            for line in geom:
                xs, ys = line.xy
                for i in range(len(xs)):
                    points.append((ys[i], xs[i]))
                    point_to_road.append(idx)
        except:
            pass

points = np.array(points)

tree = KDTree(points)

print("KD-tree ready. Total points:", len(points))

# ---------------------------------------------------------
# 3. FUNCTION: GET SPEED LIMIT FROM A GPS POSITION
# ---------------------------------------------------------
def get_speed_limit(lat, lon):
    # Find nearest road point
    dist, idx = tree.query((lat, lon))
    road_index = point_to_road[idx]
    road_row = roads.loc[road_index]
    return road_row['maxspeed'], road_row['highway']


# ---------------------------------------------------------
# 4. FUNCTION: CHECK OVERSPEED
# ---------------------------------------------------------
def check_speed(current_speed, lat, lon):
    limit, road_type = get_speed_limit(lat, lon)
    
    # tolerance rule
    tolerance = max(5, limit * 0.05)
    
    if current_speed > limit + tolerance:
        return {
            "status": "OVER_SPEED",
            "speed": current_speed,
            "limit": limit,
            "excess": current_speed - limit,
            "road_type": road_type
        }
    else:
        return {
            "status": "OK",
            "speed": current_speed,
            "limit": limit,
            "road_type": road_type
        }


# ---------------------------------------------------------
# 5. EXAMPLE USAGE
# ---------------------------------------------------------
gps_points = [
    (36.80625, 10.18105, 48),
    (36.80630, 10.18120, 45),
    (36.80633, 10.18140, 60)
]

for lat, lon, speed in gps_points:
    print(check_speed(speed, lat, lon))
