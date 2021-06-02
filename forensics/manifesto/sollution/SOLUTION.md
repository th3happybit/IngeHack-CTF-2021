# MANIFESTO challenge solution

Use this tool to convert key strokes to text

`https://github.com/TeamRocketIst/ctf-usb-keyboard-parser`

- Extract key strokes codes

`tshark -r ./manifesto.pcapng -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2'> data`

- Convert them with ctf-usb-keyboard-parser

`python usbkeyboard.py data`

## flag

`IngeHack{i_4m_4_H4Ck3r_4Nd_THi5_i5_MT_M4nIF35t0}`
