#!user/bin/env python3

######################################
# Submitted By: Neel Kumar           #
#                                    #
# Consulted the lab lecture and code #
# No other collaboration             #
#######################################

import socket, time, sys
from multiprocessing import Process

# get_remote_ip() method
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

# handle_request() method
def handle_request(addr, conn):
    print(f"[CONNECTED BY: {addr}]")
    BUFFER_SIZE = 1024
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():

    # establish localhost, extern_host (google), port, buffer size
    HOST = "localhost"
    PORT = 8001
    BUFFER_SIZE = 1024
    extern_host = "www.google.com"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start: # (connects to local host)
        # bind and set to listending mode
        print("[STARTING PROXY SERVER]")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            # accept incoming connections from proxy_start, print information about connection
            conn_start, addr_start = proxy_start.accept()
            print(f"[CONNECTED BY: {addr_start}]")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end: #(connects to Google)
                # get remote ip of google, connect proxy_end to it
                print("[CONNECTING TO EXTERN_HOST]")
                remote_ip = get_remote_ip(extern_host)
                extern_port = 80
                proxy_end.connect((remote_ip, extern_port))

                #
                send_full_data = conn_start.recv(BUFFER_SIZE)
                print(f"[SENDING RECEIVED DATA {send_full_data} TO GOOGLE]")
                proxy_end.sendall(send_full_data)

                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                print(f"[SENDING RECEIVED DATA {data} TO CLIENT]")
                conn_start.send(data)
                #

                # multiprocessing.
                # allow for multiple connections with a process daemon
                # make sure to set target=handle_request when creating the Process
                p = Process(target=handle_request, args=(addr_start, conn_start))
                p.daemon = True
                p.start()
                print(f"[STARTED PROCESS: {p}]")

            # close the connection!
            conn_start.close()

if __name__ == "__main__":
    main()