import time
import os
from prometheus_client import start_http_server, Gauge

LATENCY_GAUGE = Gauge('cupcarbon_latency', 'Latency of transmission', ['node_id'])
BATTERY_GAUGE = Gauge('cupcarbon_battery', 'Current battery Level', ['node_id'])


def tail_logs(filename):
    start_http_server(8000)
    print(f"Prometheus metrics available at http://localhost:8000")

    with open(filename, "r") as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            if "METRIC|" in line:
                parse_and_export(line)


def parse_and_export(line):
    try:
        # Example line: METRIC|node_1|battery=95.5|temp=22.1
        parts = line.strip().split("|")
        node_id = parts[1]

        latency_val = float(parts[2].split("=")[1])
        LATENCY_GAUGE.labels(node_id=node_id).set(latency_val)

        # Parse battery
        # batt_val = float(parts[2].split("=")[1])
        # BATTERY_GAUGE.labels(node_id=node_id).set(batt_val)

        # Parse temp
        # temp_val = float(parts[3].split("=")[1])
        # TEMP_GAUGE.labels(node_id=node_id).set(temp_val)

        # print(f"Updated {node_id}: Batt={batt_val}, Temp={temp_val}")
    except Exception as e:
        print(f"Parsing error: {e}")


if __name__ == "__main__":
    # Path to CupCarbon's output (usually in results/ or logs/ folder)
    LOG_PATH = "path/to/cupcarbon/logs/simulation_output.log"
    tail_logs(LOG_PATH)
