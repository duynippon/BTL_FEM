import tkinter as tk
from itertools import combinations
import numpy as np
from matrandocung import MatranDocung
from tensorbiendang import TensorBienDang
from tkinter import simpledialog
from chuyenvi import ChuyenVi

from tkinter import simpledialog

np.set_printoptions(precision=4, suppress=True)

GRID_SIZE = 5  # kích thước lưới 5x5
SPACING = 100  # khoảng cách hiển thị trên canvas
REAL_SPACING = 2  # mỗi ô cách nhau 2m
NODE_RADIUS = 8  # bán kính node trên canvas
MARGIN = 50  # khoảng cách từ mép canvas đến lưới

selected_node = None  # node đang được chọn để nối cạnh
lines = []  # lưu trữ các cạnh đã vẽ
edges = set()  # lưu trữ các cạnh đã vẽ

node_dict = {}  # lưu trữ mapping node_id -> (x, y) thực tế
coord_to_id = (
    {}
)  # lưu trữ mapping (x, y) thực tế -> node_id để tránh trùng lặp khi click vào cùng 1 node
next_node_id = (
    0  # biến toàn cục để gán ID cho node mới khi click vào node chưa được gán ID
)

root = tk.Tk()
root.title("Node numbering")

canvas_width = GRID_SIZE * SPACING + 2 * MARGIN
canvas_height = GRID_SIZE * SPACING + 2 * MARGIN

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

nodes = {}

# -----------------------------
# Vẽ lưới
# -----------------------------
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        x = MARGIN + i * SPACING
        y = canvas_height - (MARGIN + j * SPACING)

        node = canvas.create_oval(
            x - NODE_RADIUS,
            y - NODE_RADIUS,
            x + NODE_RADIUS,
            y + NODE_RADIUS,
            fill="lightblue",
        )

        # tọa độ thực tế cách nhau 2m
        nodes[node] = (i * REAL_SPACING, j * REAL_SPACING)


# -----------------------------
# Đánh số node
# -----------------------------
def assign_node_id(coord):
    global next_node_id

    if coord not in coord_to_id:
        coord_to_id[coord] = next_node_id
        node_dict[next_node_id] = coord
        next_node_id += 1

    return coord_to_id[coord]


# -----------------------------
# Phát hiện tam giác
# -----------------------------
def detect_triangles():
    triangles = []

    all_nodes = list(coord_to_id.keys())

    for a, b, c in combinations(all_nodes, 3):
        e1 = tuple(sorted([a, b]))
        e2 = tuple(sorted([b, c]))
        e3 = tuple(sorted([a, c]))

        if e1 in edges and e2 in edges and e3 in edges:
            triangles.append((a, b, c))

    return triangles


# -----------------------------
# Click node
# -----------------------------
def on_node_click(event):
    global selected_node

    clicked = canvas.find_closest(event.x, event.y)[0]

    if clicked not in nodes:
        return

    coord = nodes[clicked]
    node_id = assign_node_id(coord)

    x = canvas.coords(clicked)[0] + NODE_RADIUS
    y = canvas.coords(clicked)[1] + NODE_RADIUS

    canvas.create_text(x, y + 20, text=str(node_id), fill="red")

    if selected_node is None:
        selected_node = clicked
        canvas.itemconfig(clicked, fill="red")

    else:
        c1 = nodes[selected_node]
        c2 = coord

        x1 = canvas.coords(selected_node)[0] + NODE_RADIUS
        y1 = canvas.coords(selected_node)[1] + NODE_RADIUS

        edge = tuple(sorted([c1, c2]))

        if edge not in edges:
            canvas.create_line(x1, y1, x, y, width=2)
            edges.add(edge)

        canvas.itemconfig(selected_node, fill="lightblue")
        selected_node = None

        update_output()


# from chuyenvi import ChuyenVi   # nếu có class này


# -----------------------------
# Nút giải ma trận độ cứng
# -----------------------------


def solve_stiffness():
    if len(node_dict) < 3:
        output.insert(tk.END, "\nCần ít nhất 3 node.\n")
        return

    try:
        n1 = simpledialog.askinteger("Nhập node", "Node thứ 1 tạo tam giác:")
        n2 = simpledialog.askinteger("Nhập node", "Node thứ 2 tạo tam giác:")
        n3 = simpledialog.askinteger("Nhập node", "Node thứ 3 tạo tam giác:")

        if None in [n1, n2, n3]:
            return

        # kiểm tra node có tồn tại không
        for n in [n1, n2, n3]:
            if n not in node_dict:
                output.insert(tk.END, f"\nNode {n} không tồn tại.\n")
                return

        phantu = {1: node_dict[n1], 2: node_dict[n2], 3: node_dict[n3]}

        output.insert(tk.END, "\n=== Phần tử đã chọn ===\n")
        output.insert(tk.END, f"Node [{n1}, {n2}, {n3}]\n")
        output.insert(tk.END, f"Tọa độ: {phantu}\n")

        k = MatranDocung(phantu).tinhmatrandocung()

        output.insert(tk.END, "\n=== Ma trận độ cứng ===\n")
        output.insert(tk.END, f"{np.round(k,4)}\n")

    except Exception as e:
        output.insert(tk.END, f"\nLỗi: {e}\n")


# -----------------------------
# Nút giải chuyển vị
# -----------------------------


def solve_displacement():
    try:
        so_pt = simpledialog.askinteger("Số phần tử", "Nhập số phần tử:")

        if so_pt is None or so_pt <= 0:
            return

        ungsuatx = []
        ungsuaty = []
        ungsuatxy = []

        for i in range(so_pt):
            data = simpledialog.askstring(
                f"Phần tử {i+1}",
                f"Nhập σx, σy, τxy cho phần tử {i+1}\n" f"Ví dụ: 21832,27162,19400",
            )

            if data is None:
                return

            sx, sy, sxy = map(float, data.split(","))

            ungsuatx.append(sx)
            ungsuaty.append(sy)
            ungsuatxy.append(sxy)

        tensor = TensorBienDang(ungsuatx, ungsuaty, ungsuatxy)

        output.insert(tk.END, "\nBiến dạng:\n")

        for i, bd in enumerate(tensor.biendang):
            output.insert(
                tk.END,
                f"Phần tử {i+1}: "
                f"Ex={bd[0]:.6e}, "
                f"Ey={bd[1]:.6e}, "
                f"Exy={bd[2]:.6e}, "
                f"Ez={bd[3]:.6e}\n",
            )

        gioi_hanchay = simpledialog.askfloat("Giới hạn chảy", "Nhập giới hạn chảy:")

        if gioi_hanchay is None:
            return

        vm, trangthai = tensor.ham_tinh_von_mises(gioi_hanchay)

        output.insert(
            tk.END, f"\nỨng suất Von Mises: {vm/1e3:.2f} KPa -> {trangthai}\n"
        )

    except Exception as e:
        output.insert(tk.END, f"\nLỗi nhập liệu: {e}\n")


def tinh_chuyenvi():

    try:
        # nhập toàn bộ vector chuyển vị đã biết
        data = simpledialog.askstring(
            "Nhập chuyển vị",
            "Nhập toàn bộ chuyển vị cách nhau dấu phẩy\nVí dụ:\n1,2,3,4,5,6,7,8,9,10,11,12",
        )

        if data is None:
            return

        chuyenvichotruoc = list(map(float, data.split(",")))

        

        # nhập các node liên quan
        nut_data = simpledialog.askstring(
            "Node liên quan", "Nhập 3 node liên quan\nVí dụ: 4,5,6"
        )

        if nut_data is None:
            return

        nutlienquan = list(map(int, nut_data.split(",")))

        if len(nutlienquan) != 3:
            output.insert(tk.END, "\nPhải nhập đúng 3 node.\n")
            return

        # tọa độ điểm cần nội suy
        toadoA_x = simpledialog.askfloat("Tọa độ A", "Nhập x:")
        toadoA_y = simpledialog.askfloat("Tọa độ A", "Nhập y:")

        if None in [toadoA_x, toadoA_y]:
            return

        # tính chuyển vị
        ketqua = ChuyenVi(chuyenvichotruoc, nutlienquan, toadoA_x, toadoA_y)

        ux, uy = ketqua.tinhchuyenvi()

        output.insert(tk.END, "\n=== Kết quả chuyển vị ===\n")
        output.insert(tk.END, f"ux = {ux:.6e}\n")
        output.insert(tk.END, f"uy = {uy:.6e}\n")

    except Exception as e:
        output.insert(tk.END, f"\nLỗi tính chuyển vị: {e}\n")


# -----------------------------
# Frame chứa nút
# -----------------------------
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn1 = tk.Button(button_frame, text="Ma trận độ cứng", command=solve_stiffness)
btn1.pack(side=tk.LEFT, padx=5)

btn2 = tk.Button(button_frame, text="Tensor biến dạng", command=solve_displacement)
btn2.pack(side=tk.LEFT, padx=5)

btn3 = tk.Button(button_frame, text="Chuyển vị", command=tinh_chuyenvi)
btn3.pack(side=tk.LEFT, padx=5)

canvas.bind("<Button-1>", on_node_click)

output = tk.Text(root, height=30, width=100)
output.pack()


root.mainloop()
