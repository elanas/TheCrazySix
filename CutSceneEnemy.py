from Enemy import Enemy


class CutSceneEnemy(Enemy):
    WALK_ANIM_TIME = .10
    VELOCITY = 220
    WAIT_TIME = 1.5

    def __init__(self, centerx, target_y, level):
        super(CutSceneEnemy, self).__init__()
        self.direction = Enemy.INDEX_DOWN
        self.image = Enemy.images[self.direction][0]
        self.anim_time = 0
        self.cycle = 0
        self.is_moving = True
        self.rect.bottom = -1
        self.rect.centerx = centerx
        self.target_y = target_y
        self.velocity = CutSceneEnemy.VELOCITY
        self.level = level
        self.time_waiting = 0
        self.is_waiting = False
        self.has_paused = False

    def update(self, time, camera=None):
        if self.velocity < 0 and self.rect.bottom < 0:
            return
        if self.is_waiting:
            self.time_waiting += time
            if self.time_waiting >= CutSceneEnemy.WAIT_TIME:
                self.is_waiting = False
                self.time_waiting = 0
                self.direction = Enemy.INDEX_UP
                self.image = Enemy.images[self.direction][self.cycle]
                self.level.handle_unpause()
            return
        self.rect.bottom += time * self.velocity
        if self.rect.bottom > self.target_y and not self.has_paused:
            self.has_paused = True
            self.rect.bottom = self.target_y
            self.velocity *= -1
            self.is_waiting = True
            self.level.handle_pause()

        if self.is_moving:
            self.anim_time += time
            if self.anim_time >= CutSceneEnemy.WALK_ANIM_TIME:
                self.anim_time = 0
                self.cycle = (self.cycle + 1) % len(Enemy.images[self.direction])
                self.image = Enemy.images[self.direction][self.cycle]
                old_rect = self.rect
                self.rect = self.image.get_rect()
                self.rect.center = old_rect.center