import numpy
from PIL import Image
from timeit import default_timer as timer
import matplotlib.pyplot as plt

def get_image(image_path):
    image = Image.open(image_path, "r")
    width, height = image.size
    pixel_values = list(image.getdata())
    
    pixel_values = numpy.array(pixel_values).reshape((height, width, 1))
    
    return pixel_values

def rech_supsymb(liste):
    minimum = 1
    calc = 0
    couple_indice = [0,1]
    for i in range(len(liste)):
        a = liste[i]
        idx = 0
        while (idx != len(liste)):
            if idx != i :
                b = liste[idx]
                calc = a+b
                if (minimum > calc) :
                    minimum = calc
                    couple_indice = [i,idx]
            idx+=1
    return (couple_indice,minimum)   

def main(fichier) :
    start = timer()

    img = Image.open(str(fichier)).convert('L')
    img.save('input.png')
    image = get_image("input.png")
    f = open("output.txt","w")
    for ligne in image :
        for pixel in ligne :
            if len(str(pixel[0])) != 3:
                f.write((3-len(str(pixel[0])))*'0'+str(pixel[0])+' ') 
            else: 
                f.write(f"{str(pixel[0])} ")
        f.write('\n')


    Prob = {
        "nb_valeur" : 0
    }
    f = open("output.txt","r")
    fichier = f.read().split(' ')
    f.close()
    
    for i in range(len(fichier)-1):
        valeur = str(fichier[i]).replace("\n","")
        if valeur not in Prob :
            Prob[valeur] = 1
        else :
            Prob[valeur] += 1
        Prob["nb_valeur"]+=1

    for key, value in Prob.items():
        if value != Prob["nb_valeur"] :
            Prob[key] = value/Prob["nb_valeur"]

    f = open("table_hamming.txt","w")
    Prob = dict(sorted(Prob.items(), key=lambda item: item[1]))
    for key, value in Prob.items():
        if key != "nb_valeur":
            value = format(value, '.60g')
            f.write(f"{key} : {value} \n")
    f.write("\n")

    Liste_prob = []
    for value in Prob.values():
        Liste_prob.append(value)
    Liste_prob.pop()

    L_operations =[]
    i=0
    while (len(Liste_prob)!=1):
        couple,minimum = rech_supsymb(Liste_prob)
        L_operations.append((minimum))     
        Liste_prob.pop(couple[1])
        Liste_prob[couple[0]]=minimum
        minimum = 1
        couple = [0,1]
        SS = format(L_operations[-1],'.60g')
        if i<10:
            f.write(f"SS0{i}: {SS}\n")
        else :
            f.write(f"SS{i}: {SS}\n")
        i+=1
    f.write("\n")
    f.close()

    end = timer()
    print(f"{end - start}s")


def calc_distance(p1,p2):
    x0=int(p1[0])
    x1=int(p2[0])
    y0=int(p1[1])
    y1=int(p2[1])

    a = abs(x1-x0)
    b = abs(y1-y0)
    c = a**2 + b**2

    return c**(1/2) 

def detect_forme(fichier,seuil):
    main(fichier)
    start = timer()
    f = open("output.txt",'r')
    Matrice = f.readlines()
    f.close()
    ImgX = []
    ImgXY = []
    for x in range(len(Matrice)):
        ligne = Matrice[x].split(" ")
        
        ImgX = []
        for y in range(len(ligne)):
            if ligne[y] != '\n':
                pxy = int(ligne[y])
                if pxy < seuil :
                    ImgX.append((x,y))
        ImgXY.append(ImgX)
    f = open("img.txt",'w')
    for ligne in ImgXY :
        if len(ligne)!=0:
            for pt in ligne:
                x = len(Matrice)-pt[0]
                y = pt[1]
                if len(str(x)) != 3 and len(str(y))==3:
                    f.write(f"{(3-len(str(x)))*'0'}{x},{y}|")

                elif len(str(y)) != 3 and len(str(x))==3:
                    f.write(f"{x},{(3-len(str(y)))*'0'}{y}|")

                elif (len(str(y)) != 3) and (len(str(x)) != 3):
                    f.write(f"{(3-len(str(x)))*'0'}{x},{(3-len(str(y)))*'0'}{y}|")

                else :
                    f.write(f"{x},{y}|")
            f.write('\n')
    f.close()

    f = open("img.txt",'r')
    Coord = f.readlines()
    f.close()
    coord_x = []
    coord_y = []

    for x in range(len(Coord)):
        ligne = Coord[x].split("|")
        for pt in ligne:
            if pt != '\n':
                coord_x.append(int(pt.split(',')[0]))
                coord_y.append(int(pt.split(',')[1]))
    
    f=open("log_dist.txt",'w')
    distance = 0
    sortie=()
    for ligne_pxl in ImgXY :
        if ligne_pxl != []:
            for p1 in ligne_pxl :
                
                for x in ImgXY:
                    if x != []:
                        for pt in x :
                            
                            if pt!=p1:
                                dist = calc_distance(p1,pt)
                                if dist > distance:
                                    distance=dist
                                    sortie=(p1,pt)
                                    f.write(f"{sortie}=>{distance} \n")
    f.close()
    distance_f = round(distance)
    pt_x = [len(Matrice)-sortie[0][0],len(Matrice)-sortie[1][0]]
    pt_y = [sortie[0][1],sortie[1][1]]
    end = timer()
    print(f"{end - start}s")

    plt.scatter(coord_y, coord_x)
    plt.plot(pt_y,pt_x,'-o',c='red',label=f"distance = {distance_f}")
    
    for i, j in zip(pt_y, pt_x):
        plt.text(i, j+0.5, '({}, {})'.format(i, j))
    
    plt.legend()
    plt.savefig('out.png')
    plt.show()
    

