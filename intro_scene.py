from cocos.director import director
from cocos.scene import Scene
from cocos.scenes import TransitionScene
from cocos.layer import Layer, ColorLayer
from menu_scene import create_menu_scene


class IntroLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super(IntroLayer, self).__init__()

        self.add(ColorLayer(0, 255, 0, 255))

    def on_key_press(self, key, modifiers):
        director.replace(create_menu_scene())


def create_intro_scene():
    return Scene(
	    ColorLayer(0, 255, 0, 255),
		IntroLayer())
