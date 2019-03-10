from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.sprite import Sprite
from track import Track
from cocos.actions.interval_actions import MoveTo
from background import BackgroundLayer
from config import player_controls
from coor import coor_to_real, coor_track_width
from pyglet.image import Animation, AnimationFrame, load
from cocos.collision_model import CollisionManager, AARectShape
from random import choice
import game_over_scene


class Item(Sprite):
    PLAYER = 0
    ANGRY_CLOUD = 1
    THUNDERBOLT = 2
    POCKET_WATCH = 3

    def __init__(self, image, position, itemType, scale = 0.4):
        super(Item, self).__init__(image, position, scale = scale)
        self.itemType = itemType


class Player(Item):
    def __init__(self, position):
        super(Player, self).__init__(
            Animation([
                AnimationFrame(load('assets/img/player1.png'), 0.2),
                AnimationFrame(load('assets/img/player2.png'), 0.2)
            ]),
            position,
            Item.PLAYER,
            scale = 0.5)


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()

        self.tracks = [Track(i) for i in range(5)]
        self.trackOrder = [i for i in range(5)]
        for track in self.tracks:
            self.add(track)

        self.collision_manager = CollisionManager()

        self.player = Player(coor_to_real(0.5, 0.1))
        self.add(self.player)

        self.items = []

        w, h = director.get_window_size()
        self.add(Sprite('assets/img/hand.png', (w * 0.1, h * 0.8)))

        self.scrolling_speed = 2.0
        self.schedule(self.scroll)
        self.schedule_interval(self.update_scrolling_speed, 0.1)
        self.schedule_interval(self.spawn_item, 0.5)

    def switch_tracks(self, k, l):
        i, j = self.tracks[k].i, self.tracks[k].j
        self.tracks[k].moveTo(self.tracks[l].i, self.tracks[l].j)
        self.tracks[l].moveTo(i, j)

        self.trackOrder[k], self.trackOrder[l] = self.trackOrder[l], self.trackOrder[k]

    def spawn_item(self, dt):
        x = choice([i + 0.5 for i in range(5)])
        itemType = choice([Item.ANGRY_CLOUD, Item.THUNDERBOLT, Item.POCKET_WATCH])

        item = None
        if itemType == Item.ANGRY_CLOUD:
            item = Item('assets/img/angry_cloud.png', coor_to_real(x, 1.1), Item.ANGRY_CLOUD)
        elif itemType == Item.THUNDERBOLT:
            item = Item('assets/img/thunderbolt.png', coor_to_real(x, 1.1), Item.THUNDERBOLT)
        elif itemType == Item.POCKET_WATCH:
            item = Item('assets/img/pocket_watch.png', coor_to_real(x, 1.1), Item.POCKET_WATCH)

        self.items.append(item)
        self.add(item)

    def on_key_press(self, key, modifiers):

        # on enter
        if key == 65293:
            self.switch_tracks(0, 1)
            self.switch_tracks(3, 2)
            self.switch_tracks(1, 3)
            self.switch_tracks(0, 4)
            return

        if key in player_controls['rainbow_keys']:
            k = player_controls['rainbow_keys'].index(key)
            x = self.tracks[k].x + coor_track_width() / 2.0
            self.player.do(MoveTo((x, self.player.y), duration = 0.1))

    def scroll(self, dt):
        to_remove = []
        for i, item in enumerate(self.items):
            item.y -= self.scrolling_speed
            if item.y < -item.height:
                self.remove(item)
                to_remove.append(i)

        for j, i in enumerate(to_remove):
            self.items = self.items[:i-j] + self.items[i-j+1:]

        to_remove = []
        for i, item in enumerate(self.items):
            if self.is_colliding_with_player(item):
                self.remove(item)
                to_remove.append(i)
                if item.itemType == Item.ANGRY_CLOUD:
                    # game over
                    director.replace(game_over_scene.create_game_over_scene())

                elif item.itemType == Item.THUNDERBOLT:
                    # switch tracks
                    li = range(5)
                    k = choice(li)
                    li.remove(k)
                    l = choice(li)

                    self.switch_tracks(k, l)

                elif item.itemType == Item.POCKET_WATCH:
                    # slow down time
                    self.scrolling_speed -= 1.5
                    if self.scrolling_speed < 2.0:
                        self.scrolling_speed = 2.0

        for j, i in enumerate(to_remove):
            self.items = self.items[:i-j] + self.items[i-j+1:]

    def update_scrolling_speed(self, dt):
        self.scrolling_speed += 0.08

    def is_colliding_with_player(self, item):
        return not (self.player.y + self.player.height/2 < item.y - self.player.height/2
            or self.player.y - self.player.height/2 > item.y + self.player.height/2
            or self.player.x + self.player.height/2 < item.x - self.player.height/2
            or self.player.x - self.player.height/2 > item.x + self.player.height/2)

def create_play_scene():
    return Scene(
        BackgroundLayer(),
        GameLayer())
