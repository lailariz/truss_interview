import csv
import sys
import re
import fileinput
from datetime import datetime, timedelta

class NormalizeCSV:
  """Normalize an input CSV file as specified in the README"""
  def __init__(self, in_file):
    self.in_file = in_file.decode('utf-8', 'replace')

  def normalize(self):
    """Process each input line and send it to STDOUT according to the requirements"""
    reader = csv.reader(self.in_file.splitlines())
    writer = csv.writer(sys.stdout)

    # Header row
    writer.writerow(next(reader))
    for row in reader:
      try:
        # Col 1 - Timestamp
        eastern_time = None
        try:
          eastern_time = self.timestampPSTtoEST(row[0])
        except ValueError as e:
          print("Timestamp written in an invalid format:", str(e), file=sys.stderr)
          continue

        # Col 2 - Address
        address = row[1]

        # Col 3 - Zipcodes
        zip_code = self.prefixZipCode(row[2])

        # Col 4 - FullName
        name = row[3].upper()

        # Col 5, 6, 7 - FooDuration, BarDuration, TotalDuraction
        foo_time = self.getDeltaTime(row[4]).total_seconds()
        bar_time = self.getDeltaTime(row[5]).total_seconds()
        total_time = foo_time + bar_time

        # Col 8 - Notes
        note = row[7]

        writer.writerow([eastern_time, address, zip_code, name, foo_time,
          bar_time, total_time, note])

      except Exception as e:
        print("Unknown error, skipping row", str(e), file=sys.stderr)
        continue

  def prefixZipCode(self, zip_string):
    """Left pad zeros to zip codes up to 5 digits"""
    return zip_string.zfill(5)

  def timestampPSTtoEST(self, date_string):
    """Parse the input date string and convert from PST to EST"""
    parsed_time = datetime.strptime(date_string, "%m/%d/%y %I:%M:%S %p")
    return (parsed_time + timedelta(hours=3)).isoformat()

  def getDeltaTime(self, time_string):
    """Parse delta time string and return timedelta object"""
    t = re.findall(r"[0-9]+", time_string)
    t = [int(component) for component in t]
    return timedelta(hours=t[0], minutes=t[1], seconds=t[2], milliseconds=t[3])

def main():
    in_file = sys.stdin.buffer.read()
    if not in_file:
      print("Please provide an input file. 'python process_csv.py < sample.csv'", file=sys.stderr)
      return 1

    obj = NormalizeCSV(in_file)
    obj.normalize()
  
if __name__ == "__main__":
  main()
