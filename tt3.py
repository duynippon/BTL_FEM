import numpy as np


class MatranDocung:
    def __init__(self, phantu):
        self.E = 210 * 10**9
        self.v = 0.3
        self.t = 15 * 10**(-3)

        self.phantu = phantu

        self.x = 0
        self.y = 1

        self.i = 1
        self.j = 2
        self.k = 3

        self.C2 = self.v
        self.lamda = (1 - self.v) / 2

    def ham_tinh_Ae(self):
        p = self.phantu
        x, y = self.x, self.y

        Ae = 0.5 * (
            (p[2][x] * p[3][y] - p[3][x] * p[2][y])
            + (p[2][y] - p[3][y]) * p[1][x]
            + p[1][y] * (p[3][x] - p[2][x])
        )
        return abs(Ae)

    def ham_tinh_C1(self):
        return self.E / (1 - self.v**2)

    def tinhmatrandocung(self):
        p = self.phantu
        x, y = self.x, self.y
        i, j, k = self.i, self.j, self.k
        lamda = self.lamda
        C2 = self.C2

        Ae = self.ham_tinh_Ae()
        C1 = self.ham_tinh_C1()

        # Hàng 1
        k11 = (p[j][y] - p[k][y])**2 + lamda*(p[j][x] - p[k][x])**2
        k12 = -C2*(p[j][x] - p[k][x])*(p[j][y] - p[k][y]) - lamda*(p[j][y] - p[k][y])*(p[j][x] - p[k][x])
        k13 = -(p[j][y] - p[k][y])*(p[i][y] - p[k][y]) - lamda*(p[j][x] - p[k][x])*(p[i][x] - p[k][x])
        k14 = C2*(p[i][x] - p[k][x])*(p[j][y] - p[k][y]) + lamda*(p[i][y] - p[k][y])*(p[j][x] - p[k][x])
        k15 = (p[j][y] - p[k][y])*(p[i][y] - p[j][y]) + lamda*(p[j][x] - p[k][x])*(p[i][x] - p[j][x])
        k16 = -C2*(p[j][y] - p[k][y])*(p[i][x] - p[j][x]) - lamda*(p[j][x] - p[k][x])*(p[i][y] - p[j][y])

        # Ma trận tam giác trên
        A = np.array([
            [k11, k12, k13, k14, k15, k16],
            [0, 0,   0,   0,   0,   0],
            [0, 0,   0,   0,   0,   0],
            [0, 0,   0,   0,   0,   0],
            [0, 0,   0,   0,   0,   0],
            [0, 0,   0,   0,   0,   0]
        ])

        # Đối xứng
        A = A + A.T - np.diag(np.diag(A))

        # Nhân hệ số
        A = A * C1 * self.t / (4 * Ae)

        return A


# Test
phantu = {
    1: (0, 0),
    2: (1, 0),
    3: (0, 1)
}

matran = MatranDocung(phantu)
np.set_printoptions(precision=4, suppress=True)
print(np.round(matran.tinhmatrandocung(), 2))