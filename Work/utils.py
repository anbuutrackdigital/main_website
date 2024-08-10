from django.contrib.gis.geos import Point

def get_location_coordinates(point):
    if isinstance(point, Point):
        return point.x, point.y
    return "Unknown", "Unknown"
