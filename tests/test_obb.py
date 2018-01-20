from pytest import mark
from math import pi, cos, sin, sqrt, radians
from pyobb.obb import OBB

EPSILON = 0.025


def tpl_cmp(a, b, epsilon=EPSILON):
    for aX, bX in zip(a, b):
        if abs(aX - bX) > epsilon:
            return False
    return True


def render_to_png(filename, callback, obb, model_matrix=(1, 0, 0, 0,
                                                         0, 1, 0, 0,
                                                         0, 0, 1, 0,
                                                         0, 0, 0, 1)):
    from pygame import init, display, quit
    from pygame.constants import OPENGL, DOUBLEBUF
    from OpenGL.GL import glLightfv, glCullFace, glEnable, glShadeModel, glMatrixMode, glLoadIdentity, glClear, \
        glLoadMatrixf, glPolygonMode, glCallList, glReadPixels, GL_LIGHT0, GL_POSITION, GL_AMBIENT, GL_DIFFUSE, \
        GL_BACK, GL_LIGHTING, GL_COLOR_MATERIAL, GL_DEPTH_TEST, GL_SMOOTH, GL_PROJECTION, GL_MODELVIEW, \
        GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_FRONT_AND_BACK, GL_FILL, GL_LINE, GL_BGR, GL_UNSIGNED_BYTE
    from OpenGL.GLU import gluPerspective
    from cv2 import imwrite
    from numpy import frombuffer, uint8
    init()
    viewport = (800, 600)
    display.set_mode(viewport, OPENGL | DOUBLEBUF)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, -1, 0, 0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))
    glCullFace(GL_BACK)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width / float(height), 0.1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glLoadMatrixf(model_matrix)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glCallList(callback())
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glCallList(create_obb_gl_list(obb))
    img_data = glReadPixels(0, 0, width, height, GL_BGR, GL_UNSIGNED_BYTE)
    img = frombuffer(img_data, dtype=uint8)
    img = img.reshape((height, width, 3))
    imwrite(filename, img)
    quit()


def create_obb_gl_list(obb):
    from OpenGL.GL import glGenLists, glNewList, glFrontFace, glBegin, glEnd, glEndList, glColor3fv, glVertex3fv, \
        GL_CCW, GL_COMPILE, GL_LINES
    gl_list = glGenLists(1)
    glNewList(gl_list, GL_COMPILE)
    glFrontFace(GL_CCW)
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

    return gl_list


def create_gl_list(shape):
    from OpenGL.GL import glGenLists, glNewList, glFrontFace, glBegin, glEnd, glEndList, glNormal3fv, glVertex3fv, \
        GL_COMPILE, GL_CCW, GL_TRIANGLES
    vertices = shape['vertices']
    normals = shape['normals']
    indices = shape['indices']
    gl_list = glGenLists(1)
    glNewList(gl_list, GL_COMPILE)
    glFrontFace(GL_CCW)
    glBegin(GL_TRIANGLES)
    for idx in indices:
        glNormal3fv(normals[idx])
        glVertex3fv(vertices[idx])
    glEnd()
    glEndList()
    return gl_list


def sphere(radius, center, num_slices):
    theta_step = 2.0 * pi / (num_slices - 1)
    phi_step = pi / (num_slices - 1.0)
    theta = 0.0
    vertices = []
    normals = []
    for i in range(0, num_slices):
        cos_theta = cos(theta)
        sin_theta = sin(theta)
        phi = 0.0
        for j in range(0, num_slices):
            x = -sin(phi) * cos_theta
            y = -cos(phi)
            z = -sin(phi) * sin_theta
            n = sqrt(x * x + y * y + z * z)
            if n < 0.99 or n > 1.01:
                x /= n
                y /= n
                z /= n
            normals.append((x, y, z))
            vertices.append((x * radius + center[0],
                             y * radius + center[1],
                             z * radius + center[2]))
            phi += phi_step
        theta += theta_step
    indices = []
    for i in range(0, num_slices - 1):
        for j in range(0, num_slices - 1):
            base_idx = (i * num_slices + j)
            indices.append(base_idx)
            indices.append(base_idx + num_slices)
            indices.append(base_idx + num_slices + 1)
            indices.append(base_idx)
            indices.append(base_idx + num_slices + 1)
            indices.append(base_idx + 1)

    return {'radius': radius,
            'center': center,
            'num_slices': num_slices,
            'vertices': vertices,
            'normals': normals,
            'indices': indices}


def cube(size, T, R):
    vertices = []
    normals = []
    c1 = cos(radians(R[0]))
    c2 = cos(radians(R[1]))
    c3 = cos(radians(R[2]))
    s1 = sin(radians(R[0]))
    s2 = sin(radians(R[1]))
    s3 = sin(radians(R[2]))
    model = [c2 * c3, -c2 * s3, s2, T[0],
             c1 * s3 + c3 * s1 * s2, c1 * c3 - s1 * s2 * s3, -c2 * s1, T[1],
             s1 * s3 - c1 * c3 * s2, c3 * s1 + c1 * s2 * s3, c1 * c2, T[2]]

    def new_vertex(x, y, z):
        vertices.append((model[0] * x * size + model[1] * y * size + model[2] * z * size + model[3],
                         model[4] * x * size + model[5] * y * size + model[6] * z * size + model[7],
                         model[8] * x * size + model[9] * y * size + model[10] * z * size + model[11]))
        normals.append((x, y, z))

    new_vertex(-1.0, -1.0, -1.0)
    new_vertex(-1.0, -1.0, 1.0)
    new_vertex(-1.0, 1.0, 1.0)
    new_vertex(1.0, 1.0, -1.0)
    new_vertex(-1.0, -1.0, -1.0)
    new_vertex(-1.0, 1.0, -1.0)
    new_vertex(1.0, -1.0, 1.0)
    new_vertex(-1.0, -1.0, -1.0)
    new_vertex(1.0, -1.0, -1.0)
    new_vertex(1.0, 1.0, -1.0)
    new_vertex(1.0, -1.0, -1.0)
    new_vertex(-1.0, -1.0, -1.0)
    new_vertex(-1.0, -1.0, -1.0)
    new_vertex(-1.0, 1.0, 1.0)
    new_vertex(-1.0, 1.0, -1.0)
    new_vertex(1.0, -1.0, 1.0)
    new_vertex(-1.0, -1.0, 1.0)
    new_vertex(-1.0, -1.0, -1.0)
    new_vertex(-1.0, 1.0, 1.0)
    new_vertex(-1.0, -1.0, 1.0)
    new_vertex(1.0, -1.0, 1.0)
    new_vertex(1.0, 1.0, 1.0)
    new_vertex(1.0, -1.0, -1.0)
    new_vertex(1.0, 1.0, -1.0)
    new_vertex(1.0, -1.0, -1.0)
    new_vertex(1.0, 1.0, 1.0)
    new_vertex(1.0, -1.0, 1.0)
    new_vertex(1.0, 1.0, 1.0)
    new_vertex(1.0, 1.0, -1.0)
    new_vertex(-1.0, 1.0, -1.0)
    new_vertex(1.0, 1.0, 1.0)
    new_vertex(-1.0, 1.0, -1.0)
    new_vertex(-1.0, 1.0, 1.0)
    new_vertex(1.0, 1.0, 1.0)
    new_vertex(-1.0, 1.0, 1.0)
    new_vertex(1.0, -1.0, 1.0)

    for i in range(0, len(normals), 3):
        v0 = normals[i]
        v1 = normals[i + 1]
        v2 = normals[i + 2]
        a = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
        b = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
        cross = (a[1] * b[2] - a[2] * b[1],
                 a[2] * b[0] - a[0] * b[2],
                 a[0] * b[1] - a[1] * b[0])
        length = sqrt(cross[0] * cross[0] + cross[1] * cross[1] + cross[2] * cross[2])
        if length > 0:
            normal = (cross[0] / length, cross[1] / length, cross[2] / length)
        else:
            # degenerate normal
            normal = (0, 0, 0)
        normals[i] = normal
        normals[i + 1] = normal
        normals[i + 2] = normal

    return {'size': size,
            'T': T,
            'R': R,
            'vertices': vertices,
            'normals': normals,
            'indices': list(range(0, 36))}


@mark.parametrize('sphere,idx', [(sphere(1, (0, 0, 0), 30), 0),
                                 (sphere(1, (1, 0, 0), 30), 1),
                                 (sphere(1, (-1, 0, 0), 30), 2),
                                 (sphere(1, (0, 1, 0), 30), 3),
                                 (sphere(1, (0, -1, 0), 30), 4),
                                 (sphere(1, (0, 0, 1), 30), 5),
                                 (sphere(1, (0, 0, -1), 30), 6)])
def test_obb_center(sphere, idx):
    obb = OBB.build_from_points(sphere['vertices'])
    # render_to_png('test_obb_center_%d.png' % idx, lambda: create_gl_list(sphere), obb, (1,  0,  0,  0,
    #                                                                                     0,  1,  0,  0,
    #                                                                                     0,  0,  1,  0,
    #                                                                                     0,  0, -5,  1))
    assert tpl_cmp(obb.centroid, sphere['center'])


@mark.parametrize('sphere,idx,extents', [(sphere(1, (0, 0, 0), 30), 0, [1, -1, 1]),
                                         (sphere(1, (1, 0, 0), 30), 1, [1, 1, -1]),
                                         (sphere(1, (-1, 0, 0), 30), 2, [1, 1, -1])])
def test_obb_size(sphere, idx, extents):
    obb = OBB.build_from_points(sphere['vertices'])
    # render_to_png('test_obb_size_%d.png' % idx, lambda: create_gl_list(sphere), obb, (1,  0,  0,  0,
    #                                                                                   0,  1,  0,  0,
    #                                                                                   0,  0,  1,  0,
    #                                                                                   0,  0, -5,  1))
    assert tpl_cmp(obb.extents, extents)

# @mark.parametrize('cube,u,v,w,idx', [(cube(1, (0, 0, 0), (0, 0, 0)), (0, 0, 1), (0, -1, 0), (-1, 0, 0), 0),
#                                      (cube(1, (0, 0, 0), (45, 45, 0)), (0, 0, 1), (0, 1, 0), (-1, 0, 0), 1),
#                                      (cube(1, (0, 0, 0), (-45, -45, 0)), (0, 1, 0), (0, 0, 1), (-1, 0, 0), 2)])
# def test_obb_axis(cube, u, v, w, idx):
#     obb = OBB.build_from_triangles(cube['vertices'], cube['indices'])
#     # render_to_png('test_obb_axis_%d.png' % idx, lambda: create_gl_list(cube), obb, (1,  0,  0,  0,
#     #                                                                                 0,  1,  0,  0,
#     #                                                                                 0,  0,  1,  0,
#     #                                                                                 0,  0, -5,  1))
#     assert tpl_cmp(obb.rotation[0], u)
#     assert tpl_cmp(obb.rotation[1], v)
#     assert tpl_cmp(obb.rotation[2], w)
