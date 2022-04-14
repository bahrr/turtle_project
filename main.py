#! usr/bin/python
import turtle
from OpenGL.GL import *
import glm

# Set up screen
screen = turtle.Screen()
screen.screensize(canvwidth=640, canvheight=480, bg='black')
draw = turtle.Turtle()
draw.hideturtle()
draw.color('white')
draw.pensize(3)
draw.speed(0)
turtle.tracer(0, 0)

# cube
class Cube():
    # points of the cube
    vertices = [
        (-1, -1, -1),
        (-1, -1, 1),
        (-1, 1, -1),
        (-1, 1, 1),
        (1, 1, -1),
        (1, 1, 1),
        (1, -1, -1),
        (1, -1, 1),
    ]
    # surfaces
    surfaces = [
        (0, 2, 4, 6),
        (1, 3, 5, 7),
        (0, 1, 3, 2),
        (2, 3, 5, 4),
        (4, 5, 7, 6),
        (6, 7, 1, 0),
    ]
    
    # direction of each surface
    normals = [
        (0, 0, -1),
        (0, 0, 1),
        (-1, 0, 0),
        (0, 1, 0),
        (1, 0, 0),
        (0, -1, 0),
    ] 

    # colors of each surface
    colors = [
        'red',
        'green',
        'blue',
        'yellow',
        'cyan',
        'magenta',
    ]

# just the perspective to handle things like the FOV
PERSPECTIVE = glm.perspective(glm.radians(90), 1, 1, 50)

# area for bouncing off of
PHYSICS_BOX = (640, 480)

# moves the cube aroun
def move_objects():
    global position
    global movedir
    global rotate

    # checks for collision between model and screen
    position = [(position[0] + movedir[0]), (position[1] + movedir[1]), position[2]]
    if abs(position[0]) >= PHYSICS_BOX[0] // 2:
        movedir[0] *= -1 
    elif abs(position[1]) >= PHYSICS_BOX[1] // 2:
        movedir[1] *= -1 
    else:
        rotate += 0.01
    

# calculates where each vertex will be in screenspace
def calculate_models():
    global points
    global normalpoints
    global rotate

    points = []
    normalpoints = []
    # deals with where to put each vector
    for vertex in model.vertices:

            # scales up and moves the object
            vector_vertex = glm.vec4(vertex, 1)
            scale_matrix = glm.scale((50, 50, 50))
            translate_matrix = glm.translate((position))
            rotation_matrix = glm.rotate(rotate, (1, 1, 1))
            model_matrix = translate_matrix * rotation_matrix * scale_matrix

            # moves camera around
            camera_pos_matrix = glm.translate((0, 0, 0))
            camera_look_matrix = glm.lookAt((0, 0, 0), (0, 0, -1),  (0, 1, 0))
            view_matrix = camera_look_matrix * camera_pos_matrix

            # adjusts camera space to screen space
            mvp_matrix = PERSPECTIVE * view_matrix * model_matrix
            points.append(mvp_matrix * vector_vertex)
    
    # calculates where each normal points
    for normal in model.normals:
            vector_normal = glm.vec4(normal, 0)
            rotation_matrix = glm.rotate(rotate, (1, 1, 1))
            normalpoints.append(rotation_matrix * vector_normal)


# to handle the actual drawing
def draw_models(model, points, normals):
    # an iterator is needed for this type of stuff
    i = 0
    for surface in model.surfaces:
        normal = normals[i]            
        
        # primitive backface culling so that we cant see the faces behind other faces
        if normal.z <= 0:
            i += 1
            continue
        draw.penup()

        # coords of the first point in the polygon as it requires a certain order to draw correctly
        fpx = points[surface[0]].x
        fpy = points[surface[0]].y
        draw.goto(fpx, fpy)
        draw.fillcolor(model.colors[i])
        draw.begin_fill()

        # basically just goes to the x and y of the array 
        for vertex in surface:
            vert_x = points[vertex].x
            vert_y = points[vertex].y
            draw.pendown()
            draw.goto(vert_x, vert_y)
        draw.end_fill()
        draw.goto(fpx, fpy)
        i += 1


# setup of the object itself
model = Cube()
rotate = 0
position = [0, 0, 0]
movedir = [1, 1]

def main():
    # few global declarations to get out of the way
    global points
    global normalpoints
    global rotate
    global position
    global movedir

    # clear buffers
    draw.clear()

    # callse each function
    move_objects()
    calculate_models()
    draw_models(model, points, normalpoints)
    turtle.update()

    # make exiting work via recursion
    screen.ontimer(main, (1000 // 60))

# loops
main()
screen.mainloop()