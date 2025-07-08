#!/bin/bash

# Script to check the availability of websites and log the results
# Array of websites to check
WEBSITES=(
  "https://google.com"
  "https://facebook.com"
  "https://twitter.com"
)

# Log file name
LOG_FILE="website_status.log"

# Clear the previous log file if it exists
> "$LOG_FILE"

# Check each website
for SITE in "${WEBSITES[@]}"; do
  # Using curl with:
  # -s: silent mode
  # -L: follow redirects
  # -o /dev/null: discard body
  # -w "%{http_code}": output only HTTP status code
  STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" -L "$SITE")

  if [[ "$STATUS_CODE" == "200" ]]; then
    echo "<$SITE> is UP" | tee -a "$LOG_FILE"
  else
    echo "<$SITE> is DOWN" | tee -a "$LOG_FILE"
  fi
done

# Final message
echo "Results have been written to $LOG_FILE"
