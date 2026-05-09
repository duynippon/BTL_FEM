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
        """Tính ứng suất Von Mises"""

        sx = sum(self.ungsuat_x) / len(self.ungsuat_x)
        sy = sum(self.ungsuat_y) / len(self.ungsuat_y)
        txy = sum(self.ungsuat_xy) / len(self.ungsuat_xy)

        # Công thức đúng cho ứng suất phẳng
        vm = sqrt(sx**2 - sx * sy + sy**2 + 3 * txy**2)

        trang_thai = "Quá tải" if vm > gioi_hanchay else "An toàn"

        return vm, trang_thai


# Dữ liệu
ungsuatx = [21832, 6549, 0]
ungsuaty = [27162, -5288, -1752]
ungsuatxy = [19400, -10381, 8584]

tensor = TensorBienDang(ungsuatx, ungsuaty, ungsuatxy)

print("Biến dạng:")
for i, bd in enumerate(tensor.biendang):
    print(
        f"Phần tử {i+1}: "
        f"Ex={bd[0]:.6e}, "
        f"Ey={bd[1]:.6e}, "
        f"Exy={bd[2]:.6e}, "
        f"Ez={bd[3]:.6e}"
    )
