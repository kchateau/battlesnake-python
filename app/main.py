import bottle
import os
import random
import json



@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    global height
    global width

    height = board_height
    width = board_width

    head_url = '%s://%s/static/xan.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'Kendra Awesomer Snake'
    }



@bottle.post('/move')
def move():
    data = bottle.request.json
    ls = []

    directions = ['up', 'down', 'left', 'right']
    snakes = data['snakes']

    for y in snakes:
        if y['id'] == data['you']:
            me = y
            #snakes.remove(y)

    head = me['coords'][0]
    headx = head[0]
    heady = head[1]

    neck = me['coords'][1]
    neckx = neck[0]
    necky = neck[1]

    if headx == neckx+1:
        directions.remove('left')
    if headx == neckx-1:
        directions.remove('right')
    if heady == necky+1:
        directions.remove('up')
    if heady == necky-1:
        directions.remove('down')

    if headx == width-1:
        directions.remove('right')
    if headx == 0:
        directions.remove('left')
    if heady == height-1:
        directions.remove('down')
    if heady == 0:
        directions.remove('up')

    directions = donthitothers(snakes, me, directions)

    foodlist = data['food']
    legalmove = getfood(me, foodlist)

    if legalmove in directions:
        move = legalmove
    else:
        move = random.choice(directions)

    return {
        'move': move,
        'taunt': me['name']
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))



def donthitothers(othersnakes, me, dir):
    head = me['coords'][0]
    headx = head[0]
    heady = head[1]
    snakes = []

    for x in othersnakes:
        snakes.append(x['coords'])

    i = 0
    for x in snakes:
        j = 0
        for y in snakes[i]:
            try:
                if snakes[i][j][0] == headx-1:
                    dir.remove('left')
                if snakes[i][j][0] == headx+1:
                    dir.remove('right')
                if snakes[i][j][1] == heady-1:
                    dir.remove('up')
                if snakes[i][j][1] == heady+1:
                    dir.remove('down')
            except ValueError:
                pass
        i = i+1

    return dir

def getfood(me, foodlist):
    head = me['coords'][0]
    headx = head[0]
    heady = head[1]

    closestfood = foodlist[0]
    if len(foodlist) > 1:
        for x in foodlist:
            dist = abs(headx - x[0]) + abs(heady - x[1])
            if dist < abs(headx - closestfood[0]) + abs(heady - closestfood[1]):
                closestfood = x

    if headx - closestfood[0] >= 0 and heady - closestfood[1] >= 0:
        if abs(headx - closestfood[0]) >= abs(heady - closestfood[1]):
            return 'left'
        if abs(headx - closestfood[0]) <= abs(heady - closestfood[1]):
            return 'up'
        else:
            return 'left'

    if headx - closestfood[0] <= 0 and heady - closestfood[1] >= 0:
        if abs(headx - closestfood[0]) >= abs(heady - closestfood[1]):
            return 'up'
        if abs(headx - closestfood[0]) <= abs(heady - closestfood[1]):
            return 'right'
        else:
            return 'up'

    if headx - closestfood[0] <= 0 and heady - closestfood[1] <= 0:
        if abs(headx - closestfood[0]) >= abs(heady - closestfood[1]):
            return 'right'
        if abs(headx - closestfood[0]) <= abs(heady - closestfood[1]):
            return 'down'
        else:
            return 'right'

    if headx - closestfood[0] >= 0 and heady - closestfood[1] <= 0:
        if abs(headx - closestfood[0]) >= abs(heady - closestfood[1]):
            return 'left'
        if abs(headx - closestfood[0]) <= abs(heady - closestfood[1]):
            return 'down'
        else:
            return 'left'