x= 0 
y = 1
def ham_tinh_Ae(phantu):
    Ae = 0.5 * (
        (phantu[2][x] * phantu[3][y] - phantu[3][x] * phantu[2][y])
        + (phantu[2][y] - phantu[3][y]) * phantu[1][x]
        + phantu[1][y] * (phantu[3][x] - phantu[2][x])
    )
    return abs(Ae)


phantu_mau = {1: (2, 0), 2: (2, 2), 3: (4, 2)}
print(ham_tinh_Ae(phantu_mau))
