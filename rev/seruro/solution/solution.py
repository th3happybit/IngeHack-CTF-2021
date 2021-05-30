import hashlib

# flag ==> IngeHack{53rur0_7h3_unbr34k4bl3_l0ck}
# extracted from apk
firstCheckHash = "4f413a1f2c3501bdf30305cacea8d42230e853a0e44500b7aa0ca5f376a23748"
secondCheckDump = [236, 6, 13, 236, 12, 14, 236, 11, 8, 238, 11, 1, 245, 11, 250]
secondCheckSum = 1557
thirdCheckDump = [227, 147, 245, 214, 103, 118, 241, 64, 251, 85]

# get certificat sha256 with `keytool -printcert -jarfile seruro.apk`
thirdCheckCertificatHash = [0xF5,0x8F,0xE3,0xCA,0x71,0x54,0xD0,0x55,0xE0,0x40]

def crack_first_hash(hash):
    for i in range(0,36):
        for j in range(0,36):
            for k in range(0,36):
                for l in range(0,36):
                    values = [i,j,k,l]
                    b = "".join(map(lambda a: chr(a), values ))
                    tested_hash = hashlib.sha256(str.encode(b)).hexdigest()
                    if tested_hash == hash:
                        return values


def extract_second_values(dump, some):
    values = []

    values.append(some - sum(dump))

    for i in range(1,16):
        values.append((values[i-1] + dump[i-1]) & 0xFF)

    return values


def extract_third_values(cert_hash, dump):
    values = []
    for i in range(0,10):
        values.append(cert_hash[i]^dump[i])
    
    return values


if __name__ == "__main__":

    values = crack_first_hash(firstCheckHash) +\
         extract_second_values(secondCheckDump,secondCheckSum) +\
         extract_third_values(thirdCheckCertificatHash,thirdCheckDump)

    combination1 = []
    combination2 = []
    combination3 = []

    for i in range(0,30):
        if i % 3 == 0:
             combination1.append(values[i])
        else:
            if i<24:
                if i % 3 == 1 :
                    combination3.append(values[i])
                else:
                    combination2.append(values[i])
            else:
                combination2.append(values[i])

    print(f"combination 1 : {combination1}")
    print(f"combination 2 : {combination2}")
    print(f"combination 3 : {combination3}")
