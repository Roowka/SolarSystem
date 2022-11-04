import sys, pygame, random, requests, json, math
pygame.init()

w,h = 1600, 1000
screen = pygame.display.set_mode((w,h))
print(pygame.display.get_window_size())

screen.fill((0, 0, 0))

# GESTION TEXTES
font = pygame.font.Font('freesansbold.ttf', 16)

def show_infos(text, x, y, color):
    infos = font.render(text, True, color)
    screen.blit(infos, (x, y))

# ETOILES/PLANETES

# Générateur d'étoiles
nbStars = 500

for i in range(nbStars):
    starRadius = random.uniform(0.25, 2.5)
    starX = random.randint(0,w)
    starY = random.randint(0,h)
    pygame.draw.circle(screen, (255,255,255), (starX, starY), starRadius)



class Planet:
    def __init__(self, name, radius, density, gravity, avgTemp, mass, color, textX, textY, angle):
        self.name = name
        self.radius = radius / 1000 # Pour garder la proportionnalité entre les planètes, seulement le soleil ne l'est pas car trop grand
        self.density = density
        self.gravity = gravity
        self.avgTemp = avgTemp
        self.mass = mass
        self.color = color
        self.textX = textX
        self.textY = textY
        self.angle = angle

    isClicked = False
    selectColor = (0, 0, 0)
    def onClick(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.textX,self.textY, 200, 200))
        if self.isClicked == False:
            self.isClicked = True
            self.selectColor = (255, 255, 255)
            show_infos(self.name, self.textX, self.textY, self.color)
            show_infos("Densité : "+str(self.density)+" g/cm³", self.textX, self.textY+20, (255, 255, 255))
            show_infos("Gravité : "+str(self.gravity)+" m/s²", self.textX, self.textY+40, (255, 255, 255))
            show_infos("Température ~ : "+str(self.avgTemp)+"°K", self.textX, self.textY+60, (255, 255, 255))
            show_infos("Masse : "+str(self.mass['massValue'])+"x10^"+str(self.mass['massExponent'])+" kg", self.textX, self.textY+80, (255, 255, 255))
        else:
            self.isClicked = False
            self.selectColor = (0, 0, 0)


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

# Pour chaque planète je définie un axe de rotation
axeMercure = Axe()
axeMercure.radius = 100

# Je récupère les données de chaque planète avec l'api <<api.le-systeme-solaire.net>> et je construis mes objets planètes avec ces données
mercureInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/mercure")
mercureData = json.loads(mercureInfos.text)
mercure = Planet(mercureData['name'], mercureData['meanRadius'], mercureData['density'], mercureData['gravity'], mercureData['avgTemp'], mercureData['mass'], (128, 128, 128), 10, 10, 3)  
 

axeVenus = Axe()
axeVenus.radius = 130

venusInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/venus")
venusData = json.loads(venusInfos.text)
venus = Planet(venusData['name'], venusData['meanRadius'], venusData['density'], venusData['gravity'], venusData['avgTemp'], venusData['mass'], (255, 153, 51), 10, 260, 2) 


axeTerre = Axe()
axeTerre.radius = 160

terreInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/terre")
terreData = json.loads(terreInfos.text)
terre = Planet(terreData['name'], terreData['meanRadius'], terreData['density'], terreData['gravity'], terreData['avgTemp'], terreData['mass'], (0, 153, 255), 10, 510, 0)


axeMars = Axe()
axeMars.radius = 190

marsInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/mars")
marsData = json.loads(marsInfos.text)
mars = Planet(marsData['name'], marsData['meanRadius'], marsData['density'], marsData['gravity'], marsData['avgTemp'], marsData['mass'], (204, 51, 0), 10, 760, 1.5)


axeJupiter = Axe()
axeJupiter.radius = 280

jupiterInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/jupiter")
jupiterData = json.loads(jupiterInfos.text)
jupiter = Planet(jupiterData['name'], jupiterData['meanRadius'], jupiterData['density'], jupiterData['gravity'], jupiterData['avgTemp'], jupiterData['mass'], (255, 204, 102), 1390, 10, 0.5) 


axeSaturne = Axe()
axeSaturne.radius = 420

saturneInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/saturne")
saturneData = json.loads(saturneInfos.text)
saturne = Planet(saturneData['name'], saturneData['meanRadius'], saturneData['density'], saturneData['gravity'], saturneData['avgTemp'], saturneData['mass'], (153, 153, 102), 1390, 260, -1)


axeUranus = Axe()
axeUranus.radius = 510

uranusInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/uranus")
uranusData = json.loads(uranusInfos.text)
uranus = Planet(uranusData['name'], uranusData['meanRadius'], uranusData['density'], uranusData['gravity'], uranusData['avgTemp'], uranusData['mass'], (102, 153, 255), 1390, 510, 0)


axeNeptune = Axe()
axeNeptune.radius = 560

neptuneInfos = requests.get("https://api.le-systeme-solaire.net/rest/bodies/neptune")
neptuneData = json.loads(neptuneInfos.text)
neptune = Planet(neptuneData['name'], neptuneData['meanRadius'], neptuneData['density'], neptuneData['gravity'], neptuneData['avgTemp'], neptuneData['mass'], (51, 102, 255), 1390, 760, 1)


play = True
clock = pygame.time.Clock()

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEMOTION:
            pass
            # print(event.pos)
        if event.type == pygame.KEYUP:
            print(event.key, event.unicode, event.scancode)
            if event.key == pygame.K_ESCAPE:
                play = False
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
            

    # Affichage du soleil
    screen.blit(soleil.img, (w/2 - soleil.radius, h/2 - soleil.radius))

    # Pour chaque planète je dessine son axe de rotation, la planète, le cercle blanc quand elle est sélectionnée et le cercle noir qui cache le blanc pour éviter les traits
    # je remets pas le screen en noir pour ne pas cacher les étoiles
    # je ne regénère pas les étoiles pour ne pas qu'elles bougent
    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeMercure.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(mercure.angle+0.01) * axeMercure.radius , h/2 + math.sin(mercure.angle+0.01) * axeMercure.radius), mercure.radius + 3, width=3)
    pygame.draw.circle(screen, mercure.color, (w/2 + math.cos(mercure.angle) * axeMercure.radius, h/2 + math.sin(mercure.angle) * axeMercure.radius), mercure.radius)
    pygame.draw.circle(screen, mercure.selectColor, (w/2 + math.cos(mercure.angle) * axeMercure.radius, h/2 + math.sin(mercure.angle) * axeMercure.radius), mercure.radius + 3, width=3) 

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeVenus.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(venus.angle+0.009) * axeVenus.radius , h/2 + math.sin(venus.angle+0.009) * axeVenus.radius), venus.radius + 3, width=3)
    pygame.draw.circle(screen, venus.color, (w/2 + math.cos(venus.angle) * axeVenus.radius, h/2 + math.sin(venus.angle) * axeVenus.radius), venus.radius)
    pygame.draw.circle(screen, venus.selectColor, (w/2 + math.cos(venus.angle) * axeVenus.radius, h/2 + math.sin(venus.angle) * axeVenus.radius), venus.radius + 3, width=3)
    
    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeTerre.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(terre.angle+0.008) * axeTerre.radius , h/2 + math.sin(terre.angle+0.008) * axeTerre.radius), terre.radius + 3, width=3)
    pygame.draw.circle(screen, terre.selectColor, (w/2 + math.cos(terre.angle) * axeTerre.radius, h/2 + math.sin(terre.angle) * axeTerre.radius), terre.radius + 3, width=3)
    pygame.draw.circle(screen, terre.color, (w/2 + math.cos(terre.angle) * axeTerre.radius, h/2 + math.sin(terre.angle) * axeTerre.radius), terre.radius)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeMars.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(mars.angle+0.007) * axeMars.radius , h/2 + math.sin(mars.angle+0.007) * axeMars.radius), mars.radius + 3, width=3)
    pygame.draw.circle(screen, mars.color, (w/2 + math.cos(mars.angle) * axeMars.radius, h/2 + math.sin(mars.angle) * axeMars.radius), mars.radius)
    pygame.draw.circle(screen, mars.selectColor, (w/2 + math.cos(mars.angle) * axeMars.radius, h/2 + math.sin(mars.angle) * axeMars.radius), mars.radius + 3, width=3)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeJupiter.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(jupiter.angle+0.006) * axeJupiter.radius , h/2 + math.sin(jupiter.angle+0.006) * axeJupiter.radius), jupiter.radius + 3, width=4)
    pygame.draw.circle(screen, jupiter.color, (w/2 + math.cos(jupiter.angle) * axeJupiter.radius, h/2 + math.sin(jupiter.angle) * axeJupiter.radius), jupiter.radius)
    pygame.draw.circle(screen, jupiter.selectColor, (w/2 + math.cos(jupiter.angle) * axeJupiter.radius, h/2 + math.sin(jupiter.angle) * axeJupiter.radius), jupiter.radius + 3, width=4)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeSaturne.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(saturne.angle+0.005) * axeSaturne.radius , h/2 + math.sin(saturne.angle+0.005) * axeSaturne.radius), saturne.radius + 3, width=4)
    pygame.draw.circle(screen, saturne.color, (w/2 + math.cos(saturne.angle) * axeSaturne.radius, h/2 + math.sin(saturne.angle) * axeSaturne.radius), saturne.radius)
    pygame.draw.circle(screen, saturne.selectColor, (w/2 + math.cos(saturne.angle) * axeSaturne.radius, h/2 + math.sin(saturne.angle) * axeSaturne.radius), saturne.radius + 3, width=4)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeUranus.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(uranus.angle+0.004) * axeUranus.radius , h/2 + math.sin(uranus.angle+0.004) * axeUranus.radius), uranus.radius + 3, width=4)
    pygame.draw.circle(screen, uranus.color, (w/2 + math.cos(uranus.angle) * axeUranus.radius, h/2 + math.sin(uranus.angle) * axeUranus.radius), uranus.radius)
    pygame.draw.circle(screen, uranus.selectColor, (w/2 + math.cos(uranus.angle) * axeUranus.radius, h/2 + math.sin(uranus.angle) * axeUranus.radius), uranus.radius + 3, width=4)

    pygame.draw.circle(screen, (255, 255, 255), (w/2, h/2), axeNeptune.radius, width=1)
    pygame.draw.circle(screen, (0,0,0), (w/2 + math.cos(neptune.angle+0.003) * axeNeptune.radius , h/2 + math.sin(neptune.angle+0.003) * axeNeptune.radius), neptune.radius + 3, width=4)
    pygame.draw.circle(screen, neptune.color, (w/2 + math.cos(neptune.angle) * axeNeptune.radius, h/2 + math.sin(neptune.angle) * axeNeptune.radius), neptune.radius)
    pygame.draw.circle(screen, neptune.selectColor, (w/2 + math.cos(neptune.angle) * axeNeptune.radius, h/2 + math.sin(neptune.angle) * axeNeptune.radius), neptune.radius + 3, width=4)


    mercure.angle -= 0.01
    venus.angle -= 0.009
    terre.angle -= 0.008
    mars.angle -= 0.007
    jupiter.angle -= 0.006
    saturne.angle -= 0.005
    uranus.angle -= 0.004
    neptune.angle -= 0.003
    # Plus on s'éloigne du soleil plus elles mettent du temps à en faire le tour

    clock.tick(60)
    pygame.display.flip()