from Enemy import Enemy


class CutSceneEnemy(Enemy):
    WALK_ANIM_TIME = .10
    VELOCITY = 220

    def __init__(self, centerx, target_y):
        super(CutSceneEnemy, self).__init__()
        self.direction = Enemy.INDEX_DOWN
        self.image = Enemy.images[self.direction][0]
        self.anim_time = 0
        self.cycle = 0
        self.is_moving = True
        self.rect.bottom = 0
        self.rect.centerx = centerx
        self.target_y = target_y
        self.velocity = CutSceneEnemy.VELOCITY

    def update(self, time, camera=None):
        self.rect.bottom += time * self.velocity
        if self.rect.bottom > self.target_y:
            self.rect.bottom = self.target_y
            self.velocity *= -1
            self.direction = Enemy.INDEX_UP
            self.image = Enemy.images[self.direction][self.cycle]

        if self.is_moving:
            self.anim_time += time
            if self.anim_time >= CutSceneEnemy.WALK_ANIM_TIME:
                self.anim_time = 0
                self.cycle = (self.cycle + 1) % len(Enemy.images[self.direction])
                self.image = Enemy.images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center