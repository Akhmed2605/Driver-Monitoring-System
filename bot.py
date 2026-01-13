import cv2
import face_recognition
import telebot
import os
import time
import threading
from dotenv import load_dotenv


load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")
driver_image_file = os.getenv("DRIVER_IMAGE")
camera_index = 0


bot = telebot.TeleBot(bot_token)

allowed_faces = []
camera = None
last_voice_alert = 0
last_telegram_alert = 0


def load_driver_face():
    # Referenzbild laden und Encoding (Vektor) erstellen
    image = face_recognition.load_image_file(driver_image_file)
    encondig = face_recognition.face_encodings(image)[0]
    allowed_faces.append(encondig)


def open_camera():
    cam = cv2.VideoCapture(camera_index)
    if cam.isOpened():
        return cam 
    else:   
        return None


def send_telegram_alert(frame):
    cv2.imwrite("alert.jpg", frame)
    with open("alert.jpg", "rb") as f:
        bot.send_photo(chat_id, f, caption="Unbefugter Zugriff!!!")


load_driver_face()
camera = open_camera()

window_name = "Driver Monitoring System"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    if camera is None or not camera.isOpened():
        time.sleep(2)
        camera = open_camera()
        continue

    ret, frame = camera.read()
    if not ret:
        camera.release()
        camera = None
        continue

    frame = cv2.flip(frame, 1)

    # Performance-Optimierung: Bild verkleinern (Scale 0.25) für Echtzeit-Verarbeitung
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Gesicht finden und in Vektoren umwandeln
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    cv2.rectangle(frame, (0, 0), (3000, 70), (30, 30, 30), -1)
    cv2.putText(frame, "Driver Monitoring System",
                (40, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    engine_status = "STATUS: BEREIT"

    if not face_locations:
        cv2.putText(frame, "KEIN FAHRER",
                    (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 180, 180), 2)

    for enc, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Koordinaten hochrechnen (da Bild verkleinert war)
        top *= 4; right *= 4; bottom *= 4; left *= 4

        # Abgleich: Ist es der gespeicherte Fahrer?
        match = face_recognition.compare_faces(allowed_faces, enc, tolerance=0.5)

        if True in match:
            box_color = (0, 255, 0)
            engine_status = "MOTOR: FREIGEGEBEN"

            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)
            cv2.putText(frame, "AUTORISIERT",
                        (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, box_color, 2)

        else:
            box_color = (0, 0, 255)
            engine_status = "MOTOR: GESPERRT"

            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 3)
            cv2.putText(frame, "UNBEFUGT",
                        (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, box_color, 2)
            cv2.putText(frame, "ZUGRIFF VERWEIGERT",
                        (right + 20, top + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, box_color, 3)

            if time.time() - last_voice_alert > 5:
                os.system('say -v Anna "Achtung! Unbefugter Zugriff!" &')
                last_voice_alert = time.time()

            if time.time() - last_telegram_alert > 30:
                # Threading: Senden im Hintergrund, damit Video nicht einfriert
                threading.Thread(target=send_telegram_alert, args=(frame,)).start()
                last_telegram_alert = time.time()

    status_color = (0, 255, 0) if "FREIGEGEBEN" in engine_status else (0, 0, 255)

    cv2.putText(frame, engine_status, (50, frame.shape[0] - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, status_color, 3)

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if camera:
    camera.release()

cv2.destroyAllWindows()