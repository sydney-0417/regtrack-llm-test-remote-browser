#!/bin/bash
# Start Xvfb (vMonitor) on display port :99 in the background
Xvfb :99 -screen 0 1280x720x24 -ac +extension GLX +render -noreset &

# Wait up to 3 seconds for the socket file to actually exist in the system
for i in {1..30}; do
    if [ -S /tmp/.X11-unix/X99 ]; then
        break
    fi
    sleep 0.1
done

# Run the actual browser process with structural sandbox bypass flags
# 0.0.0.0: chromium listens to all network interfaces
exec chromium \
  --no-sandbox \
  --disable-dev-shm-usage \
  --remote-debugging-host=0.0.0.0 \
  --remote-debugging-port=${DEBUG_PORT:-9222} \
  --remote-allow-origins=* \
  --user-data-dir=/tmp/chrome-profile
