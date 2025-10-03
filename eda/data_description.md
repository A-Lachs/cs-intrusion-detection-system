
# Data desciption

Network infiltration dataset (NSL-KDD99) from [kaggle](https://www.kaggle.com/datasets/kaggleprollc/nsl-kdd99-dataset/data).

**Reference**: </br>
    M. Tavallaee, E. Bagheri, W. Lu, and A. Ghorbani, “A Detailed Analysis of the KDD CUP 99 Data Set,” Submitted to Second IEEE Symposium on Computational Intelligence for Security and Defense Applications (CISDA), 2009.
    

| Column name | Column values| Description |
| --- | ----------- |---|
| duration | - | Duration of the connection in seconds |
| protocol_type | categorical, 3 types | Type of protocol (tcp, udp, icmp) |
| service |  categorical, 70 different services | Network service on the destination (http, ftp, smtp)  |
| flag |  categorical, 11 different flags | Status of the connection (SF, S0, REJ)  |
| src_bytes |  - | Bytes sent from source to destination |
| dst_bytes |  - | Bytes sent from destination to source |
| land | bool | 1: connection to/from same host <br/>0: otherwise |
| wrong_fragment |  - | Nr of wrong fragments |
| urgent |  - | Nr of urgent packets |
| hot |  - | Nr of hot indicatiors |
| num_failed_logins |  - | Nr of failed login attempts |
| logged_in |  bool  | 1: successfully logged in <br/>0: otherwise|
| num_compromised |  - | Nr of compromised conditions |
| root_shell |  bool | 1: root shell obtained <br/>0: otherwise |
| su_attempt |  bool | 1: 'su root' command attempt <br/>0: otherwise |
| num_root |  - | Nr of root accesses |
| num_file_creations |  - | Nr of file creation operations |
| num_shells |  - | Nr of shell prompts invoked |
| num_access_files |  - | Nr of access file control operations |
| num_outbound_cmds |  - | Nr of outbound commands |
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


