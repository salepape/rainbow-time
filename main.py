from cocos.director import director
from cocos.scene import Scene
from intro_scene import create_intro_scene
from menu_scene import create_menu_scene
from time import sleep


def main():
    director.init(resizable=True, caption="Rainbow Time !")
    director.run(create_menu_scene())


if __name__ == "__main__":
    main()
