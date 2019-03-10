from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer, ColorLayer
from cocos.sprite import Sprite


class Cloud(Sprite):
	SPEED = 50.0

	def __init__(self, x, y, scale):
		super(Cloud, self).__init__(
			"assets/img/cloud.png",
			(x, y),
			scale = scale,
			anchor = (0, 0))
		self.schedule_interval(self.increm_x, 1.0/Cloud.SPEED)

	def increm_x(self, dt):
		if self.x > director.get_window_size()[0]:
			self.x = -self.width
		else:
			self.x += 1


class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()

        # Sky color
        self.add(ColorLayer(187, 239, 255, 255))

        self.add(Cloud(0, 300, 0.65))
        self.add(Cloud(150, 50, 0.5))
        self.add(Cloud(400, 200, 0.3))
