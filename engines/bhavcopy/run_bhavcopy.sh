#!/usr/bin/env bash
set -e

DATE=${1:-$(date +"%d%m%Y")}
YEAR=${DATE:4:4}
MONTH=${DATE:2:2}

DIR="data/bhavcopy"
ZIP="$DIR/bhav_${DATE}.zip"

mkdir -p "$DIR"

URL="https://nsearchives.nseindia.com/content/historical/EQUITIES/$YEAR/$MONTH/cm${DATE}bhav.csv.zip"

echo "Downloading Bhavcopy for $DATE"

curl -L \
  --retry 5 \
  --retry-delay 3 \
  --connect-timeout 15 \
  -H "User-Agent: Mozilla/5.0" \
  -H "Accept: application/zip" \
  -o "$ZIP" \
  "$URL"

SIZE=$(stat -c%s "$ZIP" 2>/dev/null || echo 0)

if [ "$SIZE" -lt 500000 ]; then
  echo "Bhavcopy unavailable or blocked"
  rm -f "$ZIP"
  exit 1
fi

echo "Extracting bhavcopy"

unzip -o "$ZIP" -d "$DIR" >/dev/null

echo "Bhavcopy Ready"
