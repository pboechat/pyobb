from numpy import ndarray, array, dot, cross
from numpy.linalg import eigh, norm


########################################################################################################################
# adapted from: http://jamesgregson.blogspot.com/2011/03/latex-test.html
########################################################################################################################
class OBB:
    def __init__(self):
        self.rotation = None
        self.position = None
        self.extents = None
        self.min = None
        self.max = None

    def build_from_covariance_matrix(self, covariance_matrix, points):
        _, eigenvectors = eigh(covariance_matrix)

        def normalize(v):
            n = norm(v)
            if n == 0:
                return v
            return v / n

        r = normalize(eigenvectors[:, 0])
        u = normalize(eigenvectors[:, 1])
        f = normalize(eigenvectors[:, 2])

        self.rotation = ndarray(shape=(3, 3), dtype=float)
        self.rotation[0, 0] = r[0]
        self.rotation[0, 1] = u[0]
        self.rotation[0, 2] = f[0]
        self.rotation[1, 0] = r[1]
        self.rotation[1, 1] = u[1]
        self.rotation[1, 2] = f[1]
        self.rotation[2, 0] = r[2]
        self.rotation[2, 1] = u[2]
        self.rotation[2, 2] = f[2]

        self.min = [1e10, 1e10, 1e10]
        self.max = [-1e10, -1e10, -1e10]
        for point in points:
            p = array(point)
            p_prime = [dot(r, p), dot(u, p), dot(f, p)]
            self.min = array([min(self.min[0], p_prime[0]),
                              min(self.min[1], p_prime[1]),
                              min(self.min[2], p_prime[2])], dtype=float)
            self.max = array([max(self.max[0], p_prime[0]),
                              max(self.max[1], p_prime[1]),
                              max(self.max[2], p_prime[2])], dtype=float)

        center = (self.max + self.min) / 2.0
        self.position = (dot(self.rotation[0], center), dot(self.rotation[1], center), dot(self.rotation[2], center))
        self.extents = (self.max - self.min) / 2.0

    def build_from_triangles(self, points, triangles):
        weighed_mean = array([0, 0, 0], dtype=float)
        area_sum = 0
        c00 = c01 = c02 = c11 = c12 = c22 = 0
        for i in range(0, len(triangles), 3):
            p = array(points[triangles[i]], dtype=float)
            q = array(points[triangles[i + 1]], dtype=float)
            r = array(points[triangles[i + 2]], dtype=float)
            mean = (p + q + r) / 3.0
            area = norm(cross((q - p), (r - p))) / 2.0
            weighed_mean += mean * area
            area_sum += area
            c00 += (9.0 * mean[0] * mean[0] + p[0] * p[0] + q[0] * q[0] + r[0] * r[0]) * (area / 12.0)
            c01 += (9.0 * mean[0] * mean[1] + p[0] * p[1] + q[0] * q[1] + r[0] * r[1]) * (area / 12.0)
            c02 += (9.0 * mean[0] * mean[2] + p[0] * p[2] + q[0] * q[2] + r[0] * r[2]) * (area / 12.0)
            c11 += (9.0 * mean[1] * mean[1] + p[1] * p[1] + q[1] * q[1] + r[1] * r[1]) * (area / 12.0)
            c12 += (9.0 * mean[1] * mean[2] + p[1] * p[2] + q[1] * q[2] + r[1] * r[2]) * (area / 12.0)

        weighed_mean /= area_sum
        c00 /= area_sum
        c01 /= area_sum
        c02 /= area_sum
        c11 /= area_sum
        c12 /= area_sum
        c22 /= area_sum

        c00 -= weighed_mean[0] * weighed_mean[0]
        c01 -= weighed_mean[0] * weighed_mean[1]
        c02 -= weighed_mean[0] * weighed_mean[2]
        c11 -= weighed_mean[1] * weighed_mean[1]
        c12 -= weighed_mean[1] * weighed_mean[2]
        c22 -= weighed_mean[2] * weighed_mean[2]

        covariance_matrix = ndarray(shape=(3, 3), dtype=float)
        covariance_matrix[0, 0] = c00
        covariance_matrix[0, 1] = c01
        covariance_matrix[0, 2] = c02
        covariance_matrix[1, 0] = c01
        covariance_matrix[1, 1] = c11
        covariance_matrix[1, 2] = c12
        covariance_matrix[2, 0] = c02
        covariance_matrix[1, 2] = c12
        covariance_matrix[2, 2] = c22

        self.build_from_covariance_matrix(covariance_matrix, points)

    def build_from_points(self, points):
        mean = array([0, 0, 0], dtype=float)
        num_points = len(points)
        for i in range(0, len(points)):
            point = array(points[i], dtype=float)
            mean += point / num_points

        c00 = c01 = c02 = c11 = c12 = c22 = 0
        for i in range(0, len(points)):
            point = array(points[i], dtype=float)
            c00 += point[0] * point[0] - mean[0] * mean[0]
            c01 += point[0] * point[1] - mean[0] * mean[1]
            c02 += point[0] * point[2] - mean[0] * mean[2]
            c11 += point[1] * point[1] - mean[1] * mean[1]
            c12 += point[1] * point[2] - mean[1] * mean[2]
            c22 += point[2] * point[2] - mean[2] * mean[2]

        covariance_matrix = ndarray(shape=(3, 3), dtype=float)
        covariance_matrix[0, 0] = c00
        covariance_matrix[0, 1] = c01
        covariance_matrix[0, 2] = c02
        covariance_matrix[1, 0] = c01
        covariance_matrix[1, 1] = c11
        covariance_matrix[1, 2] = c12
        covariance_matrix[2, 0] = c02
        covariance_matrix[2, 1] = c12
        covariance_matrix[2, 2] = c22

        self.build_from_covariance_matrix(covariance_matrix, points)
