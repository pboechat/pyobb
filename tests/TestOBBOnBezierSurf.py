"""
from Beams.BeamElements import KirchhoffBeam, TimoshenkoBeam, TimoshenkoBeam3D
from Beams.GeometricallyExact import SR3DBeams
from Common import BoundaryConditions, Solver, FEM
from Common.FEM import Model
from Common.Utilities import nel_from_nn
import numpy as np
from numpy import zeros, ones_like,  zeros_like, asarray, array, ones, ix_, allclose, arange
from numpy.linalg import norm, solve
from pdb import set_trace
import matplotlib.pylab as plt
from mayavi import mlab
from pdb import set_trace
from pyobb.obb import OBB


E = 100.
# we will get a circular cross section of radius = 0.5
b = array([0.6, 0.6])
h = array([0.2, 0.2])
try:
    mlab.close()
except AttributeError:
    pass

plt.close('all')

# Y1 beam suppose to represent a rigid obstacle
nnY1 = 5
XY1 = zeros((nnY1, 3), dtype = float)
XY1[:,1] = 0.501 * (b[0] + b[1])
XY1[:,2] = np.linspace( -2, 2, nnY1)
nel_Y1 = nel_from_nn(2, nnY1)
nIDs_Y1 = zeros((nel_Y1,2), dtype = int)
nIDs_Y1[:,0] = np.arange(nnY1 -1)
nIDs_Y1[:,1] = np.arange(1, nnY1)
el_Y1 = np.arange(nel_Y1)

nnY2 = 20
XY2 = zeros((nnY2, 3), dtype = float)
XY2[:,0] = np.linspace(-4, 4, nnY2)
nel_Y2 = nel_from_nn(2, nnY2)
nIDs_Y2 = zeros((nel_Y2,2), dtype = int)
nIDs_Y2[:,0] = nnY1 + np.arange(nnY2-1)
nIDs_Y2[:,1] = nnY1 + np.arange(1, nnY2)
el_Y2= nel_Y1 + np.arange(nel_Y2)


# 6 dofs per node
ndofsPern = 6
nN = nnY1 + nnY2
nEl = nel_Y1 + nel_Y2
# we just set the x coordinates
X = np.vstack((XY1, XY2))
# dofs per node
dperN = np.arange(ndofsPern * nN).reshape(-1, ndofsPern)
# Construct beam elements
el = np.zeros(nEl, dtype = np.object)
nIDs = np.vstack((nIDs_Y1, nIDs_Y2))

for ii in range(nEl):
    nIDsi = array(nIDs[ii] )
    t3 =  X[nIDsi][1] - X[nIDsi][0]
    t3 /= norm(t3)

    if ii in range(nel_Y1):
        bii = b[0]
        hii = h[0]
        t1 = array([1,0,0])
        t2 = np.cross(t3, t1)
    else:
        bii = b[1]
        hii = h[1]
        t1 = array([0,0,-1])
        t2 = np.cross(t3, t1)

    el[ii] = SR3DBeams( X = X[nIDsi], E = E,
                        nu = 0.3, b = bii, h = hii,
                        nID = nIDsi, dofs = dperN[nIDsi],
                        E1= t1,E2 = t2,
                        rot_vars_storage= 1,
                        shapeCrossSec='Elliptical')

# Construct FE assembly
# 3 rotations and translations per node
BeamMod = Model(el, X.shape[0], ndofsPern, X,\
                HasConstraints = 1,\
                dperN = dperN)

BeamMod.set_plotting_package('mayavi')

# the first elements are the one associated with the Y1 yarn !
el_curves_YY1 = np.vstack((np.arange(nel_Y1)[:-1],
    np.arange(nel_Y1)[1:])).T
el_curves_YY2 = nel_Y1 + np.vstack((np.arange(nel_Y2)[:-1],
    np.arange(nel_Y2)[1:])).T
elements_per_curve = np.concatenate((el_curves_YY1,
    el_curves_YY2))

# Be extremely careful when setting which curves are master and which
# ones are slaves. Be careful not to mix the element per curves

ID_master_curves = np.arange( el_curves_YY1.shape[0])
ID_slave_curves = ID_master_curves[-1] + 1 +  np.arange( el_curves_YY2.shape[0])

BeamMod.create_unset_Contact_Table(\
            enforcement = 1,\
            method = 'curve_to_curve',\
            isConstant = False,\
            alpha = 0.9,\
            smooth_cross_section_vectors = True,\
            elements_per_curve = elements_per_curve,
            master_curves_ids= ID_master_curves,
            slave_curves_ids= ID_slave_curves,\
            nintegrationIntervals = array([1,2]),\
            nxiGQP = 8,\
            nthetaGQP = 8)

BeamMod.ContactTable.set_default_value_LM(0)


# sample points on a curve
Pts =\
    BeamMod.sample_surf_point_on_smooth_geo(\
                            BeamMod.el_per_curves[1],\
                            10,\
                            10 ,\
                            array([0,1]),\
                            array([0, 2 * np.pi])).reshape(-1,3)
"""
import numpy as np
from numpy import array
from mayavi import mlab
from pyobb.obb import OBB
try:
    mlab.close()
except AttributeError:
    pass
Pts =\
array([[ 0.3       ,  0.6012    , -0.5       ],
       [ 0.22981333,  0.66547876, -0.5       ],
       [ 0.05209445,  0.69968078, -0.5       ],
       [-0.15      ,  0.68780254, -0.5       ],
       [-0.28190779,  0.63540201, -0.5       ],
       [-0.28190779,  0.56699799, -0.5       ],
       [-0.15      ,  0.51459746, -0.5       ],
       [ 0.05209445,  0.50271922, -0.5       ],
       [ 0.22981333,  0.53692124, -0.5       ],
       [ 0.3       ,  0.6012    , -0.5       ],
       [ 0.3       ,  0.6012    , -0.36200274],
       [ 0.22981333,  0.66547876, -0.36200274],
       [ 0.05209445,  0.69968078, -0.36200274],
       [-0.15      ,  0.68780254, -0.36200274],
       [-0.28190779,  0.63540201, -0.36200274],
       [-0.28190779,  0.56699799, -0.36200274],
       [-0.15      ,  0.51459746, -0.36200274],
       [ 0.05209445,  0.50271922, -0.36200274],
       [ 0.22981333,  0.53692124, -0.36200274],
       [ 0.3       ,  0.6012    , -0.36200274],
       [ 0.3       ,  0.6012    , -0.2441701 ],
       [ 0.22981333,  0.66547876, -0.2441701 ],
       [ 0.05209445,  0.69968078, -0.2441701 ],
       [-0.15      ,  0.68780254, -0.2441701 ],
       [-0.28190779,  0.63540201, -0.2441701 ],
       [-0.28190779,  0.56699799, -0.2441701 ],
       [-0.15      ,  0.51459746, -0.2441701 ],
       [ 0.05209445,  0.50271922, -0.2441701 ],
       [ 0.22981333,  0.53692124, -0.2441701 ],
       [ 0.3       ,  0.6012    , -0.2441701 ],
       [ 0.3       ,  0.6012    , -0.14074074],
       [ 0.22981333,  0.66547876, -0.14074074],
       [ 0.05209445,  0.69968078, -0.14074074],
       [-0.15      ,  0.68780254, -0.14074074],
       [-0.28190779,  0.63540201, -0.14074074],
       [-0.28190779,  0.56699799, -0.14074074],
       [-0.15      ,  0.51459746, -0.14074074],
       [ 0.05209445,  0.50271922, -0.14074074],
       [ 0.22981333,  0.53692124, -0.14074074],
       [ 0.3       ,  0.6012    , -0.14074074],
       [ 0.3       ,  0.6012    , -0.04595336],
       [ 0.22981333,  0.66547876, -0.04595336],
       [ 0.05209445,  0.69968078, -0.04595336],
       [-0.15      ,  0.68780254, -0.04595336],
       [-0.28190779,  0.63540201, -0.04595336],
       [-0.28190779,  0.56699799, -0.04595336],
       [-0.15      ,  0.51459746, -0.04595336],
       [ 0.05209445,  0.50271922, -0.04595336],
       [ 0.22981333,  0.53692124, -0.04595336],
       [ 0.3       ,  0.6012    , -0.04595336],
       [ 0.3       ,  0.6012    ,  0.04595336],
       [ 0.22981333,  0.66547876,  0.04595336],
       [ 0.05209445,  0.69968078,  0.04595336],
       [-0.15      ,  0.68780254,  0.04595336],
       [-0.28190779,  0.63540201,  0.04595336],
       [-0.28190779,  0.56699799,  0.04595336],
       [-0.15      ,  0.51459746,  0.04595336],
       [ 0.05209445,  0.50271922,  0.04595336],
       [ 0.22981333,  0.53692124,  0.04595336],
       [ 0.3       ,  0.6012    ,  0.04595336],
       [ 0.3       ,  0.6012    ,  0.14074074],
       [ 0.22981333,  0.66547876,  0.14074074],
       [ 0.05209445,  0.69968078,  0.14074074],
       [-0.15      ,  0.68780254,  0.14074074],
       [-0.28190779,  0.63540201,  0.14074074],
       [-0.28190779,  0.56699799,  0.14074074],
       [-0.15      ,  0.51459746,  0.14074074],
       [ 0.05209445,  0.50271922,  0.14074074],
       [ 0.22981333,  0.53692124,  0.14074074],
       [ 0.3       ,  0.6012    ,  0.14074074],
       [ 0.3       ,  0.6012    ,  0.2441701 ],
       [ 0.22981333,  0.66547876,  0.2441701 ],
       [ 0.05209445,  0.69968078,  0.2441701 ],
       [-0.15      ,  0.68780254,  0.2441701 ],
       [-0.28190779,  0.63540201,  0.2441701 ],
       [-0.28190779,  0.56699799,  0.2441701 ],
       [-0.15      ,  0.51459746,  0.2441701 ],
       [ 0.05209445,  0.50271922,  0.2441701 ],
       [ 0.22981333,  0.53692124,  0.2441701 ],
       [ 0.3       ,  0.6012    ,  0.2441701 ],
       [ 0.3       ,  0.6012    ,  0.36200274],
       [ 0.22981333,  0.66547876,  0.36200274],
       [ 0.05209445,  0.69968078,  0.36200274],
       [-0.15      ,  0.68780254,  0.36200274],
       [-0.28190779,  0.63540201,  0.36200274],
       [-0.28190779,  0.56699799,  0.36200274],
       [-0.15      ,  0.51459746,  0.36200274],
       [ 0.05209445,  0.50271922,  0.36200274],
       [ 0.22981333,  0.53692124,  0.36200274],
       [ 0.3       ,  0.6012    ,  0.36200274],
       [ 0.3       ,  0.6012    ,  0.5       ],
       [ 0.22981333,  0.66547876,  0.5       ],
       [ 0.05209445,  0.69968078,  0.5       ],
       [-0.15      ,  0.68780254,  0.5       ],
       [-0.28190779,  0.63540201,  0.5       ],
       [-0.28190779,  0.56699799,  0.5       ],
       [-0.15      ,  0.51459746,  0.5       ],
       [ 0.05209445,  0.50271922,  0.5       ],
       [ 0.22981333,  0.53692124,  0.5       ],
       [ 0.3       ,  0.6012    ,  0.5       ]])

mlab.points3d(Pts[:,0],
        Pts[:,1],
        Pts[:,2],
        color = (1.,1.,0.))
obb = OBB.build_from_points(Pts)
# get the vertices of the obb
vertices = np.concatenate(obb.points).reshape(-1,3)
mlab.points3d(vertices[:,0],
        vertices[:,1],
        vertices[:,2],
        color = (0.,1.,0.))

from pdb import set_trace
for i in range(vertices.shape[0]):
    mlab.text3d(vertices[i,0] + 0.1,
        vertices[i,1] + 0.1,
        vertices[i,2] + 0.1,
        str(i),
        scale = 0.1)
set_trace()

