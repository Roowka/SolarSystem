import sys, pygame, random, requests, json, math
pygame.init()

w,h = 1600, 1000
screen = pygame.display.set_mode((w,h))
print(pygame.display.get_window_size())

screen.fill((0, 0, 0))  

# GESTION TEXTES
titleFont = pygame.font.Font('freesansbold.ttf', 16)
mainFont = pygame.font.Font('freesansbold.ttf', 14)
# smallFont est compatible avec les emojis
secondFont = pygame.font.SysFont("segoeuisymbol", 15)

# Fonction d'affichage de texte
def show_infos(text, x, y, color, font):
    infos = font.render(text, True, color)
    screen.blit(infos, (x, y))


# Générateur d'étoiles
nbStars = 500
stars = []
for i in range(nbStars):
    starX = random.randint(0,w)
    starY = random.randint(0,h)
    stars.append((starX, starY))

starsRadius = []
for i in range(nbStars):
    radius = random.uniform(0.5, 2.5)
    starsRadius.append(radius)


# Affichage des infos générales
infosGenX = 250
infosGenY = 10

show_infos("Système solaire", infosGenX, infosGenY, (252, 219, 3), titleFont)
show_infos("🡱 pour accélérer", infosGenX, infosGenY +20, (255,255,255), secondFont)
show_infos("🡳 pour ralentir", infosGenX, infosGenY +40, (255,255,255), secondFont)
show_infos("© Lucas Goï - 2022", infosGenX, infosGenY +60, (255,255,255), secondFont)

show_infos("📖 Cliquez sur une", w-infosGenX-150, 10, (255,255,255), secondFont)
show_infos("planète pour avoir", w-infosGenX-150, 30, (255,255,255), secondFont)
show_infos("ses informations !", w-infosGenX-150, 50, (255,255,255), secondFont)

# ASTRES SYSTEME SOLAIRE

class Planet:
    def __init__(self, name, radius, density, gravity, avgTemp, mass, color, textX, textY, angle, number):
        self.name = name
        self.radius = radius / 1000 # Pour garder la proportionnalité entre les planètes, seulement le soleil ne l'est pas car trop grand
        self.density = density
        self.gravity = gravity
        self.avgTemp = avgTemp - 273,15 # Pour passer de °K à °C
        self.mass = mass
        self.color = color
        self.textX = textX
        self.textY = textY
        self.angle = angle
        self.number = number

    isClicked = False
    selectColor = (0, 0, 0)
    
    def onClick(self):
        pygame.draw.rect(screen, (50, 50, 50), (self.textX,self.textY, 205, 110))
        if self.isClicked == False:
            self.isClicked = True
            self.selectColor = (255, 255, 255)
            show_infos(str(self.number)+". "+self.name, self.textX+5, self.textY+5, self.color, titleFont)
            show_infos("Densité : "+str(self.density)+" g/cm³", self.textX+5, self.textY+25, (255, 255, 255), mainFont)
            show_infos("Gravité : "+str(self.gravity)+" m/s²", self.textX+5, self.textY+45, (255, 255, 255), mainFont)
            show_infos("Température ~ : "+str(self.avgTemp)+"°C", self.textX+5, self.textY+65, (255, 255, 255), mainFont)
            show_infos("Masse : "+str(self.mass['massValue'])+"x10^"+str(self.mass['massExponent'])+" kg", self.textX+5, self.textY+85, (255, 255, 255), mainFont)
        else:
            self.isClicked = False
            self.selectColor = (0, 0, 0)
            pygame.draw.rect(screen, (0, 0, 0), (self.textX,self.textY, 225, 110))


class Star:
    def __init__(self, name, radius, color, imgPath):
        self.name = name
        self.radius = radius
        self.color = color
        self.img = pygame.image.load(imgPath)
        self.img = pygame.transform.scale(self.img, (160, 160))

class Axe:
    pass

soleil = Star("soleil", 80, (255, 213, 0), "img/sun.png")

# DEFINITIONS PLANETES

# Pour chaque planète je définie un axe de rotation
# J'ai fait une classe au cas ou j'ai besoin de plus d'informations
axeMercure = Axe()
axeMercure.radius = 100

# Je récupère les données de chaque planète avec l'api <<api.le-systeme-solaire.net>> et je construis mes objets planètes avec ces données
mercureInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/mercure")
mercureData = json.loads(mercureInfos.text)
mercure = Planet(mercureData['name'], mercureData['meanRadius'], mercureData['density'], mercureData['gravity'], mercureData['avgTemp'], mercureData['mass'], (128, 128, 128), 10, 10, 3, 1)  
 

axeVenus = Axe()
axeVenus.radius = 130

venusInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/venus")
venusData = json.loads(venusInfos.text)
venus = Planet(venusData['name'], venusData['meanRadius'], venusData['density'], venusData['gravity'], venusData['avgTemp'], venusData['mass'], (255, 153, 51), 10, 260, 2, 2) 


axeTerre = Axe()
axeTerre.radius = 160

terreInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/terre")
terreData = json.loads(terreInfos.text)
terre = Planet(terreData['name'], terreData['meanRadius'], terreData['density'], terreData['gravity'], terreData['avgTemp'], terreData['mass'], (0, 153, 255), 10, 600, 0, 3)


axeMars = Axe()
axeMars.radius = 190

marsInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/mars")
marsData = json.loads(marsInfos.text)
mars = Planet(marsData['name'], marsData['meanRadius'], marsData['density'], marsData['gravity'], marsData['avgTemp'], marsData['mass'], (204, 51, 0), 10, 850, 1.5, 4)


axeJupiter = Axe()
axeJupiter.radius = 280

jupiterInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/jupiter")
jupiterData = json.loads(jupiterInfos.text)
jupiter = Planet(jupiterData['name'], jupiterData['meanRadius'], jupiterData['density'], jupiterData['gravity'], jupiterData['avgTemp'], jupiterData['mass'], (255, 204, 102), 1385, 10, 2, 5) 


axeSaturne = Axe()
axeSaturne.radius = 420

saturneInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/saturne")
saturneData = json.loads(saturneInfos.text)
saturne = Planet(saturneData['name'], saturneData['meanRadius'], saturneData['density'], saturneData['gravity'], saturneData['avgTemp'], saturneData['mass'], (153, 153, 102), 1385, 260, -1, 6)


axeUranus = Axe()
axeUranus.radius = 510

uranusInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/uranus")
uranusData = json.loads(uranusInfos.text)
uranus = Planet(uranusData['name'], uranusData['meanRadius'], uranusData['density'], uranusData['gravity'], uranusData['avgTemp'], uranusData['mass'], (102, 153, 255), 1385, 600, 3, 7)


axeNeptune = Axe()
axeNeptune.radius = 560

neptuneInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/neptune")
neptuneData = json.loads(neptuneInfos.text)
neptune = Planet(neptuneData['name'], neptuneData['meanRadius'], neptuneData['density'], neptuneData['gravity'], neptuneData['avgTemp'], neptuneData['mass'], (51, 102, 255), 1385, 850, 1, 8)

# GESTION ACCELERATION
acceleration = 0
isAccelerated = False

def speedUp():
    global isAccelerated
    global acceleration
    if(isAccelerated == False):
        acceleration = 0.002
        isAccelerated = True

def slowDown():
    global isAccelerated
    global acceleration
    if(isAccelerated == True):
        acceleration = 0
        isAccelerated = False

# GESTION BOUTON PAUSE
pause = False
play = True

clock = pygame.time.Clock()

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEMOTION:
            pass
            # print(event.pos)
        if event.type == pygame.KEYDOWN:
            print(event.key, event.unicode, event.scancode)
            if event.key == pygame.K_ESCAPE:
                play = False
            if event.key == pygame.K_UP:
                speedUp() 
            if event.key == pygame.K_DOWN:
                slowDown() 
            if event.key == pygame.K_SPACE:
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            pause = False
                            pygame.event.clear()
                            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if screen.get_at(pygame.mouse.get_pos()) == mercure.color:
                mercure.onClick()
                print('mercure')
            if screen.get_at(pygame.mouse.get_pos()) == venus.color:
                venus.onClick()
                print('venus')
            if screen.get_at(pygame.mouse.get_pos()) == terre.color:
                terre.onClick()
                print('terre')
            if screen.get_at(pygame.mouse.get_pos()) == mars.color:
                mars.onClick()
                print('mars')
            if screen.get_at(pygame.mouse.get_pos()) == jupiter.color:
                jupiter.onClick()
                print('jupiter')
            if screen.get_at(pygame.mouse.get_pos()) == saturne.color:
                saturne.onClick()
                print('saturne')
            if screen.get_at(pygame.mouse.get_pos()) == uranus.color:
                uranus.onClick()
                print('uranus')
            if screen.get_at(pygame.mouse.get_pos()) == neptune.color:
                neptune.onClick()
                print('neptune')
                

    # Affichage des étoiles
    i = 0
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), star, starsRadius[i])
        i += 1

    # Affichage du soleil
    screen.blit(soleil.img, (w/2 - soleil.radius, h/2 - soleil.radius))

    # Pour chaque planète je dessine son axe de rotation, la planète, le cercle blanc quand elle est sélectionnée et le cercle noir qui cache le blanc pour éviter les traits
    # Je ne remets pas le fond en noir pour ne pas cacher les différents textes
    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeMercure.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(mercure.angle+0.01) * axeMercure.radius , h/2 + math.sin(mercure.angle+0.01) * axeMercure.radius), mercure.radius + 6, width=6)
    pygame.draw.circle(screen, mercure.color, (w/2 + math.cos(mercure.angle) * axeMercure.radius, h/2 + math.sin(mercure.angle) * axeMercure.radius), mercure.radius)
    pygame.draw.circle(screen, mercure.selectColor, (w/2 + math.cos(mercure.angle) * axeMercure.radius, h/2 + math.sin(mercure.angle) * axeMercure.radius), mercure.radius + 3, width=3) 

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeVenus.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(venus.angle+0.009) * axeVenus.radius , h/2 + math.sin(venus.angle+0.009) * axeVenus.radius), venus.radius + 6, width=6)
    pygame.draw.circle(screen, venus.color, (w/2 + math.cos(venus.angle) * axeVenus.radius, h/2 + math.sin(venus.angle) * axeVenus.radius), venus.radius)
    pygame.draw.circle(screen, venus.selectColor, (w/2 + math.cos(venus.angle) * axeVenus.radius, h/2 + math.sin(venus.angle) * axeVenus.radius), venus.radius + 3, width=3)
    
    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeTerre.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(terre.angle+0.008) * axeTerre.radius , h/2 + math.sin(terre.angle+0.008) * axeTerre.radius), terre.radius + 6, width=6)
    pygame.draw.circle(screen, terre.selectColor, (w/2 + math.cos(terre.angle) * axeTerre.radius, h/2 + math.sin(terre.angle) * axeTerre.radius), terre.radius + 3, width=3)
    pygame.draw.circle(screen, terre.color, (w/2 + math.cos(terre.angle) * axeTerre.radius, h/2 + math.sin(terre.angle) * axeTerre.radius), terre.radius)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeMars.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(mars.angle+0.007) * axeMars.radius , h/2 + math.sin(mars.angle+0.007) * axeMars.radius), mars.radius + 6, width=6)
    pygame.draw.circle(screen, mars.color, (w/2 + math.cos(mars.angle) * axeMars.radius, h/2 + math.sin(mars.angle) * axeMars.radius), mars.radius)
    pygame.draw.circle(screen, mars.selectColor, (w/2 + math.cos(mars.angle) * axeMars.radius, h/2 + math.sin(mars.angle) * axeMars.radius), mars.radius + 3, width=3)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeJupiter.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(jupiter.angle+0.006) * axeJupiter.radius , h/2 + math.sin(jupiter.angle+0.006) * axeJupiter.radius), jupiter.radius + 5, width=5)
    pygame.draw.circle(screen, jupiter.color, (w/2 + math.cos(jupiter.angle) * axeJupiter.radius, h/2 + math.sin(jupiter.angle) * axeJupiter.radius), jupiter.radius)
    pygame.draw.circle(screen, jupiter.selectColor, (w/2 + math.cos(jupiter.angle) * axeJupiter.radius, h/2 + math.sin(jupiter.angle) * axeJupiter.radius), jupiter.radius + 4, width=4)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeSaturne.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(saturne.angle+0.005) * axeSaturne.radius , h/2 + math.sin(saturne.angle+0.005) * axeSaturne.radius), saturne.radius + 5, width=5)
    pygame.draw.circle(screen, saturne.color, (w/2 + math.cos(saturne.angle) * axeSaturne.radius, h/2 + math.sin(saturne.angle) * axeSaturne.radius), saturne.radius)
    pygame.draw.circle(screen, saturne.selectColor, (w/2 + math.cos(saturne.angle) * axeSaturne.radius, h/2 + math.sin(saturne.angle) * axeSaturne.radius), saturne.radius + 4, width=4)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeUranus.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(uranus.angle+0.004) * axeUranus.radius , h/2 + math.sin(uranus.angle+0.004) * axeUranus.radius), uranus.radius + 5, width=5)
    pygame.draw.circle(screen, uranus.color, (w/2 + math.cos(uranus.angle) * axeUranus.radius, h/2 + math.sin(uranus.angle) * axeUranus.radius), uranus.radius)
    pygame.draw.circle(screen, uranus.selectColor, (w/2 + math.cos(uranus.angle) * axeUranus.radius, h/2 + math.sin(uranus.angle) * axeUranus.radius), uranus.radius + 4, width=4)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeNeptune.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(neptune.angle+0.003) * axeNeptune.radius , h/2 + math.sin(neptune.angle+0.003) * axeNeptune.radius), neptune.radius + 5, width=5)
    pygame.draw.circle(screen, neptune.color, (w/2 + math.cos(neptune.angle) * axeNeptune.radius, h/2 + math.sin(neptune.angle) * axeNeptune.radius), neptune.radius)
    pygame.draw.circle(screen, neptune.selectColor, (w/2 + math.cos(neptune.angle) * axeNeptune.radius, h/2 + math.sin(neptune.angle) * axeNeptune.radius), neptune.radius + 4, width=4)


    mercure.angle -= 0.01 + acceleration * 10 
    venus.angle -= 0.008 + acceleration * 8
    terre.angle -= 0.006 + acceleration * 6
    mars.angle -= 0.004 + acceleration * 4
    jupiter.angle -= 0.002 + acceleration * 2
    saturne.angle -= 0.0009 + acceleration * 0.9
    uranus.angle -= 0.0007 + acceleration * 0.7
    neptune.angle -= 0.0005 + acceleration * 0.5
    # les valeurs ne sont pas celles de l'API car les vitesses réelles n'auraient aucun sens dans cette simulation
    # Mercure est 684 fois plus rapide que Neptune par exemple
    # donc j'ai mis des valeurs décroissantes pour quand même voir la différence de vitesse mais ne sont pas représentatives de la réalité
    # les * 10, * 8, * 6... font en sorte que l'accelération soit proportionnelle à la vitesse de base

    clock.tick(60)
    pygame.display.flip()