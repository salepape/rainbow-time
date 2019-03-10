from cocos.director import director
from cocos.scene import Scene
from cocos.layer import MultiplexLayer, ColorLayer
from cocos.menu import Menu, MenuItem, CENTER
import play_scene
from background import BackgroundLayer
from cocos.sprite import Sprite
from cocos.layer import Layer


class TitleLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super(TitleLayer, self).__init__()

        self.add(Sprite(
            "assets/img/title.png",
            (75, 350),
            scale = 0.4,
            anchor = (0, 0)))


class MainMenu(Menu):

    def __init__(self):
        super(MainMenu, self).__init__()

        self.y = -0.2 * director.get_window_size()[1]
        self.menu_halign = CENTER

        self.create_menu([
            MenuItem('PLAY', self.on_play),
            MenuItem('OPTIONS', self.on_options),
            MenuItem('QUIT', self.on_quit)
        ])

    def on_play(self):
        director.replace(play_scene.create_play_scene())

    def on_options(self):
        global ml
        ml.switch_to(1)

    def on_quit(self):
        # TODO
        exit()


class OptionsMenu(Menu):

    is_event_handler = True

    def __init__(self):
        super(OptionsMenu, self).__init__()

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        self.create_menu([
            MenuItem('BACK', self.on_back)
        ])

    def on_back(self):
        global ml
        ml.switch_to(0)


def create_menu_scene():
    global ml
    ml = MultiplexLayer(MainMenu(), OptionsMenu())

    return Scene(
	    BackgroundLayer(),
        TitleLayer(),
        ml)
