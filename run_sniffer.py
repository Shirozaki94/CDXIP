import subprocess

def run_sniffer():
    cmd_command = ['python', 'packet_sniffer.py']
    process = subprocess.Popen(cmd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline().decode().strip()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)

if __name__ == '__main__':
    run_sniffer()
