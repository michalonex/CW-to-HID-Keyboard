# CW-to-HID-Keyboard
CW to HID Keyboard

!(https://github.com/michalonex/CW-to-HID-Keyboard/blob/main/photo_2025-09-01_20-32-32.jpg)!

**EN Below (soon)**

Podczas nauki telegrafii wpadłem na pomysł zrobiena adaptera do klucza telegraficznego, ażeby to co "nadajemy", było interpretowane i wstawiane jako zwykły tekst do dowolnego okna lub edytora.
Celem tego jest nauka poprawnego nadawania liter, cyfr i znaków a w przysłości możliwosc pisania długich dokumentów jedna ręką ;)

**BOM:**
- Raspberry Pi Pico (RP2040)
- Gniazdo Jack 3.5mm TRS
- Enkoder
- Ekran Oled I2C (soon to be done)

**Podłączenie zestawu:**
- Pin GP28 do lewej łopatki (kropka)
- Pin GP29 do prawej łopatki (kreska)
- pin wspólny manipulatora do masy
- Enkoder podłączamy do masy, GP27, GP26

**Instrukcja obsługi:**

Podłaczamy kablem USB do komputera RP Pico i otwieramy port COM przypisany do urządzenia. Mamy wtedy podgląd na debug, oraz na prędkośc w WPM. I to wsumie tyle, Możemy się cieszyć klawiaturą do treningu ;)

SQ9ALW VE 73!!
