import math


def bearing(lat1, lon1, lat2, lon2):
    # lat1&lon1 is our base station
    lat1_rad = lat1 * math.pi / 180
    lon1_rad = lon1 * math.pi / 180
    lat2_rad = lat2 * math.pi / 180
    lon2_rad = lon2 * math.pi / 180

    y = math.sin(lon2_rad - lon1_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - \
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)

    brng = math.atan2(y, x) * 180 / math.pi
    if brng < 0:
        brng = brng + 360

    return float(brng)


if __name__ == '__main__':
    print(bearing(42.72335, -73.27792, 42.6648, -73.7787))
