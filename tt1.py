from math import sqrt
import numpy as np


class TensorBienDang:
    def __init__(self, UNGSUAT_x, UNGSUAT_y, UNGSUAT_xy):
        self.E = 210e9
        self.v = 0.3
        self.t = 15e-3

        self.ungsuat_x = UNGSUAT_x
        self.ungsuat_y = UNGSUAT_y
        self.ungsuat_xy = UNGSUAT_xy

        self.biendang = self.ham_tinh_biendang()

    def ham_tinh_biendang(self):
        """Tính tensor biến dạng"""
        bien_dang_values = []

        strain_matrix = (1 / self.E) * np.array(
            [[1, -self.v, 0], [-self.v, 1, 0], [0, 0, 1 + self.v]]
        )

        for sx, sy, txy in zip(self.ungsuat_x, self.ungsuat_y, self.ungsuat_xy):
            stress_vector = np.array([sx, sy, txy])

            Ex, Ey, Exy = strain_matrix @ stress_vector
            Ez = (-self.v / self.E) * (sx + sy)

            bien_dang_values.append((Ex, Ey, Exy, Ez))

        return bien_dang_values

    def ham_tinh_von_mises(self, gioi_hanchay):
        """Tính ứng suất Von Mises và kiểm tra"""
        ket_qua = []
        ungsuat_trungbinh = 0
        for i, (sx, sy, txy) in enumerate(
            zip(self.ungsuat_x, self.ungsuat_y, self.ungsuat_xy)
        ):
            vm = sqrt(sx**2 - sx * sy + sy**2 + 3 * txy**2)

            trang_thai = "Quá tải" if vm > gioi_hanchay else "An toàn"

            ket_qua.append((i + 1, vm, trang_thai))
        for index in range(len(ket_qua)):

            ungsuat_trungbinh += self.ket_qua[index][1]

        return ungsuat_trungbinh / len(ket_qua)


# Dữ liệu test
ungsuatx = [21832, 6549, 0]
ungsuaty = [27162, -5288, -1752]
ungsuatxy = [19400, -10381, 8584]

tensor = TensorBienDang(ungsuatx, ungsuaty, ungsuatxy)
