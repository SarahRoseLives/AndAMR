import subprocess
import socket

def start_rtlamr_and_send_udp():
    try:
        # Start rtlamr subprocess
        proc = subprocess.Popen(
            ["$HOME/go/bin/rtlamr"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True
        )

        # Set up UDP socket to send data
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while True:
            output = proc.stdout.readline().strip()
            if not output:
                break

            # Here, parse 'output' as needed and send as UDP packet
            udp_sock.sendto(output.encode(), ('localhost', 8585))

        proc.terminate()

    except Exception as e:
        print(f"Error starting RTLAMR or sending UDP: {e}")

if __name__ == "__main__":
    start_rtlamr_and_send_udp()
