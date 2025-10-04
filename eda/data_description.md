
# Data source and import 

The analysis is based on the network infiltration dataset (NSL-KDD99) downloaded from [kaggle](https://www.kaggle.com/datasets/kaggleprollc/nsl-kdd99-dataset/data).

When importing the data with pandas I used the following code to include the column names:

```
import pandas as pd

file_name_train_data = "KDDTrain+.txt"
file_name_test_tata = "KDDTest+.txt"
file_path = "path_to_file"

column_names = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate" "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "attack_type", "difficulty_level"
]

# load data as df
train_data = pd.read_csv(file_path + file_name_train_data,  names=column_names)
test_data = pd.read_csv(file_path + file_name_test_tata, names=column_names)

```
</br>

# Data description 

Overview and description of the variables in the dataset. Will be updated continously...
    

| Column name | Column values| Description |
| --- | ----------- |---|
| duration | - | Duration of the connection in seconds |
| protocol_type | categorical, 3 types | Type of protocol ([TCP](#tcp---transmission-control-protocol), [UDP](#udp---user-datagram-protocol), [ICMP](#icmp---internet-control-message-protocol)) |
| service |  categorical, 70 different services | Network service on the destination (http, ftp, smtp)  |
| flag |  categorical, 11 different flags | Status of connection</br>('SF', 'S0', 'REJ', 'RSTR', 'SH', 'RSTO', 'S1', 'RSTOS0', 'S3', 'S2', 'OTH')  |
| src_bytes |  - | Bytes sent from source to destination |
| dst_bytes |  - | Bytes sent from destination to source |
| land | bool | 1: connection to/from same host <br/>0: otherwise |
| wrong_fragment |  0, 1, 3 | Nr of wrong fragments |
| urgent | 0-3 | Nr of urgent packets |
| hot | 0-77 | Nr of hot indicatiors |
| num_failed_logins |  0-5 | Nr of failed login attempts |
| logged_in |  bool  | 1: successfully logged in <br/>0: otherwise|
| num_compromised |  - | Nr of compromised conditions |
| root_shell |  bool | 1: root shell obtained <br/>0: otherwise |
| su_attempted |  0, 1, 2 | 'su root' command attempt |
| num_root |  - | Nr of root accesses |
| num_file_creations |  - | Nr of file creation operations |
| num_shells |  0,1,2 | Nr of shell prompts invoked |
| num_access_files |  0-9 | Nr of access file control operations |
| num_outbound_cmds |  always 0 | Nr of outbound commands |
| is_host_login |  bool | 1: login belongs to host </br>0: otherwise |
| is_guest_login |  bool | 1: login from guest account <br/>0: otherwise |
| count |  - | Nr of connections to **same host** as current connection in past 2s |
| srv_count |  - | Nr of connections to the **same service** as current connection in past 2s |
| serror_rate |  - | Percentage of connections with **SYN** errors |
| srv_error_rate |  - | Percentage of connections with **SYN** errors for same service|
| rerror_rate |  - | Percentage of connections with **REJ** errors |
| srv_rerror_rate |  - | Percentage of connections with **REJ** errors for same service|
| same_srv_rate |  - | Percentage of connections to the same service|
| diff_srv_rate |  - | Percentage of connections to different services|
| srv_diff_host_rate |  - | Percentage of connections to different hosts|
| dst_host_count |  - | Count of destinations hosts accessed|
| dst_host_srv_count |  - | Count of connections to the same service at the destination|
| dst_host_same_srv_rate |  - | Percentage of connections to the **same service** at the destination|
| dst_host_diff_srv_rate |  - | Percentage of connections to **different services** at the destination|
| dst_host_same_src_port_rate |  - | Percentage of connections to same source port |
| dst_host_srv_diff_host_rate |  - | Percentage of different hosts connected via same service |
| dst_host_serror_rate |  - | Percentage of **SYN** errors at the destination host |
| dst_host_srv_serror_rate |  - | Percentage of **SYN** errors for the same service at the destination |
| dst_host_rerror_rate |  - | Percentage of **REJ** errors at the destination host |
| dst_host_srv_rerror_rate |  - | Percentage of **REJ** errors for the same service at the destination |
| attack_type |  categorical, 23 different types | normal, neptune, ... |
| difficulty_level |  - | - |

</br>
</br>


#  Background information 

Some background knowledge and variables explained in more detail. 

## TCP/IP model

- The Transmission Control Protocol/ Internet Protocol model defines data transmission across networks (modern internet) and consists of 4 layers:
    1. **Application**: handles high lvl protocols like HTTP, FTP, SSH, DNS
    2. **Transport**: enables data transfer, reliable (via TCP) or fast (via UDP) 
    3. **Internet**: manages adressing and routing with IP and ICMP
    4. **Network accees**: deals with physical transmission methods (Ethernet, WiFi)

## TCP - Transmission control protocol

- Connection-oriented protocol that uses reliable data transfer (correct sequence of data packets)
    1. Establish connection (via 3-way handshake)
        - **Synchronize**: Client sends a SYN packet to initiate a connection
        - **Synchronize-acknowledge**: Server responds with a SYN-ACK packet
        - **Acknowledge**: Client sends ACK packet to finalize connction
    2. Transmit data
        - Data is divided into packets and transmitted in sequence
        - Receiver acknowledges received packets
        - Retransmission of missing packets
    3. Terminate connetion 
        - Either party can close the connection using a FIN-ACK exchange

## UDP - User Datagram Protocol
- Connectionless protocol that prioritises fast and lightweight communication over reliability
    1. Sender transmits data packets directly to recipient
    2. Recipient receives packets without acknowledging 
    3. No retransmission of lost packets

## ICMP - Internet Control Message Protocol
- Supporting protocol used to send error messages and diagnostic info, no data transmission
- Common ICMP messages:
    1. Echo request and reply: unsed in `ping` to test connectivity
    2. Destination unreachable: indicates routing issues
    3. Time exceeded: used in `traceroute` to map network paths
- Security issues with ICMP exploits:
    - attacks like ICMP flooding and Ping of Death can lead to firewall restrictions on IMCP traffic

</br>
</br>

## Overview networking protocols 

|Feature| TCP| UDP| ICMP|
| --- | ----------|----|----|
|Connection type| **connection-oriented**,</br> establish connection before data transmission|**connectionless**,</br>no handshake or acknowledgement|message-based|
|Reliability|**High**</br>(data integrety ensured by acknowledgements, retransmissions, error checking with checksums)|**None**</br>(best effort, no retransmissions)|**No data transfer**</br>(error reporting)|
|Speed|**Slow**</br>(due to reliability checks)|**Fast**</br>(minimal overhead)|**N/A**</br>(control message only)|
|Use cases|Web browsing (HTTP/HTTPS),</br>Email (SMTP, IMAP, POP3),</br>File transfer (FTP,SFTP)|Streaming, Gaming, Voice over IP calls (VoIP), DNS queries|Network diagnostics|

</br>
</br>

# References

**Dataset**: </br>

    M. Tavallaee, E. Bagheri, W. Lu, and A. Ghorbani, “A Detailed Analysis of the KDD CUP 99 Data Set,” Submitted to Second IEEE Symposium on Computational Intelligence for Security and Defense Applications (CISDA), 2009.

[Information about networking protocols](https://www.linuxjournal.com/content/linux-networking-protocols-understanding-tcpip-udp-and-icmp)