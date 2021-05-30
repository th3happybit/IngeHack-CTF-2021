
##
# can be solved directly (2**50)
# or by brute force
# #

if __name__ == "__main__":
    for i in range(10000):
        value = 2**i
        if (value & -value == value) and (value >> 50) == 1:
            print(f"magic number is => {i}")
            break
