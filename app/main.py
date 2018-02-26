import bottle
import os
import random

# Input: snake coordinates, target coordinates
# Output: move
def goTo(my_x, my_y, target_x, target_y):
    
    move_x = my_x - target_x
    move_y = my_y - target_y

    if (move_y > 0):
        return 'up'
    elif (move_y < 0):
        return 'down'
    elif (move_x > 0):
        return 'left'
    else:
        return 'right'

def nextMove(data):
    
    my_x = data['you']['body']['data'][0]['x']
    my_y = data['you']['body']['data'][0]['y']
    print('My Snake: {0}, {1}'.format(my_x, my_y))

    target_x = data['food']['data'][0]['x']
    target_y = data['food']['data'][0]['y']
    closestDistance = target_x + target_y
    
    #find closest food
    for i in range(len(data['food']['data'])):
        distance_x = abs(my_x - data['food']['data'][i]['x'])
        distance_y = abs(my_y - data['food']['data'][i]['y'])
        distance = distance_x + distance_y
        print('Food: ({0}, {1}) is {2} squares away'.format(target_x, target_y, distance))

        if (distance < closestDistance):
            closestDistance = distance
            target_x = distance_x
            target_y = distance_y
    
    print('Closest Food: ({0}, {1}) is {2} squares away'.format(target_x, target_y, distance))

    return goTo(my_x, my_y, target_x, target_y)


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#FF9333',
        'taunt': 'What a fish!',
        'head_url': head_url,
        'name': 'Big Asp',
        'head_type': 'tongue',
        'tail_type': 'curled'
    }


@bottle.post('/move')
def move():
    print('Calculating Move')
    data = bottle.request.json

    # TODO: Do things with data
    move = nextMove(data)
    print(move)
    directions = ['up', 'down', 'left', 'right']

    return {
        'move': move,
        'taunt': 'You Fish!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
