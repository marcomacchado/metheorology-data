from pathlib import Path
import csv
import zipfile

DATA_DIR: Path = Path("data")

MAX_FILES_PER_ZIP = 20

def find_header_row_from_lines(lines: list[str]) -> tuple[list[str], int] | None:
        for index, raw_line in enumerate(lines):
            line : str = raw_line.strip() 
            if not line:  # empty line
                continue
            upper_line : str = line.upper()
            if "DATA" in upper_line and "HORA" in upper_line:
                reader = csv.reader([line], delimiter=";")
                header_columns: list[str] = next(reader)
                header_columns = [col.strip() for col in header_columns]
                return header_columns, index
        return None
    

def read_lines_from_zip_member(zf: zipfile.ZipFile, member_name: str) -> list[str]:
        with zf.open(member_name, "r") as member_file:
            lines : list[str] = [raw_line.decode("latin-1", errors="replace") for raw_line in member_file]
            return lines
        
def classify_date_format(date_str: str) -> str:
    date_str_sripped: str = date_str.strip()
    if not date_str_sripped:
        return "EMPTY"
    if len(date_str_sripped) == 10 and date_str_sripped[4] == "/":
        return "YYYY/MM/DD"
    if len(date_str_sripped) == 10 and date_str_sripped[4] == "-" and date_str_sripped[7] == "-":
        return "YYYY-MM-DD"
    return

def classify_time_format(time_str: str) -> str:
    time_str_stripped: str = time_str.strip().upper()
    if not time_str_stripped:  # empty cell
        return "EMPTY"
    has_utc: bool = False
    if time_str_stripped.endswith("UTC"):
        has_utc = True
        time_str_stripped_clean: str = time_str_stripped[:-3].strip()
    else:
        time_str_stripped_clean = time_str_stripped

    if len(time_str_stripped_clean) == 5 and time_str_stripped_clean[2] == ":":
        return "HH:MM_UTC" if has_utc else "HH:MM"
    
    if len(time_str_stripped_clean) == 4 and time_str_stripped_clean.isdigit():
        return "HHMM_UTC" if has_utc else "HHMM"
    
    return "UNKNOWN"


def inspect_measurements_headers() -> None:
    header_signatures : dict[str, list[str]] = {}
    date_time_patterns: dict[tuple[str, str], list[str]] = {}
    files_processed: int = 0
    
    for zip_path in DATA_DIR.rglob("*.zip"):
        print(f"Opening zip file: {zip_path}")

        with zipfile.ZipFile(zip_path, "r") as zf:

            files_in_this_zip: int = 0

            for member in zf.infolist():
                member_name: str = member.filename
            
                if not member_name.lower().endswith(".csv"):
                    continue

                if files_in_this_zip >= MAX_FILES_PER_ZIP:
                    break

                file_identifier: str = f"{zip_path}:{member_name}"

                print(f"Looking inside file: {file_identifier}")

                lines: list[str] = read_lines_from_zip_member(zf=zf, member_name=member_name)
                header_result = find_header_row_from_lines(lines=lines)

                if header_result is None:
                    print(f"It wasn't possible to identify a header in this file")
                    continue

                header_columns, header_index = header_result

                header_signature: str = "|".join(header_columns)
                
                if header_signature not in header_signatures:
                    header_signatures[header_signature] = []
                
                header_signatures[header_signature].append(file_identifier)

                data_date_pattern: str | None = None
                data_time_pattern: str | None = None

                for data_line in lines[header_index+1:]:
                    if not data_line.strip():
                        continue

                    reader = csv.reader([data_line], delimiter=";")
                    row: list[str] = next(reader)
                    
                    if len(row) < 2:
                        continue
                    
                    date_str: str = row[0].strip()
                    time_str: str = row[1].strip()

                    if not date_str:
                        continue

                    data_date_pattern = classify_date_format(date_str=date_str)
                    data_time_pattern = classify_time_format(time_str=time_str)

                    pattern_key: tuple[str, str] = (data_date_pattern, data_time_pattern)

                    if pattern_key not in date_time_patterns:
                        date_time_patterns[pattern_key] = []
                    date_time_patterns[pattern_key].append(file_identifier)

                    break

                files_processed += 1
                files_in_this_zip += 1
    
    print("\n=== HEADERS FOUND ===\n")
    print(f"Measurements files processed: {files_processed}\n")
    print(f"Amount of different headers signatures: {len(header_signatures)}")

    for idx, (signature, files) in enumerate(header_signatures.items(), start=1):
        print(f"Type #{idx}")
        columns = signature.split("|")
        print(f" Number of columns: {len(columns)}")
        print(f" Columns: {columns}")

    print("\n=== DATE/TIME PATTERNS FOUND ===\n")
    print(f"Amount of different date/time patterns: {len(date_time_patterns)}\n")

    for idx, (pattern_key, files) in enumerate(date_time_patterns.items(), start=1):
        date_pattern, time_pattern = pattern_key
        print(f"Pattern #{idx}:")
        print(f"  Date format: {date_pattern}")
        print(f"  Time format: {time_pattern}")
        print(f"  Number of files using this pattern: {len(files)}")
        print(f"  Example files (up to 3):")
        for example_file in files[:3]:
            print(f"    - {example_file}")
        print()


if __name__ == "__main__":
    inspect_measurements_headers()

