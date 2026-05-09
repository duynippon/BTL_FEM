from matrandocung import MatranDocung
import numpy as np

nutlienquan = [4, 5, 6]
chuyenvichotruoc = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

phantu = {1: (2, 0), 2: (2, 2), 3: (4, 2), 4: (4, 0), 5: (6, 0), 6: (6, 2)}


class ChuyenVi(MatranDocung):
    def __init__(self, chuyenvichotruoc: list, nutlienquan: list, toadoA_x, toadoA_y):

        super().__init__(phantu)

        self.toadoA_x = toadoA_x
        self.toadoA_y = toadoA_y
        self.chuyenvichotruoc = chuyenvichotruoc
        self.nutlienquan = nutlienquan

        self.Ae = self.ham_tinh_Ae()
        self.chuyenvi_phantu = np.array(self.ham_chuyenvi())

    def ham_chuyenvi(self):
        chuyenvi_phantu = []

        for nut in self.nutlienquan:
            index_x = 2 * nut - 2
            index_y = 2 * nut - 1

            chuyenvi_phantu.append(self.chuyenvichotruoc[index_x])
            chuyenvi_phantu.append(self.chuyenvichotruoc[index_y])

        return chuyenvi_phantu

    def tinhchuyenvi(self):
        N1 = (
            (1 / (2 * self.Ae))
            * (
                (self.phantu[self.j][self.y] - self.phantu[self.k][self.y])
                * (self.toadoA_x - self.phantu[self.j][self.x])
                + (self.phantu[self.k][self.x] - self.phantu[self.j][self.x])
                * (self.toadoA_y - self.phantu[self.j][self.y])
            )
            * 10e-6
        )

        N2 = (
            (1 / (2 * self.Ae))
            * (
                (self.phantu[self.k][self.y] - self.phantu[self.i][self.y])
                * (self.toadoA_x - self.phantu[self.k][self.x])
                + (self.phantu[self.i][self.x] - self.phantu[self.k][self.x])
                * (self.toadoA_y - self.phantu[self.k][self.y])
            )
            * 10e-6
        )

        N3 = (
            (1 / (2 * self.Ae))
            * (
                (self.phantu[self.i][self.y] - self.phantu[self.j][self.y])
                * (self.toadoA_x - self.phantu[self.i][self.x])
                + (self.phantu[self.j][self.x] - self.phantu[self.i][self.x])
                * (self.toadoA_y - self.phantu[self.i][self.y])
            )
            * 10e-6
        )

        hamN = np.array([[N1, 0, N2, 0, N3, 0], [0, N1, 0, N2, 0, N3]])

        ux, uy = hamN @ self.chuyenvi_phantu

        return ux, uy

test = ChuyenVi(chuyenvichotruoc, nutlienquan, 3, 1)
print(test.tinhchuyenvi())
