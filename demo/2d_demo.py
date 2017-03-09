from sys import exit
from pygame import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pyobb.obb import OBB


########################################################################################################################
# copied from: http://www.pygame.org/wiki/OBJFileLoader
########################################################################################################################
if __name__ == '__main__':
    init()
    viewport = (800, 600)
    surface = display.set_mode(viewport, OPENGL | DOUBLEBUF)
    display.set_caption('pyobb 2D demo')

    clock = time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluOrtho2D(0, width, 0, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    points = []
    render_gl_lists = False
    while 1:
        clock.tick(30)
        for e in event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    exit()
                elif e.key == K_RETURN:
                    poly_gl_list = glGenLists(1)
                    glNewList(poly_gl_list, GL_COMPILE)
                    glColor3fv((0, 0, 1))
                    glBegin(GL_POLYGON)
                    for point in points:
                        glVertex2fv(point)
                    glEnd()
                    glEndList()

                    obb = OBB()
                    obb.build_from_points([(point[0], point[1], 0) for point in points])

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
                    render_gl_lists = True
                elif e.key == K_BACKSPACE:
                    points = []
                    render_gl_lists = False
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    point = mouse.get_pos()
                    points.append((point[0], height - point[1]))
                elif e.button == 2:
                    points = points[:-1]

        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        if render_gl_lists:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glCallList(poly_gl_list)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glCallList(obb_gl_list)
        glPointSize(6.0)
        glColor3fv((0, 1, 0))
        glBegin(GL_POINTS)
        for point in points:
            glVertex2fv(point)
        glEnd()

        display.flip()
