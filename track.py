from cocos.director import director
from cocos.layer import ColorLayer
from cocos.actions.interval_actions import MoveTo
from coor import coor_to_real, coor_track_width


track_colors = [
    (255, 48, 32),
    (255, 166, 0),
    (190, 255, 40),
    (99, 155, 255),
    (187, 88, 150),
]


class Track(ColorLayer):
    is_event_handler = True

    def __init__(self, index):
        super(Track, self).__init__(
            track_colors[index][0],
            track_colors[index][1],
            track_colors[index][2],
            190)

        self.i = index
        self.j = 0.0

        w, h = director.get_window_size()
        self.on_resize(w, h)

    def on_resize(self, w, h):
        self.position = coor_to_real(self.i, self.j)
        self.width = coor_track_width()

    def moveTo(self, i, j):
        self.i = i
        self.j = j
        self.do(MoveTo(coor_to_real(i, j), 0.1))
