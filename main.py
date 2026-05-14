import time
import os
import paho.mqtt.client as mqtt
from prometheus_client import start_http_server, Gauge

PACKET_SIZE_GAUGE = Gauge('cupcarbon_packet_size', 'Packet Size', ['node_id'])
TRANSMISSION_TIME_GAUGE = Gauge('cupcarbon_transmission_time', 'Transmission Time', ['node_id'])
BANDWIDTH_USAGE_GAUGE = Gauge('cupcarbon_bandwidth_usage', 'Bandwidth Usage', ['node_id'])
LATENCY_GAUGE = Gauge('cupcarbon_latency', 'Latency of transmission', ['node_id'])
JITTER_GAUGE = Gauge('cupcarbon_jitter', 'Jitter', ['node_id'])
PACKET_LOSS_RATE_GAUGE = Gauge('cupcarbon_packet_loss', 'Packet Loss Rate', ['node_id'])
ENERGY_USAGE_GAUGE = Gauge('cupcarbon_energy_usage', 'Energy Usage', ['node_id'])
BATTERY_GAUGE = Gauge('cupcarbon_battery', 'Current battery Level', ['node_id'])
PACKET_SEND_RATE_GAUGE = Gauge('cupcarbon_packet_send_rate', 'Packet Send Rate', ['node_id'])

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "cupcarbon/data"


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        print(f"Received message on {msg.topic}: {payload}")

        parse_and_export(payload)
    except Exception as e:
        print(f"Error handling message: {e}")

    pass


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


def start():
    start_http_server(8000)
    print(f"Prometheus metrics available at http://localhost:8000")

    client = mqtt.Client()
    client.on_message = on_message

    print(f"Connecting to MQTT Broker: ${MQTT_BROKER} ...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.subscribe(MQTT_TOPIC)

    client.loop_forever()


def parse_and_export(line):
    try:
        # Example line: METRIC|node_1|packet_size=0.0|transmission_time=0.0
        parts = line.strip().split("|")
        node_id = parts[1].strip()

        packet_size_val = float(parts[2].split("=")[1])
        PACKET_SIZE_GAUGE.labels(node_id=node_id).set(packet_size_val)

        transmission_time_val = float(parts[3].split("=")[1])
        TRANSMISSION_TIME_GAUGE.labels(node_id=node_id).set(transmission_time_val)

        bandwidth_usage_val = float(parts[4].split("=")[1])
        BANDWIDTH_USAGE_GAUGE.labels(node_id=node_id).set(bandwidth_usage_val)

        latency_val = float(parts[5].split("=")[1])
        LATENCY_GAUGE.labels(node_id=node_id).set(latency_val)

        jitter_val = float(parts[6].split("=")[1])
        JITTER_GAUGE.labels(node_id=node_id).set(jitter_val)

        packet_loss_rate_val = float(parts[7].split("=")[1])
        PACKET_LOSS_RATE_GAUGE.labels(node_id=node_id).set(packet_loss_rate_val)

        energy_usage_val = float(parts[8].split("=")[1])
        ENERGY_USAGE_GAUGE.labels(node_id=node_id).set(energy_usage_val)

        battery_val = float(parts[9].split("=")[1])
        BATTERY_GAUGE.labels(node_id=node_id).set(battery_val)

        packet_send_rate_val = float(parts[10].split("=")[1])
        PACKET_SEND_RATE_GAUGE.labels(node_id=node_id).set(packet_send_rate_val)
    except Exception as e:
        print(f"Parsing error: {e}")


if __name__ == "__main__":
    start()
