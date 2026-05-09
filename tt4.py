import numpy as np
i = "i"
j = "j"
k = "k"
# Tam giác mẫu
phantu_mau = {1: (0, 0), 2: (1, 0), 3: (0, 1)}

phantu = {i: (0, 0), j: (1, 0), k: (0, 1)}


class MatranDocung:
    self.E = 210 * 10**9
    self.v = 0.3
    self.t = 15 * 10**(-3)

    self.phantu = phantu

    self.x = 0
    self.y = 1

    self.i = 1
    self.j = 2
    self.k = 3

    self.self.C2 = self.v
    self.lamda = (1 - self.v) / 2
    def __init__(self, phantu, phantu_mau):
        self.phantu = phantu
        self.phantu_mau = phantu_mau
        self.lamda = (1 - v) / 2

    def ham_tinh_Ae(self,phantu_mau):
        Ae = 0.5 * (
            (
                self.phantu_mau[2][x] * self.phantu_mau[3][y]
                - self.phantu_mau[3][x] * self.phantu_mau[2][y]
            )
            + (self.phantu_mau[2][y] - self.phantu_mau[3][y]) * self.phantu_mau[1][x]
            + self.phantu_mau[1][y] * (self.phantu_mau[3][x] - self.phantu_mau[2][x])
        )
        return abs(Ae)

    def ham_tinh_C(self, E, v):
        C = E / (1 - v**2)
        return C

    def ham_tinh_Ae(phantu_mau):
        Ae = 0.5 * (
            (phantu_mau[2][x] * phantu_mau[3][y] - phantu_mau[3][x] * phantu_mau[2][y])
            + (phantu_mau[2][y] - phantu_mau[3][y]) * phantu_mau[1][x]
            + phantu_mau[1][y] * (phantu_mau[3][x] - phantu_mau[2][x])
        )
        return abs(Ae)


    def ham_tinh_C1(self.E, self.v):
        return self.C1 = self.E / (1 - self.v**2)
    def tinhmatrandocung(phantu):
        Ae = self.ham_tinh_Ae(self.phantu_mau)
        C1 = self.ham_tinh_C1(self.E, self.v)
        global x, y, lamda, self.C2
        # Tính hàng 1
        k11 = (phantu[j][y] - phantu[k][y]) ** 2 + self.lamda * (
            phantu[j][x] - phantu[k][x]
        ) ** 2
        k12 = -self.C2 * (phantu[j][x] - phantu[k][x]) * (
            phantu[j][y] - phantu[k][y]
        ) - self.lamda * (phantu[j][y] - phantu[k][y]) * (phantu[j][x] - phantu[k][x])
        k13 = -(phantu[j][y] - phantu[k][y]) * (phantu[i][y] - phantu[k][y]) - self.lamda * (
            phantu[j][x] - phantu[k][x]
        ) * (phantu[i][x] - phantu[k][x])
        k14 = self.C2 * (phantu[i][x] - phantu[k][x]) * (phantu[j][y] - phantu[k][y]) + self.lamda * (
            phantu[i][y] - phantu[k][y]
        ) * (phantu[j][x] - phantu[k][x])
        k15 = (phantu[j][y] - phantu[k][y]) * (phantu[i][y] - phantu[j][y]) + self.lamda * (
            phantu[j][x] - phantu[k][x]
        ) * (phantu[i][x] - phantu[j][x])
        k16 = -self.C2 * (phantu[j][y] - phantu[k][y]) * (
            phantu[i][x] - phantu[j][x]
        ) - self.lamda * (phantu[j][x] - phantu[k][x]) * (phantu[i][y] - phantu[j][y])

        hang1 = [k11, k12, k13, k14, k15, k16]
        # tinh hang 2
        k22 = (phantu[j][x] - phantu[k][x]) ** 2 + self.lamda * (
            phantu[j][y] - phantu[k][y]
        ) ** 2

        k23 = self.C2 * (phantu[j][x] - phantu[k][x]) * (phantu[i][y] - phantu[k][y]) + self.lamda * (
            phantu[i][x] - phantu[k][x]
        ) * (phantu[j][y] - phantu[k][y])

        k24 = -(phantu[j][x] - phantu[k][x]) * (phantu[i][x] - phantu[k][x]) - self.lamda * (
            phantu[j][y] - phantu[k][y]
        ) * (phantu[i][y] - phantu[k][y])

        k25 = -self.C2 * (phantu[j][x] - phantu[k][x]) * (
            phantu[i][y] - phantu[j][y]
        ) - self.lamda * (phantu[j][y] - phantu[k][y]) * (phantu[i][x] - phantu[j][x])

        k26 = (phantu[i][x] - phantu[j][x]) * (phantu[j][x] - phantu[k][x]) + self.lamda * (
            phantu[j][y] - phantu[k][y]
        ) * (phantu[i][y] - phantu[j][y])
        hang2 = [0, k22, k23, k24, k25, k26]
        # tinh hang 3
        k33 = (phantu[i][y] - phantu[k][y]) ** 2 + self.lamda * (
            phantu[i][x] - phantu[k][x]
        ) ** 2

        k34 = -self.C2 * (phantu[i][x] - phantu[k][x]) * (
            phantu[i][y] - phantu[k][y]
        ) - self.lamda * (phantu[i][x] - phantu[k][x]) * (phantu[i][y] - phantu[k][y])

        k35 = -(phantu[i][y] - phantu[k][y]) * (phantu[i][y] - phantu[j][y]) - self.lamda * (
            phantu[i][x] - phantu[k][x]
        ) * (phantu[i][x] - phantu[j][x])

        k36 = self.C2 * (phantu[i][x] - phantu[j][x]) * (phantu[i][y] - phantu[k][y]) + self.lamda * (
            phantu[i][x] - phantu[k][x]
        ) * (phantu[i][y] - phantu[j][y])
        hang3 = [0, 0, k33, k34, k35, k36]
        # tinh hang 4
        k44 = (phantu[i][x] - phantu[k][x]) ** 2 + self.lamda * (
            phantu[i][y] - phantu[k][y]
        ) ** 2

        k45 = self.C2 * (phantu[i][x] - phantu[k][x]) * (phantu[i][y] - phantu[j][y]) + self.lamda * (
            phantu[i][y] - phantu[k][y]
        ) * (phantu[i][x] - phantu[j][x])

        k46 = -(phantu[i][x] - phantu[k][x]) * (phantu[i][x] - phantu[j][x]) - self.lamda * (
            phantu[i][y] - phantu[k][y]
        ) * (phantu[i][y] - phantu[j][y])
        hang4 = [0, 0, 0, k44, k45, k46]
        # tinh hang 5
        k55 = (phantu[i][y] - phantu[j][y]) ** 2 + self.lamda * (
            phantu[i][x] - phantu[j][x]
        ) ** 2

        k56 = -self.C2 * (phantu[i][x] - phantu[j][x]) * (
            phantu[i][y] - phantu[j][y]
        ) - self.lamda * (phantu[i][x] - phantu[j][x]) * (phantu[i][y] - phantu[j][y])
        hang5 = [0, 0, 0, 0, k55, k56]
        # tinh hang 6
        k66 = (phantu[i][x] - phantu[j][x]) ** 2 + self.lamda * (
            phantu[i][y] - phantu[j][y]
        ) ** 2
        hang6 = [0, 0, 0, 0, 0, k66]

        # Tạo ma trận 6x6
        cau_1 = np.zeros((6, 6))

        # Gán hàng đầu tiên
        for col in range(6):
            cau_1[0][col] = hang1[col]
        for col in range(6):
            cau_1[1][col] = hang2[col]

        for col in range(6):
            cau_1[2][col] = hang3[col]

        for col in range(6):
            cau_1[3][col] = hang4[col]
        for col in range(6):
            cau_1[4][col] = hang5[col]
        for col in range(6):
            cau_1[5][col] = hang6[col]
        A = cau_1 * C1 * t / 4 * Ae
        A = A + A.T - np.diag(np.diag(A))
        return A




