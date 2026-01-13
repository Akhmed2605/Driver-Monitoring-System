# Driver-Monitoring-System

Dieses Projekt ist ein **Driver Monitoring System**, das mithilfe von **OpenCV** und **face_recognition** überprüft, ob eine autorisierte Person (Fahrer) vor der Kamera sitzt.  
Bei unbefugtem Zugriff wird der Motor symbolisch gesperrt, eine **Sprachwarnung** ausgegeben und eine **Telegram-Benachrichtigung mit Foto** versendet.

---

## 🔧 Funktionen

- 🎥 Echtzeit-Gesichtserkennung über Webcam
- ✅ Autorisierung eines vordefinierten Fahrers
- ❌ Erkennung von unbefugten Personen
- 🔊 Sprachwarnung bei unbefugtem Zugriff
- 📩 Telegram-Alarm mit Bild (zeitlich begrenzt, um Spam zu vermeiden)
- 🖥 Vollbild-Anzeige mit Statusinformationen
- ⚡ Performance-Optimierung durch Bildskalierung

---

## 🛠 Verwendete Technologien

- Python 3
- OpenCV (`cv2`)
- face_recognition
- Telegram Bot API (`pyTelegramBotAPI`)
- threading
- dotenv (`python-dotenv`)

---

## 📁 Projektstruktur

```text
.
├── main.py              # Hauptprogramm
├── .env                 # Umgebungsvariablen (Token, Chat-ID, Bildpfad)
├── driver.jpg           # Referenzbild des autorisierten Fahrers
├── alert.jpg            # Temporäres Bild für Telegram-Alarm
└── README.md
⚙️ Installation
1️⃣ Abhängigkeiten installieren
bash
Code kopieren
pip install opencv-python face-recognition pyTelegramBotAPI python-dotenv
Hinweis:
face_recognition benötigt dlib. Unter manchen Systemen kann die Installation etwas Zeit in Anspruch nehmen.

2️⃣ .env Datei erstellen
Erstelle im Projektverzeichnis eine Datei .env mit folgendem Inhalt:

env
Code kopieren
BOT_TOKEN=DEIN_TELEGRAM_BOT_TOKEN
CHAT_ID=DEINE_CHAT_ID
DRIVER_IMAGE=driver.jpg
BOT_TOKEN → Token deines Telegram-Bots

CHAT_ID → Deine Telegram-Chat-ID

DRIVER_IMAGE → Referenzbild des autorisierten Fahrers

▶️ Programm starten
bash
Code kopieren
python main.py
Webcam wird automatisch geöffnet

Drücke q, um das Programm zu beenden

🧠 Funktionsweise
Ein Referenzbild des Fahrers wird geladen und codiert

Die Webcam erkennt Gesichter in Echtzeit

Jedes erkannte Gesicht wird mit dem Referenzbild verglichen

Bei Übereinstimmung:

Status: MOTOR: FREIGEGEBEN

Grüner Rahmen um das Gesicht

Bei Nicht-Übereinstimmung:

Status: MOTOR: GESPERRT

Roter Rahmen

Sprachwarnung alle 5 Sekunden

Telegram-Alarm mit Foto alle 30 Sekunden

⚠️ Hinweise
Dieses Projekt ist ein Demonstrations- und Lernprojekt

Es ersetzt keine echte Fahrzeugsicherheit

Sprachwarnung (say) funktioniert standardmäßig auf macOS

Unter Windows oder Linux muss die TTS-Funktion angepasst werden

🚀 Mögliche Erweiterungen
Mehrere autorisierte Fahrer

Datenbank-Anbindung

GUI mit Qt oder Tkinter

Integration mit Raspberry Pi

Nachtmodus / IR-Kamera

Logging von Zugriffen
