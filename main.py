import sys, pygame, random, requests, json, math
from pygame import mixer

pygame.init()
mixer.init()

# Easter egg Star Wars
mixer.music.load('music/impwalk.mp3')

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
w,h = pygame.display.get_surface().get_size()
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
show_infos("Espace pour ⏯",infosGenX, infosGenY+60, (255,255,255), secondFont)

show_infos("📖 Cliquez sur une", w-infosGenX-150, 10, (255,255,255), secondFont)
show_infos("planète pour avoir", w-infosGenX-150, 30, (255,255,255), secondFont)
show_infos("ses informations !", w-infosGenX-150, 50, (255,255,255), secondFont)

show_infos("© Lucas Goï - 2022", infosGenX, h-30, (255,255,255), secondFont)

textBoxWidth = w/9
textBoxHeight = h/9

# ASTRES SYSTEME SOLAIRE

# Définition des couleurs
MERCURE_COLOR = (128, 128, 128)
VENUS_COLOR = (255, 153, 51)
TERRE_COLOR = (0, 153, 255)
MARS_COLOR = (204, 51, 0)
JUPITER_COLOR = (255, 204, 102)
SATURNE_COLOR = (153, 153, 102)
URANUS_COLOR = (102, 153, 255)
NEPTUNE_COLOR = (51, 102, 255)

def getPlanetInfos(id):
    match id:
        case 'mercure':
            return (MERCURE_COLOR, 10, 10, 3, 100)
        case 'venus':
            return (VENUS_COLOR, 10, textBoxHeight * 2, 2, 130)
        case 'terre':
            return (TERRE_COLOR, 10, textBoxHeight * 4, 0, 160)
        case 'mars':
            return (MARS_COLOR, 10, textBoxHeight * 6, 1.5, 190)
        case 'jupiter':
            return (JUPITER_COLOR, w-textBoxWidth-10, 10, 2, 280)
        case 'saturne':
            return (SATURNE_COLOR, w-textBoxWidth-10, textBoxHeight * 2, -1, 420)
        case 'uranus':
            return (URANUS_COLOR, w-textBoxWidth-10, textBoxHeight * 4, 3, 510)
        case 'neptune':
            return (NEPTUNE_COLOR, w-textBoxWidth-10, textBoxHeight * 6, 1, 560)


class Planet:
    def __init__(self, name, radius, density, gravity, avgTemp, mass, tupleInfos, number):
        self.name = name
        self.radius = radius / 1000 # Pour garder la proportionnalité entre les planètes, seulement le soleil ne l'est pas car trop grand
        self.density = density
        self.gravity = gravity
        self.avgTemp = avgTemp - 273,15 # Pour passer de °K à °C
        self.mass = mass
        self.color, self.textX, self.textY, self.angle, self.axe = tupleInfos
        self.number = number

    isClicked = False
    selectColor = (0, 0, 0)
    
    def onClick(self):
        pygame.draw.rect(screen, (50, 50, 50), (self.textX,self.textY, textBoxWidth, textBoxHeight))
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
            pygame.draw.rect(screen, (0, 0, 0), (self.textX,self.textY, textBoxWidth, textBoxHeight))


class Star:
    def __init__(self, name, radius, color, imgPath):
        self.name = name
        self.radius = radius
        self.color = color
        self.img = pygame.image.load(imgPath)
        self.img = pygame.transform.scale(self.img, (160, 160))


soleil = Star("soleil", 80, (255, 213, 0), "img/sun.png")
soleil.isNormal = True


# Marre du soleil classique ? Essayez plutôt le côté obscur...
def switchStar():
    if(soleil.isNormal == True):
        pygame.draw.circle(screen, (0, 0, 0), (w/2, h/2), soleil.radius)
        soleil.img = pygame.image.load('img/deathstar.png')
        soleil.img = pygame.transform.scale(soleil.img, (160, 160))
        soleil.isNormal = False
        mixer.music.play()
    else:
        pygame.draw.circle(screen, (0, 0, 0), (w/2, h/2), soleil.radius)
        soleil.img = pygame.image.load('img/sun.png')
        soleil.img = pygame.transform.scale(soleil.img, (160, 160))
        soleil.isNormal = True
        mixer.music.stop()

# DEFINITIONS PLANETES
planetsList = ['mercure', 'venus', 'terre', 'mars', 'jupiter', 'saturne', 'uranus', 'neptune']
planets = []
index = 1
for planet in planetsList:
    planetInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/"+planet)
    planetData = json.loads(planetInfos.text)
    planets.append(Planet(planetData['name'], planetData['meanRadius'], planetData['density'], planetData['gravity'], planetData['avgTemp'], planetData['mass'], getPlanetInfos(planetData['id']), index))
    index += 1


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
        if event.type == pygame.KEYDOWN:
            print(event.key, event.unicode, event.scancode)
            if event.key == pygame.K_ESCAPE:
                play = False
            if event.key == pygame.K_d:
                switchStar()
            if event.key == pygame.K_UP:
                speedUp()
            if event.key == pygame.K_DOWN:
                slowDown() 
            if event.key == pygame.K_SPACE:
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type==pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                pause = False
                                pygame.event.clear()
                                break
                            if event.key == pygame.K_ESCAPE:
                                play = False
                                pause = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if screen.get_at(pygame.mouse.get_pos()) == planets[0].color:
                planets[0].onClick()
                print('mercure')
            if screen.get_at(pygame.mouse.get_pos()) == planets[1].color:
                planets[1].onClick()
                print('venus')
            if screen.get_at(pygame.mouse.get_pos()) == planets[2].color:
                planets[2].onClick()
                print('terre')
            if screen.get_at(pygame.mouse.get_pos()) == planets[3].color:
                planets[3].onClick()
                print('mars')
            if screen.get_at(pygame.mouse.get_pos()) == planets[4].color:
                planets[4].onClick()
                print('jupiter')
            if screen.get_at(pygame.mouse.get_pos()) == planets[5].color:
                planets[5].onClick()
                print('saturne')
            if screen.get_at(pygame.mouse.get_pos()) == planets[6].color:
                planets[6].onClick()
                print('uranus')
            if screen.get_at(pygame.mouse.get_pos()) == planets[7].color:
                planets[7].onClick()
                print('neptune')
                

    # Affichage des étoiles
    i = 0
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), star, starsRadius[i])
        i += 1

    # Affichage du soleil
    screen.blit(soleil.img, (w/2 - soleil.radius, h/2 - soleil.radius))

    # Pour chaque planète je dessine son axe de rotation, le cercle noir qui cache le blanc pour éviter les traits, le cercle blanc quand elle est sélectionnée et la planète 
    for planet in planets:
        pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), planet.axe, width=1)
        pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(planet.angle+0.01) * planet.axe , h/2 + math.sin(planet.angle+0.01) * planet.axe), planet.radius + 6)
        pygame.draw.circle(screen, planet.selectColor, (w/2 + math.cos(planet.angle) * planet.axe, h/2 + math.sin(planet.angle) * planet.axe), planet.radius + 3)
        pygame.draw.circle(screen, planet.color, (w/2 + math.cos(planet.angle) * planet.axe, h/2 + math.sin(planet.angle) * planet.axe), planet.radius)
 

    planets[0].angle -= 0.01 + acceleration * 10 
    planets[1].angle -= 0.008 + acceleration * 8
    planets[2].angle -= 0.006 + acceleration * 6
    planets[3].angle -= 0.004 + acceleration * 4
    planets[4].angle -= 0.002 + acceleration * 2
    planets[5].angle -= 0.0009 + acceleration * 0.9
    planets[6].angle -= 0.0007 + acceleration * 0.7
    planets[7].angle -= 0.0005 + acceleration * 0.5
    # les valeurs ne sont pas celles de l'API car les vitesses réelles n'auraient aucun sens dans cette simulation
    # Mercure est 684 fois plus rapide que Neptune par exemple
    # donc j'ai mis des valeurs décroissantes pour quand même voir la différence de vitesse mais ne sont pas représentatives de la réalité
    # les * 10, * 8, * 6... font en sorte que l'accelération soit proportionnelle à la vitesse de base

    clock.tick(60)
    pygame.display.flip()