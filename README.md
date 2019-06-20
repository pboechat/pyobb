# pyobb

[![Build Status](https://travis-ci.org/pboechat/pyobb.svg?branch=master)](https://travis-ci.org/pboechat/pyobb) [![PyPI version](https://badge.fury.io/py/pyobb.svg)](https://badge.fury.io/py/pyobb)

> OBB implementation in Python (using numpy)

This is basically a port of the code found on [James' Blog](http://jamesgregson.blogspot.com/2011/03/latex-test.html), which in turn is a C++ implementation (using CGAL) of the ideas found in Stefan Gottschalk's [PhD thesis](http://gamma.cs.unc.edu/users/gottschalk/main.pdf).
The central idea of this OBB contruction is to compute a covariance matrix for a point set and then find the eigenvectors of this covariance matrix.

----------

### Installation

Simply run

    pip install pyobb


### Usage

The *pyobb* package contains a single class: *OBB*. An OBB has the following attributes:

* *centroid*: the OBB center
* *min*: the OBB point with the smallest XYZ components in the local frame (i.e., -[width/2, height/2, depth/2])
* *max*: the OBB point with the largest XYZ components in the local frame (i.e., [width/2, height/2, depth/2])
* *points*: the 8 points of the OBB
* *extents*: the extents of the OBB in the XYZ-axis (i.e., the scaled unit vectors of the global frame)
* *rotation*: the rotation matrix of the OBB

You have three different ways to build an OBB: using a covariance matrix, using a point set and using a triangle mesh. Those ways are respectively implemented by the methods:

* *OBB.build_from_covariance_matrix(covariance_matrix, points)*: expects a 3x3 covariance matrix and a set of 3D points
* *OBB.build_from_points(points)*: expects a set of 3D points
* *OBB.build_from_triangles(points, triangles)*: expects a set of 3D points and a flat list of indices refering those points for which every 3-uple would form a triangle

For instance, you can create an OBB from the points of a lat/lon sphere

    from math import pi, cos, sin, sqrt
    from pyobb.obb import OBB
    
    # creates a lat/lon sphere with a given radius and centered at a given point
    def sphere(radius, center, num_slices=30):
        theta_step = 2.0 * pi / (num_slices - 1)
        phi_step = pi / (num_slices - 1.0)
        theta = 0.0
        vertices = []
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
                vertices.append((x * radius + center[0],
                                 y * radius + center[1],
                                 z * radius + center[2]))
                phi += phi_step
            theta += theta_step
        return vertices
    
    obb = OBB.build_from_points(sphere(1, (0, 0, 0)))

Which gives you this OBB:

![](http://www.pedroboechat.com/images/pyobb_0.png)

You can also create an OBB from the vertices and faces of OBJ models

    from pyobb.obb import OBB
    from objloader import OBJ  # source: http://www.pygame.org/wiki/OBJFileLoader
    
    obj = OBJ(filename='bunny.obj')  # stanford bunny
    # obj = OBJ(filename='killeroo.obj')  # killeroo
    indices = []
    for face in obj.faces:
        indices.append(face[0][0] - 1)
        indices.append(face[0][1] - 1)
        indices.append(face[0][2] - 1)
    obb = OBB.build_from_triangles(obj.vertices, indices)

Which gives you something like this:

![](http://www.pedroboechat.com/images/pyobb_1.png)

or this:

![](http://www.pedroboechat.com/images/pyobb_2.png)
