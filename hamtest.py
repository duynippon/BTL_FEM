import numpy as np
from matrandocung import MatranDocung
from tensorbiendang import TensorBienDang

np.set_printoptions(precision=4, suppress=True)
phantu_mau = {1: (2, 0), 2: (2, 2), 3: (4, 2)}
#cau1 
cau_1 = MatranDocung(phantu_mau).tinhmatrandocung()

print(np.round(cau_1, 4))
# Dữ liệu
ungsuatx = [21832, 6549, 0]
ungsuaty = [27162, -5288, -1752]
ungsuatxy = [19400, -10381, 8584]
#cau 2 
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

gioi_hanchay = 20e3
vm, trangthai = tensor.ham_tinh_von_mises(gioi_hanchay)

print(f"\nỨng suất Von Mises: {vm/1e3:.2f} KPa -> {trangthai}")

