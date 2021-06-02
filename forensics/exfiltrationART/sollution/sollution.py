DATA = ""
# tshark -r packets.pcapng -Y "arp.src.proto_ipv4 == 192.168.133.0/24" -Tfields -e arp.src.hw_mac > exfiltrated.macs
with open("exfiltrated.macs", "r") as file:
    DATA = file.read()
    file.close()

FINALDATA = ""

for line in DATA.split("\n"):
    # print(repr(line.split(":")))
    if line:
        FINALDATA += "".join([chr(int(i, 16)) for i in line.split(":")])
print(FINALDATA)


# flag => IngeHack{luLZ_0n_Ur_F1r3W4ll_H4ck1Ng_4rP_1s_4Rt}
