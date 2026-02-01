from datetime import datetime
from typing import Any

# Converts a numeric value in the CSV files to float 
def parse_float_cell(raw_value: str) -> float | None:
    value_str: str = raw_value.strip()
    if not value_str:
        return None
    if value_str == "-9999":
        return None
    normalized: str = value_str.replace(",",".")
    try:
        return float(normalized)
    except:
        print(f"Couldn't normalize {normalized} to float")
        return None
    

# Combines date and time field to a standard UTC value
def parse_timestamp_utc(date_str: str, time_str: str, date_pattern: str, time_pattern: str) -> datetime:
    date_stripped = date_str.strip()
    time_stripped = time_str.strip().upper()

    if date_pattern == "YYYY-MM-DD":
        date_obj = datetime.strptime(date_stripped, "%Y-%m-%d").date()
    elif date_pattern == "YYYY/MM/DD":
        date_obj = datetime.strptime(date_stripped, "%Y/%m/%d").date()
    else:
        raise ValueError(f"Unsupported date pattern: '{date_pattern} for value '{date_str}")
    

    if time_stripped.endswith("UTC"):
        time_clean: str = time_stripped[:-3].strip()
    else:
        time_clean = time_stripped

    if time_pattern in ("HH:MM", "HH:MM_UTC"):
        time_obj = datetime.strptime(time_clean, "%H:%M").time()
    elif time_pattern in ("HHMM", "HHMM_UTC"):
        time_obj = datetime.strptime(time_clean, "%H%M").time()
    else:
        raise ValueError(f"Unsupported time pattern {time_pattern} for value {time_str}")
    
    timestamp_utc: datetime = datetime.combine(date_obj, time_obj)
    return timestamp_utc

# Parses a CSV row to a dictionary
def parse_observation_row(row: list[str], date_pattern: str, time_pattern: str) -> dict[str, Any]:
    if len(row) < 19:
        raise ValueError(f"Row has too few columns")
    
    date_str: str = row[0]
    time_str: str = row[1]

    timestamp_utc: datetime = parse_timestamp_utc(date_str, time_str, date_pattern, time_pattern)
    precipitation_mm = parse_float_cell(row[2])
    pressure_station_mb = parse_float_cell(row[3])
    pressure_max_prev_hour_mb = parse_float_cell(row[4])
    pressure_min_prev_hour_mb = parse_float_cell(row[5])
    global_radiation_kj_m2 = parse_float_cell(row[6])
    temperature_air_c = parse_float_cell(row[7])
    dew_point_c = parse_float_cell(row[8])
    temperature_max_last_hour_c = parse_float_cell(row[9])
    temperature_min_last_hour_c = parse_float_cell(row[10])
    dew_point_max_last_hour_c = parse_float_cell(row[11])
    dew_point_min_last_hour_c = parse_float_cell(row[12])
    humidity_max_last_hour = parse_float_cell(row[13])
    humidity_min_last_hour = parse_float_cell(row[14])
    humidity_rel_percent = parse_float_cell(row[15])
    wind_direction_deg = parse_float_cell(row[16])
    wind_gust_ms = parse_float_cell(row[17])
    wind_speed_ms = parse_float_cell(row[18])

    observation: dict[str, Any] = {
        "timestamp_utc": timestamp_utc,

        "precipitation_mm": precipitation_mm,

        "pressure_station_mb": pressure_station_mb,
        "pressure_max_prev_hour_mb": pressure_max_prev_hour_mb,
        "pressure_min_prev_hour_mb": pressure_min_prev_hour_mb,

        "global_radiation_kj_m2": global_radiation_kj_m2,

        "temperature_air_c": temperature_air_c,
        "dew_point_c": dew_point_c,
        "temperature_max_last_hour_c": temperature_max_last_hour_c,
        "temperature_min_last_hour_c": temperature_min_last_hour_c,
        "dew_point_max_last_hour_c": dew_point_max_last_hour_c,
        "dew_point_min_last_hour_c": dew_point_min_last_hour_c,

        "humidity_max_last_hour": humidity_max_last_hour,
        "humidity_min_last_hour": humidity_min_last_hour,
        "humidity_rel_percent": humidity_rel_percent,

        "wind_direction_deg": wind_direction_deg,
        "wind_gust_ms": wind_gust_ms,
        "wind_speed_ms": wind_speed_ms,
    }

    return observation