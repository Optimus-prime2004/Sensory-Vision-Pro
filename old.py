import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
import shutil

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("hello valliappan")
    speak("I am Friday, your personal assistant. How may I assist you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        speak("Recognizing...")
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("Say that again please...")
        print("Say that again please...")
        return "None"
    return query

def create_database():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS database (
                        id INTEGER PRIMARY KEY,
                        class_id TEXT,
                        time TEXT
                    )''')
    conn.commit()
    conn.close()

def insert_data(class_id, time):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO database (class_id, time) VALUES (?, ?)", (class_id, time))
    conn.commit()
    conn.close()

create_database()

def fetch_data_from_database():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM database")
    data = cursor.fetchall()
    conn.close()
    return data

def create_pdf(data):
    pdf_filename = "data_report.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []
    table_data = [['S No', 'Class ID', 'Time']]
    for row in data:
        table_data.append(list(row))
    table = Table(table_data, colWidths=[1 * inch, 1 * inch, 2 * inch])
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    print(f"PDF report generated: {pdf_filename}")

def send_emergency_message(message):
    sender_email = "vvalliappan2004@gmail.com"
    sender_password = "uqsx jftr slwr lave"
    receiver_email = "jayani1601@gmail.com"
    subject = "Emergency Alert!"
    body = message
    message1 = f"Subject: {subject}\n\n{body}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message1)
    server.quit()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'open yolo' in query:
            speak("Initiating object detection protocol")
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)

            def tell(audio):
                engine.say(audio)
                engine.runAndWait()

            def command():
                r = sr.Recognizer()
                tell('tell me access code to run')
                with sr.Microphone() as source:
                    speak("Listening...")
                    print("Listening...")
                    r.pause_threshold = 1
                    audio = r.listen(source)
                try:
                    speak("Recognizing...")
                    print("Recognizing...")
                    query = r.recognize_google(audio, language='en-in')
                    print(f"User said: {query}\n")
                except Exception as e:
                    speak("Say that again please...")
                    print("Say that again please...")
                    return "None"
                return query

            if __name__ == "__main__":
                query = command().lower()
                if 'object' in query:
                    import numpy as np
                    import time
                    import cv2
                    import pyttsx3
                    import threading
                    tell("access code accepted")

                    label_path = "coco.names"
                    yolo_config_path = "yolov3.cfg"
                    yolo_weight_path = "yolov3.weights"
                    base_confidence = 0.5
                    threshold = 0.6

                    engine = pyttsx3.init('sapi5')
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[1].id)

                    def say(text):
                        engine.say(text)
                        engine.runAndWait()

                    LABELS = open(label_path).read().strip().split('\n')
                    net = cv2.dnn.readNetFromDarknet(yolo_config_path, yolo_weight_path)
                    np.random.seed(42)
                    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

                    # Initialize webcam with DirectShow backend
                    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    if not cap.isOpened():
                        tell("Error: Could not open webcam. Please check if it is connected and not in use.")
                        print("Error: Could not open webcam.")
                        break

                    # Set webcam properties (optional)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                    ln = net.getLayerNames()
                    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
                    frame_counter = 0
                    detect_per = 40
                    boxes = []
                    confidences = []
                    class_ids = []
                    failure_count = 0
                    max_failures = 5  # Exit after 5 consecutive failures

                    while True:
                        frame_counter += 1
                        ok, img = cap.read()

                        # Validate frame
                        if not ok or img is None or not hasattr(img, 'shape'):
                            failure_count += 1
                            tell("Warning: Failed to capture frame from webcam.")
                            print("Warning: Failed to capture frame from webcam.")
                            if failure_count >= max_failures:
                                tell("Error: Too many failed attempts to capture frames. Exiting object detection.")
                                print("Error: Too many failed attempts to capture frames.")
                                break
                            time.sleep(0.1)  # Brief pause to avoid overwhelming the webcam
                            continue

                        # Reset failure count on successful capture
                        failure_count = 0

                        start = time.time()
                        if (frame_counter % detect_per) == 0:
                            try:
                                H, W = img.shape[:2]
                                blob = cv2.dnn.blobFromImage(
                                    img, 1 / 255, (416, 416), swapRB=True, crop=True)
                                boxes = []
                                confidences = []
                                class_ids = []

                                net.setInput(blob)
                                layer_output = net.forward(ln)

                                end = time.time()
                                print("[INFO] Predicted in", end - start)

                                frame_counter = 0
                                for out in layer_output:
                                    for detection in out:
                                        scores = detection[5:]
                                        class_id = np.argmax(scores)
                                        confidence = scores[class_id]

                                        if confidence > base_confidence:
                                            box = detection[:4] * np.array([W, H, H, W])
                                            (cx, cy, w, h) = box.astype("int")
                                            print("Found", LABELS[class_id], "At", (cx, cy))
                                            boxes.append(
                                                (int(cx - (w / 2)), int(cy - (h / 2)), int(w), int(h))
                                            )
                                            confidences.append(float(confidence))
                                            class_ids.append(class_id)
                            except Exception as e:
                                tell("Error during object detection processing.")
                                print(f"Error during object detection: {e}")
                                continue

                        idxs = cv2.dnn.NMSBoxes(boxes, confidences, base_confidence, threshold)

                        if len(idxs) > 0:
                            for i in idxs.flatten():
                                (x, y) = (boxes[i][0], boxes[i][1])
                                (w, h) = (boxes[i][2], boxes[i][3])
                                print(x, y, w, h)
                                color = [int(c) for c in COLORS[class_ids[i]]]
                                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                                value = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])
                                cv2.putText(
                                    img, value, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                center_x = x + w / 2
                                if center_x >= W * 0.7:
                                    text = f"Found {LABELS[class_ids[i]]} on the right"
                                elif center_x <= W * 0.3:
                                    text = f"Found {LABELS[class_ids[i]]} on the left"
                                else:
                                    text = f"Found {LABELS[class_ids[i]]} in the center"
                                threading.Thread(target=say, args=(text,)).start()

                        end = time.time()
                        print("[INFO] Loop in", end - start)

                        # Display frame only if valid
                        if img is not None and hasattr(img, 'shape') and img.size > 0:
                            cv2.imshow("Image", img)
                        else:
                            print("Warning: Invalid frame, skipping display.")

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            cap.release()
                            cv2.destroyAllWindows()
                            break

                    cap.release()  # Ensure webcam is released
                    cv2.destroyAllWindows()
                    tell("object detection closed")
                else:
                    tell('Access code denied')
            tell("object detection closed")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak('opening google')
            webbrowser.open("google.com")

        elif 'play music' in query:
            music_dir = 'C:/Users/al/Documents/computer networks/music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'emergency' in query:
            send_emergency_message("Emergency!please help me")
            print("Emergency message sent.")

        elif 'switch off' in query:
            speak("Goodbye!")
            data = fetch_data_from_database()
            def download_pdf():
                src_file = "data_report.pdf"
                dst_folder = "D:/blind database"
                dst_file = f"{dst_folder}/data_report.pdf"
                shutil.copy(src_file, dst_file)
                print(f"PDF downloaded to {dst_file}")
            create_pdf(data)
            download_pdf()
            break