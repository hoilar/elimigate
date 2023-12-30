# Dictorionary of constants used in the game

profiles = {
    "adventurer": {"tooltip": "Velocipede when in play gives xxx. \nLantern when in hand gives xxx.", "handitem": "lantern", "playitem": "bicycle"},
    "agent": {"tooltip": "Pocket-watch when in play gives xxx. \nMagnifying glass when in hand gives xxx.", "handitem": "magnifyingglass", "playitem": "watch"},
    "archeolog": {"tooltip": "Wheelbarrow when in play gives xxx. \nMagnifying glass when in hand gives xxx.", "handitem": "magnifyingglass", "playitem": "wheelbarrow"},
    "barber": {"tooltip": "Dagger play: +1 random witness, -1 AP next day. \nGoggles when in hand gives xxx.", "handitem": "goggles", "playitem": "dagger"},
    "barkeeper": {"tooltip": "Teapot play: full hand, -1 random witness. \nTophat when in hand gives xxx.", "handitem": "tophat", "playitem": "teapot"},
    "butcher": {"tooltip": "Dagger play: +1 random witness, -1 AP next day. \nPipe when in hand gives xxx.", "handitem": "pipe", "playitem": "dagger"},
    "coalworker": {"tooltip": "Wheelbarrow when in play gives xxx. \nGoggles when in hand gives xxx.", "handitem": "goggles", "playitem": "wheelbarrow"},
    "curator": {"tooltip": "Tophat play: +1 random witness, -1 day. \nWheelbarrow when in hand gives xxx.", "handitem": "wheelbarrow", "playitem": "tophat"},
    "detective": {"tooltip": "Pipe when in play gives xxx. \nWhistle when in hand gives xxx.", "handitem": "whistle", "playitem": "pipe"},
    "doctor": {"tooltip": "Goggles when in play gives xxx. \nVelocipede when in hand gives xxx.", "handitem": "bicycle", "playitem": "goggles"},
    "fisherman": {"tooltip": "Lantern when in play gives xxx. \nDagger when in hand gives xxx.", "handitem": "dagger", "playitem": "lantern"},
    "hobo": {"tooltip": "Pipe when in play gives xxx. \nBaton when in hand gives xxx.", "handitem": "baton", "playitem": "pipe"},
    "housewife": {"tooltip": "Teapot play: full hand, -1 random witness. \nWhistle when in hand gives xxx.", "handitem": "whistle", "playitem": "teapot"},
    "hunter": {"tooltip": "Dagger play: +1 random witness, -1 AP next day. \nLantern when in hand gives xxx.", "handitem": "lantern", "playitem": "dagger"},
    "inventor": {"tooltip": "Magnifying glass when in play gives xxx. \nGoggles when in hand gives xxx.", "handitem": "goggles", "playitem": "magnifyingglass"},
    "magician": {"tooltip": "Pocket-watch when in play gives xxx. \nLantern when in hand gives xxx.", "handitem": "lantern", "playitem": "watch"},
    "maid": {"tooltip": "Whistle when in play gives xxx. \nTeapot when in hand gives xxx.", "handitem": "teapot", "playitem": "whistle"},
    "mayor": {"tooltip": "Tophat play: +1 random witness, -1 day. \nTeapot when in hand gives xxx.", "handitem": "teapot", "playitem": "tophat"},
    "pi": {"tooltip": "Magnifying glass when in play gives xxx. \nBaton when in hand gives xxx.", "handitem": "baton", "playitem": "magnifyingglass"},
    "policeman": {"tooltip": "Baton when in play gives xxx. \nWhistle when in hand gives xxx.", "handitem": "whistle", "playitem": "baton"},
    "postman": {"tooltip": "Lantern when in play gives xxx. \nVelocipede when in hand gives xxx.", "handitem": "bicycle", "playitem": "lantern"},
    "professor": {"tooltip":"Pocket-watch when in play gives xxx. \nTophat when in hand gives xxx.", "handitem": "tophat", "playitem": "watch"},
    "scientist": {"tooltip": "Goggles when in play gives xxx.  \nPocket-watch when in hand gives xxx.", "handitem": "watch", "playitem": "goggles"},
    "vodouisant": {"tooltip": "Dagger play: +1 random witness, -1 AP next day. \nPocket-watch when in hand gives xxx.", "handitem": "watch", "playitem": "dagger"},
}

player_items = {
    "baton": {"tooltip": "Match Baton, 1+AP", "type": "item"},
    "bicycle": {"tooltip": "Match Velocipede, 1+AP", "type": "item"},
    "dagger": {"tooltip": "Match Dagger, 1+AP", "type": "item"},
    "goggles": {"tooltip": "Match Goggles, 1+AP", "type": "item"},
    "lantern": {"tooltip": "Match Lantern, 1+AP", "type": "item"},
    "magnifyingglass": {"tooltip": "Match Mag.glass, 1+AP", "type": "item"},    
    "pipe": {"tooltip": "Match Pipe, 1+AP", "type": "item"},
    "teapot": {"tooltip": "Match Teapot, 1+AP", "type": "item"},
    "tophat": {"tooltip": "Match Tophat, 1+AP", "type": "item"},    
    "watch": {"tooltip": "Match Pocket-watch, 1+AP", "type": "item"},
    "wheelbarrow": {"tooltip": "Match Wheeelbarrow, 1+AP", "type": "item"}, 
    "whistle": {"tooltip": "Match Whistle, 1+AP", "type": "item"},
    "cab": {"tooltip": "S", "type": "special"},
    "cell": {"tooltip": "S", "type": "special"},
    "duster": {"tooltip": "S", "type": "special"},
    "fist": {"tooltip": "S", "type": "special"},
    "gun": {"tooltip": "S", "type": "special"},
    "hat": {"tooltip": "S", "type": "special"},
    "mail": {"tooltip": "S", "type": "special"},
    "newspaper": {"tooltip": "S", "type": "special"},
    "note": {"tooltip": "S", "type": "special"},
    "poster": {"tooltip": "S", "type": "special"},
    "safe": {"tooltip": "S", "type": "special"},
    "telegram": {"tooltip": "S", "type": "special"},
    "whiskey": {"tooltip": "Play-actions are now hand-actions", "type": "special"},
}

enemy_items = {
    "bag": {"tooltip": "X", "type": "enemyitem"},
    "bribe": {"tooltip": "X", "type": "enemyitem"},
    "cipher": {"tooltip": "X", "type": "enemyitem"},
    "gloves": {"tooltip": "X", "type": "enemyitem"},
    "ladder": {"tooltip": "X", "type": "enemyitem"},
    "lockpick": {"tooltip": "X", "type": "enemyitem"},
    "mask": {"tooltip": "X", "type": "enemyitem"},
    "shovel": {"tooltip": "X", "type": "enemyitem"}
}

# Delt cards images update on mouse-hover 
card_images_d = {f"{name}_delt.png": f"images/profiles/{name}_delt.png" for name in profiles.keys()}
card_images_d.update({f"{name}_delt_hov.png": f"images/profiles/{name}_delt_hov.png" for name in profiles.keys()})
card_images_d.update({f"{name}_delt.png": f"images/profiles/{name}_delt.png" for name in profiles.keys()})

# Waiting room cards images update on mouse-hover 
card_images_h = {f"{name}_hand.png": f"images/profiles/{name}_hand.png" for name in profiles.keys()}
card_images_h.update({f"{name}_hand_hov.png": f"images/profiles/{name}_hand_hov.png" for name in profiles.keys()})
card_images_h.update({f"{name}_hand.png": f"images/profiles/{name}_hand.png" for name in profiles.keys()})

# Examination cards images update on mouse-hover 
card_images_p = {f"{name}_play.png": f"images/profiles/{name}_play.png" for name in profiles.keys()}
card_images_p.update({f"{name}_play_hov.png": f"images/profiles/{name}_play_hov.png" for name in profiles.keys()})
card_images_p.update({f"{name}_play.png": f"images/profiles/{name}_play.png" for name in profiles.keys()})

# Witness images
card_images_w = {f"{name}_wit.png": f"images/profiles/{name}_wit.png" for name in profiles.keys()}

# Enemy images
card_images_e = {f"e_{name}.png": f"images/profiles/e_{name}" for name in enemy_items.keys()}

# Items cards images update on mouse-hover 
card_images_i = {f"{name}.png": f"images/items/{name}.png" for name in player_items.keys()}
card_images_i.update({f"{name}_hov.png": f"images/items/{name}_hov.png" for name in player_items.keys()})
card_images_i.update({f"{name}.png": f"images/items/{name}.png" for name in player_items.keys()})
