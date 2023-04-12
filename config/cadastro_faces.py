import time
import cv2
import os


def cad_faces():
    fotos = 20

    cam = cv2.VideoCapture(0)
    name = input("Digite seu nome: ")

    print("Olhe para a camera!")
    time.sleep(3)
    if name:
        try:
            path = r'/MesaAutomatica/config/imagens/usuarios'
            os.chdir(path)
            os.mkdir(name)
            os.chdir(name)

            for i in range(fotos):
                ret, img = cam.read()

                cv2.imshow("Rosto", img)
                cv2.imwrite(name + str(i) + '.png', img)
                print("Fotos capturadas %d" % i)

                if i == fotos - 1:
                    print(name, "cadastrado com sucesso")
                    break
        except FileExistsError:
            print("path", name, "já existe")

    os.chdir(path)
    cam.release()
    cv2.destroyAllWindows()
