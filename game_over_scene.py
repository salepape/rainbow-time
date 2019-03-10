from cocos.scene import Scene
from cocos.layer import Layer
from cocos.director import director
from cocos.menu import Menu, MenuItem, CENTER
import menu_scene
import play_scene


class GameOverMenu(Menu):

    def __init__(self):
        super(GameOverMenu, self).__init__()

        self.y = -0.2 * director.get_window_size()[1]
        self.menu_halign = CENTER

        self.create_menu([
            MenuItem('PLAY AGAIN', self.on_play_again),
            MenuItem('BACK TO MENU', self.on_back_to_menu)
        ])

    def on_play_again(self):
        director.replace(play_scene.create_play_scene())

    def on_back_to_menu(self):
        director.replace(menu_scene.create_menu_scene())


class GameOverLayer(Layer):
    def __init__(self):
        super(GameOverLayer, self).__init__()

        self.add(GameOverMenu())


def create_game_over_scene():
    return Scene(
        menu_scene.BackgroundLayer(),
        GameOverLayer())
