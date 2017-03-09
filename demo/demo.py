from os import chdir
from sys import exit
from pygame import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import OBJ
chdir('..')
from pyobb.obb import OBB


########################################################################################################################
# copied from: http://www.pygame.org/wiki/OBJFileLoader
########################################################################################################################
if __name__ == '__main__':
    init()
    viewport = (800, 600)
    srf = display.set_mode(viewport, OPENGL | DOUBLEBUF)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, -1, 0, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    obj = OBJ(filename='demo/killeroo.obj')
    obb = OBB()
    indices = []
    for face in obj.faces:
        indices.append(face[0][0] - 1)
        indices.append(face[0][1] - 1)
        indices.append(face[0][2] - 1)
    obb.build_from_triangles(obj.vertices, indices)

    obb_gl_list = glGenLists(1)
    glNewList(obb_gl_list, GL_COMPILE)
    glBegin(GL_LINES)
    glColor3fv((1, 0, 0))

    def input_vertex(x, y, z):
        glVertex3fv((obb.rotation[0][0] * x + obb.rotation[0][1] * y + obb.rotation[0][2] * z,
                     obb.rotation[1][0] * x + obb.rotation[1][1] * y + obb.rotation[1][2] * z,
                     obb.rotation[2][0] * x + obb.rotation[2][1] * y + obb.rotation[2][2] * z))

    input_vertex(*obb.max)
    input_vertex(obb.max[0], obb.min[1], obb.max[2])

    input_vertex(obb.max[0], obb.min[1], obb.max[2])
    input_vertex(obb.min[0], obb.min[1], obb.max[2])

    input_vertex(obb.min[0], obb.min[1], obb.max[2])
    input_vertex(obb.min[0], obb.max[1], obb.max[2])

    input_vertex(obb.min[0], obb.max[1], obb.max[2])
    input_vertex(*obb.max)

    input_vertex(obb.max[0], obb.max[1], obb.max[2])
    input_vertex(obb.max[0], obb.max[1], obb.min[2])

    input_vertex(obb.max[0], obb.min[1], obb.max[2])
    input_vertex(obb.max[0], obb.min[1], obb.min[2])

    input_vertex(obb.min[0], obb.max[1], obb.max[2])
    input_vertex(obb.min[0], obb.max[1], obb.min[2])

    input_vertex(obb.min[0], obb.min[1], obb.max[2])
    input_vertex(obb.min[0], obb.min[1], obb.min[2])

    input_vertex(obb.max[0], obb.max[1], obb.min[2])
    input_vertex(obb.max[0], obb.min[1], obb.min[2])

    input_vertex(obb.max[0], obb.min[1], obb.min[2])
    input_vertex(*obb.min)

    input_vertex(*obb.min)
    input_vertex(obb.min[0], obb.max[1], obb.min[2])

    input_vertex(obb.min[0], obb.max[1], obb.min[2])
    input_vertex(obb.max[0], obb.max[1], obb.min[2])
    glEnd()
    glEndList()

    clock = time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width / float(height), 0.1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    rotation = [0, 0]
    translation = [-obb.position[0], -obb.position[1], -(obb.position[2] + obb.extents[2] * 2)]
    rotate = move = False
    while 1:
        clock.tick(30)
        for e in event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4:
                    translation[2] += 0.1
                elif e.button == 5:
                    translation[2] -= 0.1
                elif e.button == 1:
                    rotate = True
                elif e.button == 2:
                    move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    rotate = False
                elif e.button == 2:
                    move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rotation[1] += i
                    rotation[0] += j
                if move:
                    translation[0] += i * .025
                    translation[1] -= j * .025

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslate(translation[0], translation[1], translation[2])
        glRotate(rotation[0], 1, 0, 0)
        glRotate(rotation[1], 0, 1, 0)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glCallList(obj.gl_list)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glCallList(obb_gl_list)

        display.flip()
