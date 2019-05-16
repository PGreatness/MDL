import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print(symbols)
    for command in commands:
        print(command)
        op = command['op']
        args = command['args']
        if op == 'push':
            stack.append([ x[:] for x in stack[-1] ])
        if op == 'pop':
            stack.pop()
        if op == 'move':
            translate = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], translate)
            stack[-1] = [ x[:] for x in translate ]
        if op == 'rotate':
            theta = args[1] * math.pi/180
            if args[0] == 'x':
                rotate = make_rotX(theta)
            elif args[0] == 'y':
                rotate = make_rotY(theta)
            elif args[0] == 'z':
                rotate = make_rotZ(theta)
            matrix_mult(stack[-1], rotate)
            stack[-1] = [ x[:] for x in rotate ]
        if op == 'scale':
            scale = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], scale)
            stack[-1] = [ x[:] for x in scale ]
        if op == 'box':
            add_box(tmp, args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult(stack[-1], tmp)
            c = '.white' if not command['constants'] else command['constants']
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, c)
            tmp = []
        if op == 'torus':
            add_torus(tmp, args[0], args[1], args[2], args[3], args[4], step_3d)
            matrix_mult(stack[-1], tmp)
            c = '.white' if not command['constants'] else command['constants']
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, c)
            tmp = []
        if op == 'sphere':
            add_sphere(tmp, args[0], args[1], args[2], args[3], step_3d)
            matrix_mult(stack[-1], tmp)
            c = '.white' if not command['constants'] else command['constants']
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, c)
            tmp = []
        elif op == 'line':
            add_edge(tmp, args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult(stack[-1], tmp)
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        elif op == 'display' or op == 'save':
            if op == 'display':
                display(screen)
            else:
                save_extension(screen, args[0] + '.png')
