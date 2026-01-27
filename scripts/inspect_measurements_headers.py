from pathlib import Path
import csv
import zipfile

DATA_DIR: Path = Path("data")

MAX_FILES_PER_ZIP = 10

def find_header_row_from_lines(lines: list[str]) -> list[str] | None:
        for raw_line in lines:
            line : str = raw_line.strip() 
            if not line:  # empty line
                continue
            upper_line : str = line.upper()
            if "DATA" in upper_line and "HORA" in upper_line:
                reader = csv.reader([line], delimiter=";")
                header_columns: list[str] = next(reader)
                header_columns = [col.strip() for col in header_columns]
                return header_columns
        return None
    

def read_lines_from_zip_member(zf: zipfile.ZipFile, member_name: str) -> list[str]:
        with zf.open(member_name, "r") as member_file:
            lines : list[str] = [raw_line.decode("latin-1", errors="replace") for raw_line in member_file]
            return lines
        

def inspect_measurements_headers() -> None:
    header_signatures : dict[str, list[str]] = {}
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

                lines: str = read_lines_from_zip_member(zf=zf, member_name=member_name)
                header_columns = find_header_row_from_lines(lines=lines)

                if header_columns is None:
                    print(f"It wasn't possible to identify a header in this file")
                    continue

                header_signature: str = "|".join(header_columns)
                
                if header_signature not in header_signatures:
                    header_signatures[header_signature] = []
                
                header_signatures[header_signature].append(file_identifier)

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

if __name__ == "__main__":
    inspect_measurements_headers()

