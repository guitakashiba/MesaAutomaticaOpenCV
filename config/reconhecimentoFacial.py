import cv2
import pickle
import sqlite3

conexao = sqlite3.connect('bancoUser.db')

if conexao:
    print("Conexão ok")
else:
    print("Conexão not ok")

c = conexao.cursor()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner1.yml")

labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

cap = cv2.VideoCapture(0)


def procuraAltura(name):

    c.execute("SELECT Altura FROM People WHERE Nome = :name LIMIT 1",
      {
          'name': name,
      })
    rows = c.fetchall()
    return rows[0][0] if rows else -1


def verificaUser():

    threshold = 5

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            img_item = "my-image.png"
            cv2.imwrite(img_item, roi_gray)

            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

            id_, conf = recognizer.predict(roi_gray)
            if 45 <= conf <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]  # pegar essa variavel para comparar
                print(name)  # Para executar somente o verificador em tempo real, comentar linhas 55-61
                altura = procuraAltura(name)

                if altura == -1 and threshold == 0:
                    return -1
                elif altura == -1 and threshold > 0:
                    threshold -= 1
                else:
                    return altura

                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y - 10), font, 1, color, stroke, cv2.LINE_AA)
                cv2.putText(frame, str(conf), (x, y - 50), font, 1, color, stroke, cv2.LINE_AA)

        cv2.imshow('frame', frame)
        if cv2.waitKey(20) == ord('q'):
            break


altura_util = verificaUser()
print(altura_util)
cap.release()
cv2.destroyAllWindows()
