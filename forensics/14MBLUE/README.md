# CTF-2021 Forensics

## 14MBLUE

    -Network
    -Medium

### Description

    Hello comrade, I have a problem and I need you, it happened that I was hosting my friend's php blog in our production server (sorry), and it looks like someone got in, I don't know how it happened but it most likely was the php blog.
    Luckly for me I found the network log of the incident, Please can you find out what the hacker took.

### Solution

- Looking at the pcap file with wireshark you can find where the hacker found a vulnerable file upload and uploaded a obfuscated php webshell.
- using tshark to extract the communication with the webshell:
  `tshark -r network_log.pcapng -Y "http.request.uri == \"/uploads/wsell.php\"" -Tfields -e http.file_data >coms`
- Decoding the communication with webshell after deobfuscationg it.
- finding `tmp.py` and reading it we can find out that it's using hashes to verify the flag, cracking those hashes to find the flag.
