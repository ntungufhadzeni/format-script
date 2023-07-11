from haversine import haversine, Unit


new_stops = {
             '100A':{'lat': -23.837778, 'lon': 29.395556},
             '102A':{'lat': -23.845556, 'lon': 29.387778},
             '104A':{'lat': -23.853889, 'lon': 29.388056},
             '105A':{'lat': -23.853611, 'lon': 29.397778},
             '403A':{'lat': -23.916944, 'lon': 29.428889},
             '405A':{'lat': -23.910833, 'lon': 29.435000},
             '406A':{'lat': -23.908056, 'lon': 29.434722},
             '406B':{'lat': -23.910833, 'lon': 29.438333},
             '301A':{'lat': -23.906389, 'lon': 29.463056},
             '302A':{'lat': -23.905833, 'lon': 29.473611},
             '304A':{'lat': -23.913056, 'lon': 29.479722},
             '304A2':{'lat': -23.912500, 'lon': 29.482222},
             '307A':{'lat': -23.91194, 'lon': 29.500278},
             '310-1':{'lat': -23.901389, 'lon': 29.493611},
             '311A':{'lat': -23.905833, 'lon': 29.481389},
             '312A':{'lat': -23.907500, 'lon': 29.473333},
             '313A':{'lat': -23.909444, 'lon': 29.463333},
             }

def get_new_stop(lat, lon):
    lat = float(lat)
    lon = float(lon)
    
    stop1 = (lat, lon)
    
    closest_stop = ''
    distance = 300
    
    for stop in new_stops.keys():
        stop2 = (new_stops[stop]['lat'],new_stops[stop]['lon'])
        dist = haversine(stop1, stop2, unit=Unit.METERS)
        
        if dist <= distance:
            closest_stop = stop
            distance = dist     
    return closest_stop


def is_layover(arg_lat, arg_lon):
    arg_lat = float(arg_lat)
    arg_lon = float(arg_lon)

    min_lat = -23.89813
    max_lat = -23.89937
    min_lon = 29.44261
    max_lon = 29.44507

    if max_lat < arg_lat < min_lat:
        if min_lon < arg_lon < max_lon:
            return True
        else:
            return False

    else:
        return False


def is_fuel_wise(arg_lat, arg_lon):
    arg_lat = float(arg_lat)
    arg_lon = float(arg_lon)

    min_lat = -23.89453
    max_lat = -23.89581
    min_lon = 29.44261
    max_lon = 29.44393

    if max_lat < arg_lat < min_lat:
        if min_lon < arg_lon < max_lon:
            return True
        else:
            return False

    else:
        return False
