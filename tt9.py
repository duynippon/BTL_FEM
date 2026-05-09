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
        self.von_mises = self.ham_tinh_von_mises()

    def ham_tinh_biendang(self):
        """Tính tensor biến dạng"""
        bien_dang_values = []

        strain_matrix = (1 / self.E) * np.array(
            [[1, -self.v, 0], [-self.v, 1, 0], [0, 0, 1 + self.v]]
        )

        for sx, sy, txy in zip(self.ungsuat_x, self.ungsuat_y, self.ungsuat_xy):
            stress_vector = np.array([sx, sy, txy])
            Ez = (-self.v / (1 - self.v)) * (sx + sy)  # Biến dạng dọc theo z
            Ex, Ey, Exy = strain_matrix @ stress_vector
            bien_dang_values.append((Ex, Ey, Exy, Ez))

        return bien_dang_values

    def ham_tinh_von_mises(self, gioi_hanchay):
        """Tính ứng suất Von Mises cho từng phần tử"""
        von_mises_values = []

        for sx, sy, txy in zip(self.ungsuat_x, self.ungsuat_y, self.ungsuat_xy):
            vm = sqrt(sx**2 - sx * sy + sy**2 + 3 * txy**2)
            von_mises_values.append(vm)
        """Kiểm tra trạng thái từng phần tử"""
        ket_qua = []
        for i, vm in enumerate(von_mises_values):
            trang_thai = "Quá tải" if vm > gioi_hanchay else "An toàn"
            ket_qua.append((i + 1, vm, trang_thai))

        return ket_qua


# Dữ liệu test
ungsuatx = [100e6, 150e6, 120e6]
ungsuaty = [80e6, 90e6, 110e6]
ungsuatxy = [30e6, 40e6, 50e6]

tensor = TensorBienDang(ungsuatx, ungsuaty, ungsuatxy)

print("Biến dạng:")
for i, bd in enumerate(tensor.biendang):
    print(
        f"Phần tử {i+1}: Ex={bd[0]:.6e}, Ey={bd[1]:.6e}, Exy={bd[2]:.6e,}, Ez={bd[3]:.6e}"
    )
