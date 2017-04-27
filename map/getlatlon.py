from PIL.ExifTags import TAGS, GPSTAGS


def _convert_to_degress(x):
    return ((float(x[0][0]) / x[0][1]) + ((float(x[1][0]) / x[1][1]) / 60.0) + ((float(x[2][0]) / x[2][1]) / 3600.0))


def get_lat_lon(image):
    lat = None
    lon = None
    exif_data = {}
    try:
        info = image._getexif()
    except:
        return None
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]
        gps_latitude = gps_info.get("GPSLatitude", None)
        gps_latitude_ref = gps_info.get("GPSLatitudeRef", None)
        gps_longitude = gps_info.get("GPSLongitude", None)
        gps_longitude_ref = gps_info.get("GPSLongitudeRef", None)

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return (lat, lon)
