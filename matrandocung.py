import numpy as np

np.set_printoptions(precision=4, suppress=True)


class MatranDocung:
    def __init__(self, phantu):
        self.E = 210 * 10**9
        self.v = 0.3
        self.t = 15 * 10 ** (-3)

        self.phantu = phantu
        self.x = 0
        self.y = 1

        self.i = 1
        self.j = 2
        self.k = 3

        self.C2 = self.v
        self.lamda = (1 -  self.v) / 2 
        self.Ae = self.ham_tinh_Ae()
        self.C1 = self.ham_tinh_C1()

    def ham_tinh_Ae(self):
        Ae = 0.5 * (
            (
                self.phantu[2][self.x] * self.phantu[3][self.y]
                - self.phantu[3][self.x] * self.phantu[2][self.y]
            )
            + (self.phantu[2][self.y] - self.phantu[3][self.y]) * self.phantu[1][self.x]
            + self.phantu[1][self.y] * (self.phantu[3][self.x] - self.phantu[2][self.x])
        )
        Ae = abs(Ae)
        return Ae

    def ham_tinh_C1(self):
        C1 = self.E / (1 - self.v**2)
        return C1

    def tinhmatrandocung(self):
        phantu = self.phantu

        x = self.x
        y = self.y
        i = self.i
        j = self.j
        k = self.k

        Ae = self.ham_tinh_Ae()
        C1 = self.ham_tinh_C1()

        # Hàng 1
        k11 = (phantu[j][y] - phantu[k][y]) ** 2 + self.lamda * (
            phantu[j][x] - phantu[k][x]
        ) ** 2

        k12 = -self.C2 * (phantu[j][x] - phantu[k][x]) * (
            phantu[j][y] - phantu[k][y]
        ) - self.lamda * (phantu[j][y] - phantu[k][y]) * (phantu[j][x] - phantu[k][x])

        k13 = -(phantu[j][y] - phantu[k][y]) * (
            phantu[i][y] - phantu[k][y]
        ) - self.lamda * (phantu[j][x] - phantu[k][x]) * (phantu[i][x] - phantu[k][x])

        k14 = self.C2 * (phantu[i][x] - phantu[k][x]) * (
            phantu[j][y] - phantu[k][y]
        ) + self.lamda * (phantu[i][y] - phantu[k][y]) * (phantu[j][x] - phantu[k][x])

        k15 = (phantu[j][y] - phantu[k][y]) * (
            phantu[i][y] - phantu[j][y]
        ) + self.lamda * (phantu[j][x] - phantu[k][x]) * (phantu[i][x] - phantu[j][x])

        k16 = -self.C2 * (phantu[j][y] - phantu[k][y]) * (
            phantu[i][x] - phantu[j][x]
        ) - self.lamda * (phantu[j][x] - phantu[k][x]) * (phantu[i][y] - phantu[j][y])

        hang1 = [k11, k12, k13, k14, k15, k16]

        # Hàng 2
        k22 = (phantu[j][x] - phantu[k][x]) ** 2 + self.lamda * (
            phantu[j][y] - phantu[k][y]
        ) ** 2

        k23 = self.C2 * (phantu[j][x] - phantu[k][x]) * (
            phantu[i][y] - phantu[k][y]
        ) + self.lamda * (phantu[i][x] - phantu[k][x]) * (phantu[j][y] - phantu[k][y])

        k24 = -(phantu[j][x] - phantu[k][x]) * (
            phantu[i][x] - phantu[k][x]
        ) - self.lamda * (phantu[j][y] - phantu[k][y]) * (phantu[i][y] - phantu[k][y])

        k25 = -self.C2 * (phantu[j][x] - phantu[k][x]) * (
            phantu[i][y] - phantu[j][y]
        ) - self.lamda * (phantu[j][y] - phantu[k][y]) * (phantu[i][x] - phantu[j][x])

        k26 = (phantu[i][x] - phantu[j][x]) * (
            phantu[j][x] - phantu[k][x]
        ) + self.lamda * (phantu[j][y] - phantu[k][y]) * (phantu[i][y] - phantu[j][y])

        hang2 = [0, k22, k23, k24, k25, k26]

        # Hàng 3
        k33 = (phantu[i][y] - phantu[k][y]) ** 2 + self.lamda * (
            phantu[i][x] - phantu[k][x]
        ) ** 2

        k34 = -self.C2 * (phantu[i][x] - phantu[k][x]) * (
            phantu[i][y] - phantu[k][y]
        ) - self.lamda * (phantu[i][x] - phantu[k][x]) * (phantu[i][y] - phantu[k][y])

        k35 = -(phantu[i][y] - phantu[k][y]) * (
            phantu[i][y] - phantu[j][y]
        ) - self.lamda * (phantu[i][x] - phantu[k][x]) * (phantu[i][x] - phantu[j][x])

        k36 = self.C2 * (phantu[i][x] - phantu[j][x]) * (
            phantu[i][y] - phantu[k][y]
        ) + self.lamda * (phantu[i][x] - phantu[k][x]) * (phantu[i][y] - phantu[j][y])

        hang3 = [0, 0, k33, k34, k35, k36]

        # Hàng 4
        k44 = (phantu[i][x] - phantu[k][x]) ** 2 + self.lamda * (
            phantu[i][y] - phantu[k][y]
        ) ** 2

        k45 = self.C2 * (phantu[i][x] - phantu[k][x]) * (
            phantu[i][y] - phantu[j][y]
        ) + self.lamda * (phantu[i][y] - phantu[k][y]) * (phantu[i][x] - phantu[j][x])

        k46 = -(phantu[i][x] - phantu[k][x]) * (
            phantu[i][x] - phantu[j][x]
        ) - self.lamda * (phantu[i][y] - phantu[k][y]) * (phantu[i][y] - phantu[j][y])

        hang4 = [0, 0, 0, k44, k45, k46]

        # Hàng 5
        k55 = (phantu[i][y] - phantu[j][y]) ** 2 + self.lamda * (
            phantu[i][x] - phantu[j][x]
        ) ** 2

        k56 = -self.C2 * (phantu[i][x] - phantu[j][x]) * (
            phantu[i][y] - phantu[j][y]
        ) - self.lamda * (phantu[i][x] - phantu[j][x]) * (phantu[i][y] - phantu[j][y])

        hang5 = [0, 0, 0, 0, k55, k56]

        # Hàng 6
        k66 = (phantu[i][x] - phantu[j][x]) ** 2 + self.lamda * (
            phantu[i][y] - phantu[j][y]
        ) ** 2

        hang6 = [0, 0, 0, 0, 0, k66]

        # Tạo ma trận
        cau_1 = np.zeros((6, 6))

        cau_1[0] = hang1
        cau_1[1] = hang2
        cau_1[2] = hang3
        cau_1[3] = hang4
        cau_1[4] = hang5
        cau_1[5] = hang6

        # Đối xứng ma trận
        cau_1 = cau_1 + cau_1.T - np.diag(np.diag(cau_1))

        # Ma trận độ cứng
        A = cau_1 * self.C1 * self.t / (4 * self.Ae)

        return A
