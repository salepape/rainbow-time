from cocos.director import director


TRACKS_PROPORTION = 0.5


def coor_track_width():
    return int(director.get_window_size()[0] * TRACKS_PROPORTION / 5.0)


def coor_to_real(i, j):
    w, h = director.get_window_size()
    x0 = w * (1.0 - TRACKS_PROPORTION) / 2.0
    x = x0 + i * coor_track_width()
    y = j * h
    return int(x), int(y)
