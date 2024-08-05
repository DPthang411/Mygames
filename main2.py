from ursina import *
from random import choice
class player(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.color = color.green
        self.y = -3
        self.collider = 'box'
    def input(self, key):
        if key == 'a':
            self.x -= 3
        if key == 'd':
            self.x += 3
    def update(self):
        if self.x >= 3:
            self.x = 3
        if self.x <= -3:
            self.x = -3
class collider_entity(Entity):
    def __init__(self, pos):
        super().__init__()
        self.model = 'quad'
        self.visible = False
        self.collider = 'box'
        self.position = pos
class enemy(Entity):
    def __init__(self, pos):
        super().__init__()
        self.model = 'quad'
        self.color = color.red
        self.collider = 'box'
        self.position = pos
    def update(self):
        self.y -= 0.1
        hit_info = self.intersects(ignore=[self])
        if type(hit_info.entity) == collider_entity:
            destroy(self)
        
class scene1(Entity):
    def __init__(self):
        super().__init__()
        self.collide1 = collider_entity(pos = (-3,-5))
        self.collide2 = collider_entity(pos = (0,-5))
        self.collide3 = collider_entity(pos = (3,-5))
        self.char = player()
        self.char.parent = self
        self.enemies = []
        self.create_enemies()
    def create_enemies(self):
        if self.enabled == True:
            x = self.char.x
            y = 5
            Enemy = enemy(pos = (x, y))
            self.enemies.append(Enemy)
        invoke(self.create_enemies, delay = 1.3)
    def destroy_enemies(self):
        for enemy in self.enemies:
            destroy(enemy)
        self.enemies.clear()
class Retry(Button):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.scale = (0.1,0.1)
        self.position = (50,50)
def enabled():
    scene1.enabled = True
app = Ursina(title='')
window.borderless = False
window.exit_button.visible = False
scene1 = scene1()
retry = Retry()
def update():
    if type(scene1.char.intersects().entity) == enemy:
        scene1.enabled = False
        scene1.destroy_enemies()
        retry.position = (0,0)
    if retry.hovered == True:
        if held_keys['left mouse']:
            enabled()
            retry.position = (10,10)
            
app.run()