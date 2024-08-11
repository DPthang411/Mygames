from ursina import *
from math import atan2, degrees
import random
class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.model = 'quad'
        self.color = color.red
        self.collider = 'box'
        self.position = (x,y)

class Bullet(Entity):
    def __init__(self, owner):
        super().__init__()
        self.model = 'quad'
        self.scale = (0.5,0.3)
        self.owner = owner
        self.rotation_z = self.owner.rotation_z
        self.collider = 'box'
    def update(self):
        self.position += self.right * 0.1
        if self.x >= self.owner.x + 6.7 or self.x <= self.owner.x - 6.7 or self.y >= self.owner.y + 3.55 or self.y <= self.owner.y - 3.55:
            destroy(self)
        hitinfo=self.intersects(ignore=[self])
        if type(hitinfo.entity) == Enemy:
            destroy(self)
            destroy(hitinfo.entity)

class Player(Entity):
    def __init__(self, parent):
        super().__init__()
        self.model = 'quad'
        self.color = color.green
        self.collider = 'box'
        self.on_cooldown = False
        self.list = []
        self.parent = parent
    def shoot(self):
        if self.on_cooldown == False:
            bullet = Bullet(self)
            self.on_cooldown = True
            self.list.append(bullet)
            invoke(setattr, self, 'on_cooldown', False, delay=0.25)
    def update(self):
        rot_mouse = atan2(mouse.x, mouse.y)
        self.rotation_z = degrees(rot_mouse) - 90
        if held_keys['left mouse']:
            if self.parent.enabled == True:
                self.shoot()
class Scene1(Entity):
    def __init__(self):
        super().__init__()
        self.char = Player(self)
        self.bullets = self.char.list
        self.enemies = []
        self.create_enemies()
    def create_enemies(self):
        if self.enabled == True:
            x = random.choice((8,9,7,8.1,8.2,8.3,9.1,9.2,9.3,7.1,7.2,7.3,-8,-9,-7,-8.1,-8.2,-8.3,-9.1,-9.2,-9.3,-7.1,-7.2,-7.3))
            y = random.uniform(-5,5)
            enemy = Enemy(x, y)
            enemy.add_script(SmoothFollow(target = self.char, speed = 0.5))
            self.enemies.append(enemy)
            invoke(self.create_enemies, delay = 3)
            
    def destroy_bullet(self):
        for bullet in self.bullets:
            destroy(bullet)
        self.bullets.clear()
    def destroy_enemy(self):
        for enemy in self.enemies:
            destroy(enemy)
        self.enemies.clear()
class Retry(Button):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.text = 'Retry'
        self.text_size = 10
        self.position = (10,10)
        self.color = color.red
        self.scale = (0.1,0.1)
def enabled():
    scene1.enabled = True
def update():
    if type(scene1.char.intersects().entity) == Enemy:
        scene1.enabled = False
        scene1.destroy_bullet()
        scene1.destroy_enemy()
        retry.position = (0,0)
    if retry.hovered == True:
        if held_keys['left mouse']:
            enabled()
            retry.position = (10,10)

app = Ursina()
retry = Retry()
scene1 = Scene1()
app.run()