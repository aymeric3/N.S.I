import pyxel
import random

class Joueur1:
    def __init__(self):
        self.x = 10  # position horizontale du joueur 1
        self.y = pyxel.height / 2 - 10  # position verticale du joueur 1 (au milieu de l'écran)
        self.width = 5  # largeur de la raquette du joueur 1
        self.height = 20  # hauteur de la raquette du joueur 1
        self.vitesse = 4  # vitesse à laquelle le joueur 1 se déplace

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.y = max(0, self.y - self.vitesse)  # déplace la raquette vers le haut sans sortir de l'écran
        if pyxel.btn(pyxel.KEY_Q):
            self.y = min(pyxel.height - self.height, self.y + self.vitesse)  # déplace la raquette vers le bas sans sortir de l'écran

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 9)  # dessine la raquette du joueur 1 en rouge

    def collision(self, balle):
        # vérifie si la balle entre en collision avec la raquette du joueur 1
        if (balle.x <= self.x + self.width and
            balle.x + balle.width >= self.x and
            balle.y + balle.height >= self.y and
            balle.y <= self.y + self.height):
            balle.angle = 180 - balle.angle  # inverse la direction horizontale de la balle
            balle.vitesse += 0.2  # augmente légèrement la vitesse de la balle

class Joueur2:
    def __init__(self, is_ai=False):
        self.x = pyxel.width - 15  # position horizontale du joueur 2 (à droite de l'écran)
        self.y = pyxel.height / 2 - 10  # position verticale du joueur 2 (au milieu de l'écran)
        self.width = 5  # largeur de la raquette du joueur 2
        self.height = 20  # hauteur de la raquette du joueur 2
        self.vitesse = 3  # vitesse à laquelle le joueur 2 se déplace
        self.is_ai = is_ai  # indique si le joueur 2 est contrôlé par l'ordinateur (True) ou par un humain (False)
        self.reaction_delay = 0  # compteur pour ajouter un délai de réaction à l'ordinateur

    def update(self, balle):
        if self.is_ai:
            # si le joueur 2 est contrôlé par l'ordinateur, on exécute cette partie du code pour le faire bouger automatiquement
            self.reaction_delay += 1  # on augmente le compteur de délai de réaction à chaque mise à jour
            if self.reaction_delay > 3:
                # si le compteur de délai est supérieur à 3, l'ordinateur réagit (ce délai rend l'IA moins parfaite et donc battable)
                # on compare la position verticale de la balle avec le centre de la raquette du joueur 2
                if balle.y < self.y + self.height / 2:
                    # si la balle est au-dessus de la raquette, on déplace la raquette vers le haut
                    self.y = max(0, self.y - self.vitesse)  # on s'assure que la raquette ne sort pas de l'écran
                elif balle.y > self.y + self.height / 2:
                    # si la balle est en dessous de la raquette, on déplace la raquette vers le bas
                    self.y = min(pyxel.height - self.height, self.y + self.vitesse)  # on s'assure que la raquette ne sort pas de l'écran
                self.reaction_delay = 0  # on réinitialise le compteur de délai de réaction à zéro
            # cette logique crée un effet de délai de réaction chez le bot, le rendant moins parfait et donc possible à battre
        else:
            # si le joueur 2 est contrôlé par un humain, on utilise les touches du clavier pour le déplacer
            if pyxel.btn(pyxel.KEY_UP):
                self.y = max(0, self.y - self.vitesse)  # déplace la raquette vers le haut sans sortir de l'écran
            if pyxel.btn(pyxel.KEY_DOWN):
                self.y = min(pyxel.height - self.height, self.y + self.vitesse)  # déplace la raquette vers le bas sans sortir de l'écran

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 11)  # dessine la raquette du joueur 2 en bleu

    def collision(self, balle):
        # vérifie si la balle entre en collision avec la raquette du joueur 2
        if (balle.x + balle.width >= self.x and
            balle.x <= self.x + self.width and
            balle.y + balle.height >= self.y and
            balle.y <= self.y + self.height):
            balle.angle = 180 - balle.angle  # inverse la direction horizontale de la balle
            balle.vitesse += 0.2  # augmente légèrement la vitesse de la balle

class Balle:
    def __init__(self):
        self.reset()  # initialise la balle
        self.game_over = None  # indique si un point a été marqué

    def reset(self):
        self.x = pyxel.width / 2 - 2  # place la balle au centre horizontal de l'écran
        self.y = pyxel.height / 2 - 2  # place la balle au centre vertical de l'écran
        self.width = 4  # largeur de la balle
        self.height = 4  # hauteur de la balle
        angles = [random.randint(-60, 60), random.randint(120, 240)]  # liste des angles possibles pour la balle
        self.angle = random.choice(angles)  # choisit un angle aléatoire pour la direction de la balle
        self.vitesse = 2  # vitesse initiale de la balle
        # ne pas réinitialiser game_over ici pour conserver l'information du dernier point marqué

    def update(self):
        if not self.game_over:
            self.x += self.vitesse * pyxel.cos(self.angle)  # met à jour la position horizontale de la balle
            self.y -= self.vitesse * pyxel.sin(self.angle)  # met à jour la position verticale de la balle

            # gestion des rebonds sur les murs supérieur et inférieur
            if self.y <= 0:
                self.y = 0  # empêche la balle de sortir par le haut
                self.angle = -self.angle  # inverse la direction verticale de la balle
            elif self.y >= pyxel.height - self.height:
                self.y = pyxel.height - self.height  # empêche la balle de sortir par le bas
                self.angle = -self.angle  # inverse la direction verticale de la balle

            # vérifie si un joueur a marqué un point
            if self.x + self.width <= 0:
                self.game_over = "Bot"  # le bot (joueur 2) a marqué un point
            elif self.x >= pyxel.width:
                self.game_over = "Joueur 1"  # le joueur 1 a marqué un point

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, 7)  # dessine la balle en blanc

class Game:
    def __init__(self):
        pyxel.init(160, 120, title="POOng", fps=60)  # initialise la fenêtre du jeu avec une taille et un titre
        self.j1 = Joueur1()  # crée une instance du joueur 1
        self.j2 = Joueur2(is_ai=True)  # crée une instance du joueur 2 contrôlé par l'ordinateur
        self.b = Balle()  # crée une instance de la balle
        self.score_j1 = 0  # initialise le score du joueur 1 à 0
        self.score_j2 = 0  # initialise le score du joueur 2 (bot) à 0
        self.win_message_timer = 0  # initialise le compteur pour l'affichage du message du dernier point
        self.last_scorer = None  # variable pour stocker le nom du dernier joueur ayant marqué
        pyxel.run(self.update, self.draw)  # démarre la boucle principale du jeu

    def update(self):
        if not self.b.game_over:
            # met à jour les éléments du jeu si personne n'a marqué
            self.j1.update()  # met à jour le joueur 1
            self.j2.update(self.b)  # met à jour le joueur 2 en passant la balle (pour l'IA)
            self.b.update()  # met à jour la balle
            self.j1.collision(self.b)  # vérifie la collision entre la balle et le joueur 1
            self.j2.collision(self.b)  # vérifie la collision entre la balle et le joueur 2
        else:
            # si un joueur a marqué un point
            if self.b.game_over == "Joueur 1":
                self.score_j1 += 1  # augmente le score du joueur 1
            elif self.b.game_over == "Bot":
                self.score_j2 += 1  # augmente le score du bot
            self.last_scorer = self.b.game_over  # enregistre le nom du joueur qui a marqué
            self.win_message_timer = pyxel.frame_count  # enregistre le temps actuel pour l'affichage du message
            self.b.reset()  # réinitialise la balle pour le prochain point
            self.b.game_over = None  # réinitialise l'indicateur de fin de point

    def draw(self):
        pyxel.cls(0)  # efface l'écran avec la couleur noire
        # dessine la ligne centrale du terrain
        for i in range(0, pyxel.height, 10):
            pyxel.line(pyxel.width / 2, i, pyxel.width / 2, i + 5, 13)  # dessine une ligne pointillée en rose
        self.j1.draw()  # dessine la raquette du joueur 1
        self.j2.draw()  # dessine la raquette du joueur 2
        self.b.draw()  # dessine la balle
        # affiche les scores des joueurs
        pyxel.text(20, 5, f"J1: {self.score_j1}", 9)  # affiche le score du joueur 1 en rouge
        pyxel.text(pyxel.width - 50, 5, f"Bot: {self.score_j2}", 11)  # affiche le score du bot en bleu
        # affiche un message temporaire indiquant qui a marqué
        if self.win_message_timer > 0 and pyxel.frame_count - self.win_message_timer < 60:
            message = f"{self.last_scorer} a marqué !"  # crée le message à afficher
            # affiche le message au centre de l'écran en orange
            pyxel.text(pyxel.width / 2 - len(message) * 2, pyxel.height / 2 - 4, message, 8)

Game()  # crée une instance du jeu et lance le jeu

# SI VOUS VOULEZ JOUER à DEUX, IL SUFFIT DE MODIFIER LA LIGNE 115, EN MODIFIANT LE "is_ai", METTEZ "False" à la place de True!!
