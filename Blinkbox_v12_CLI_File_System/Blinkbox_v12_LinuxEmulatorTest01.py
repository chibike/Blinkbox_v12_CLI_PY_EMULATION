from Blinkbox_v12_CLI_Header import*

print("Blinkbox_v12 Shell 1.1 [on Blink Os v12]")

USER = ''
PWD = '\\home'
while 1:
    ssids = fileParseCsvData("SSIDS.txt")
    keys = fileParseCsvData("KEYS.txt")
    users = dict(zip(ssids, keys))
    try:
        ssid = input("Username: ")
        key = input("Password: ")
        if users[ssid] == key:
            USER = ssid+"@"+key
            break
        else:
            raise NameError()
    except:
        continue

while 1:
    CMD = input(USER+" "+PWD+" $ ")
    if CMD.startswith("ls"):
        processListDirCmd( CMD[2:], PWD )
