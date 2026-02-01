import zipfile
import csv
from pathlib import Path
import scripts.inspect_measurements_headers as auxfunc
from parsers.observation_parser import parse_observation_row


DATA_DIR: Path = Path("data")
ZIP_FILE_NAME = "2018.zip"
CSV_MEMBER_NAME = "2018/INMET_CO_DF_A047_PARANOA (COOPA-DF)_01-01-2018_A_31-12-2018.CSV"
MAX_ROWS_TO_PARSE = 5

def demo_parse_single_file() -> None:
    zip_path: Path = DATA_DIR / ZIP_FILE_NAME

    with zipfile.ZipFile(zip_path, "r") as zf:
        lines: list[str] = auxfunc.read_lines_from_zip_member(zf=zf, member_name=CSV_MEMBER_NAME)

    header_result = auxfunc.find_header_row_from_lines(lines=lines)

    header_columns, header_index = header_result

    date_pattern: str | None = None
    time_pattern: str | None = None

    first_data_raw_line = lines[header_index+1]

    if not first_data_raw_line.strip():
        return None

    reader = csv.reader([first_data_raw_line], delimiter=";")
    row: list[str] = next(reader)

    date_str: str = row[0].strip()
    time_str: str = row[1].strip()

    if not date_str:
        return  None

    date_pattern = auxfunc.classify_date_format(date_str=date_str)
    time_pattern = auxfunc.classify_time_format(time_str=time_str)

    rows_parsed: int = 0
    for raw_line in lines[header_index+1:]:

        if rows_parsed >= MAX_ROWS_TO_PARSE:
            break
        
        reader = csv.reader([raw_line], delimiter=";")
        row: list[str] = next(reader)

        observation = parse_observation_row(row=row, date_pattern=date_pattern, time_pattern=time_pattern)

        print(observation)
        rows_parsed += 1
    
if __name__ == "__main__":
    demo_parse_single_file()


        


