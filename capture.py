import cv2
import os
import copy
from numpy import vstack, hstack, shape
from tkinter import Tk, filedialog


def update_windows(frame1, frame2, y_barre, x_max, ration_reduction = 3):

    # ration_reduction = 1

    display1 = copy.deepcopy(frame1)
    cv2.line(display1, (0, y_barre), (x_max, y_barre), (0, 0, 255), 5)
    display1 = cv2.resize(display1, (int(display1.shape[1]/ration_reduction), int(display1.shape[0]/ration_reduction)))
    display2 = copy.deepcopy(frame2)
    display2 = cv2.resize(display2, (int(display2.shape[1]/ration_reduction), int(display2.shape[0]/ration_reduction)))

    cv2.imshow("Premiere frame", display1)
    cv2.imshow("Seconde frame",  display2)


def read_frame_at(cap, index):
    cap.set(cv2.CAP_PROP_POS_FRAMES, index)
    ret, frame = cap.read()
    if not ret:
        return None
    return frame


def select_interval(cap, total_frames):
    """
    Affiche la première image et la seconde pour sélectionner l'interval entre les images.

    Args:
        video_path (str): Chemin vers la vidéo.
    """

    # Lire toutes les frames et les stocker dans une liste
    print("Préparation de l'aperçu...")
    first = read_frame_at(cap, 0)
    if first is None:
        print("Erreur : impossible de lire la première frame.")
        return None, None, None
    
    y_max, x_max, _ = first.shape

    i0 = 50 if total_frames > 50 else 0
    i1 = 100 if total_frames > 100 else min(total_frames-1, i0+1)
    y_barre = int(first.shape[0]*4/5)
    reduction = 3

    # Afficher initialement
    f0 = read_frame_at(cap, i0)
    f1 = read_frame_at(cap, i1)
    if f0 is None : f0 = first
    if f1 is None : f1 = first
    update_windows(f0, f1, y_barre, x_max, ration_reduction=reduction)

    cancel = False
    while True :
        key = cv2.waitKey(0) & 0xFF
        if key == ord('w'):
            cancel = True
            print("Annulation.")
            break
        elif key == ord('a'):
            if i0 > 0 :
                i0 -= 1
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('r'):
            if i0 > 0 :
                i0 -= 10
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('z'):
            if i0 < total_frames :
                i0 += 1
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('t'):
            if i0 < total_frames :
                i0 += 10
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('q'):
            if i1 > 0 :
                i1 -= 1
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('f'):
            if i1 > 0 :
                i1 -= 10
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('s'):
            if i1 < total_frames-1 :
                i1 += 1
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('g'):
            if i1 < total_frames-1 :
                i1 += 10
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('e'):
            if y_barre > 0 :
                y_barre -= 10
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('d'):
            if y_barre < y_max-1 :
                y_barre += 10
            else : print("Limite de la vidéo atteinte.")
        elif key == ord('y'):
            if reduction > 1 :
                reduction -= 1
                print(f"reduction = {reduction}")
            else : print("Taille originale atteinte.")
        elif key == ord('h'):
            reduction += 1
            print(f"reduction = {reduction}")
        elif key == ord('x'): # Validation
            print("Validation de l'intervalle.")
            break
        else:
            # touche non gérée -> continuer sans mise à jour
            continue

        # Mettre à jour l'affichage à partir des index actuels
        f0 = read_frame_at(cap, i0)
        f1 = read_frame_at(cap, i1)
        update_windows(f0, f1, y_barre, x_max, ration_reduction=reduction)

    cv2.destroyAllWindows()

    if cancel : return None, None, None
    return i0, i1, y_barre


def trim_frames(cap, i0, i1, total_frames, y_barre) :

    print("Rognage des images...")

    interval = i1 - i0
    if interval <= 0:
        print("Intervalle invalide pour le rognage.")
        return []

    trimmed_frames = []
    idx = i0
    while idx < total_frames :
        frame = read_frame_at(cap, idx)
        if frame is None:
            break
        trimmed_frames.append(frame[:y_barre, :])
        idx += interval

    print("Images rognées !")

    return trimmed_frames


def frames_layout(frames, nb_frame_verticaly, nb_frame_horizontaly=0):

    print("Mise en page...")

    # Verticale
    pages_verticales = []

    nb_frames = len(frames)

    quotient, reste = divmod(nb_frames, nb_frame_verticaly)

    for i in range(quotient) :
        frame_in_page = []
        for j in range(nb_frame_verticaly):
            frame_in_page.append(frames[ i*nb_frame_verticaly + j])
        pages_verticales.append(vstack(frame_in_page[::-1]))
    
    if reste > 0 :
        frame_in_page = []
        for i in range(reste):
            frame_in_page.append(frames[ quotient*nb_frame_verticaly + i])
        pages_verticales.append(vstack(frame_in_page[::-1]))

    # Horizontale
    if nb_frame_horizontaly > 1:
        pages = []
        nb_pages_verticales = len(pages_verticales)
        quotient, reste = divmod(nb_pages_verticales, nb_frame_horizontaly)
        print(reste)
        for i in range(quotient):
            pages_vertical_in_page = []
            for j in range(nb_frame_horizontaly):
                pages_vertical_in_page.append(pages_verticales[i*nb_frame_horizontaly+j])
            pages.append(hstack(pages_vertical_in_page[::1]))
        if reste > 0 :
            pages_vertical_in_page = []
            hauteur_max = 0
            page_seul = []
            for i in range(reste):
                hauteur = shape(pages_verticales[quotient*nb_frame_horizontaly + i])[0]
                if i == 0 :
                    hauteur_max = hauteur
                if hauteur == hauteur_max:
                    pages_vertical_in_page.append(pages_verticales[quotient*nb_frame_horizontaly + i])
                else :
                    page_seul.append(pages_verticales[quotient*nb_frame_horizontaly + i])

            pages.append(hstack(pages_vertical_in_page[::1]))
            for p in page_seul :# On ajoute la page qui n'est pas à la bonne hauteur dans une page à part
                pages.append(p)
        
        print("Pages prêtes")

        return pages

    print("Pages prêtes")

    return pages_verticales


def save_pages(pages, output_folder) :

    print("Réduction et enregistrement des images...")

    counter = 0
    for f in pages :
        output_path = os.path.join(output_folder, f"capture_{counter:03d}.jpg")
        cv2.imwrite(output_path, f)
        counter += 1
    
    print(f"Images enregistrées ! Sous {output_folder}")


if __name__ == "__main__":

    # Ouvrir une fenêtre pour sélectionner un fichier
    root = Tk()
    # root.withdraw()  # Masquer la fenêtre principale

    # Demander à l'utilisateur de sélectionner un fichier vidéo
    video_path = filedialog.askopenfilename(
        title="Sélectionner un fichier vidéo",
        filetypes=[("Fichiers vidéo", "*.mp4 *.avi *.mkv *.mov")]
    )

    if video_path:  # Si un fichier a été sélectionné

        print(f"Fichier sélectionné : {video_path}")

        # video_path = "Vidéos inputs/Introduction - Wanderstop OST (Piano Tutorial) [7m2WpDmy0-M].mp4" # Remplace par ton fichier
        output_folder = "PhotosOutput" # Dossier de sortie
        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(output_folder, exist_ok=True)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Erreur : Impossible d'ouvrir la vidéo.")

        else :
        
            # Récupérer le nombre total de frames
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            i0, i1, y_barre = select_interval(cap, total_frames)

            if i0 != None : 

                trimmed_frames = trim_frames(cap, i0, i1, total_frames, y_barre)

                pages = frames_layout(trimmed_frames, 3, 2)

                save_pages(pages, output_folder)
        
        cap.release()
