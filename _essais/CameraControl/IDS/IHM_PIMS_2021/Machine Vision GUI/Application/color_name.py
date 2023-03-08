# Victoire
# version du 17/02/2022

import colorsys
import cv2
import numpy as np

img=cv2.imread('cube.png')
# rescale coefficient
c = 500 / img.shape[0]
# rescale image
img = cv2.resize(img, None, fx=c, fy=c, interpolation=cv2.INTER_CUBIC)
img2 = img.copy()


# mask for black
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
mask = cv2.inRange(gray, 40, 255);
cv2.imshow("Image", mask);
cv2.waitKey(0);
# mask = ouverture(mask,3)
# mask = fermeture(mask,3)
# mask = flou(mask,3)


def color_clusters(img,nclusters):
    # les samples pour cv2.kmean doivent être sous dorme d'une unique colonne
    pixels = np.float32(img.reshape(-1, 3))
    # définition du critère de terminaision pour l'algo itératif cv2.kmean
    # dès que la precision eps est atteinte ou des que le nombre max d'iteraitions est atteinte
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.)
    # pour ruptures de lignes :
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centers = cv2.kmeans(pixels, nclusters, None, criteria, 10, flags)
    return labels, centers


def color_diagram_data(img,labels):
    # counts : nombre de fois que chaque couleur apparaît :
    _, counts = np.unique(labels, return_counts=True)
    # indices (0: couleur dominante, nclusters-1 : couleur minoritaire)
    indices = np.argsort(counts)[::-1]
    # fréquences cumulées d'apparition des couleurs (dominantes d'abord, minoritaires après):
    freqs = np.cumsum(np.hstack([[0], counts[indices] / counts.sum()]))
    # nombre de lignes corresppndant pour chaque couleur
    rows = np.int_(img.shape[0] * freqs)
    return rows, indices


# quantification des couleurs : réduction du nombre de couleurs de l'image
def average_dominant(img,nclusters):
    labels, centers = color_clusters(img,nclusters)
    rows, indices = color_diagram_data(img,labels)
    liste_legende=[]
    for i in range(len(rows) - 1):
        dominant = centers[indices[i]]
        [B, G, R] = dominant
        dominant = [int(R), int(G), int(B)]
        liste_legende.append(dominant)
    return liste_legende


def hls2rgb(h,l,s):
    return tuple((i*255) for i in colorsys.hls_to_rgb(h,l,s))


def rgb2hls(r,g,b):
    return tuple((i*255) for i in colorsys.rgb_to_hls(r,g,b))


# position sur le diagramme des couleurs
def dominant_position(r, g, b):
    print(r,g,b)
    imgHL = np.zeros((255,255,3))
    [h,l,s]=rgb2hls(r/255,g/255,b/255)
    h,l,s=h/255,l/255,s/255
    min=10
    imin=0
    jmin=0
    for i in range(255):
        for j in range(255):
            H=i/255
            S=250/255
            L=j/255
            [R,G,B]=hls2rgb(H,L,S)
            imgHL[i, j, 0] = R/255
            imgHL[i, j, 1] = G/255
            imgHL[i, j, 2] = B/255
            similarity = ((H-h)**2 +(S-s)**2 +(L-l)**2)/3
            if similarity<min:
                min=similarity
                imin=i
                jmin=j
    return imin


def dominant_color(i):
    if i<=15:
        char = 'red'
    if i>15 and i<=35:
        char = 'orange'
    if i>35 and i<=45:
        char = 'yellow'
    if i>45 and i<=110:
        char = 'green'
    if i>110 and i<=120:
        char = 'blue-green'
    if i>120 and i<=135:
        char = 'cyan'
    if i>135 and i<=180:
        char = 'blue'
    if i>180 and i<=205:
        char = 'purple'
    if i>205 and i<=245:
        char = 'pink'
    if i>245:
        char = 'red'
    return char


def what_is_this_color(triplet):
    [r,g,b] = triplet
    i = dominant_position(r, g, b)
    char = dominant_color(i)
    return char

def display_name(mask,img):
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE);
    print(len(contours))
    cv2.drawContours(mask, contours, -1, 255, -1);

    for c in contours:
        mask[:] = 0;
        mask = cv2.drawContours(mask, [c], -1, 255, -1);
        cv2.imshow("Image", mask)
        cv2.waitKey(0);
        one_color = img.copy()
        one_color[mask != 255] = (0, 0, 0);
        dominant_list = average_dominant(one_color, 2)
        char = what_is_this_color(dominant_list[1])
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.drawContours(img, [c], -1, (0, 255, 0), 3)
        cv2.putText(img, char, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow("Image", img);
    cv2.waitKey(0);


display_name(mask,img)