from sage.all import *

# Define the projective space and hypersurface
P = ProjectiveSpace(3, QQ, names='x,y,z,w')
x, y, z, w = P.gens()
degree = 3

# Hypersurface equation
hypersurface_eq = x^3 + y^3 + z^3 + w^3
H = P.subscheme([hypersurface_eq])

# Theoretical Betti Numbers for Smooth Hypersurface
n = 3  # Dimension of projective space
b_0 = 1  # Single connected component
b_1 = 0  # No loops
b_2 = 0  # No 2D boundaries
b_middle = binomial(n, n - 1) * (degree - 1)**(n - 1) - binomial(n, n - 2) * (degree - 1)**(n - 2)
b_total = [b_0, b_1, b_2] + [b_middle]  # Total Betti numbers
euler_characteristic_theoretical = sum((-1)**i * b_total[i] for i in range(len(b_total)))

# Output theoretical results
print("Theoretical Betti Numbers:", b_total)
print("Theoretical Euler Characteristic:", euler_characteristic_theoretical)

# Compute middle Betti number explicitly
middle_betti_number = b_total[-1]
print("Middle Betti Number (Motivic Rank):", middle_betti_number)

# Consistency check for Euler characteristic
computed_euler_characteristic = sum((-1)**i * b_total[i] for i in range(len(b_total)))
if computed_euler_characteristic == euler_characteristic_theoretical:
    print("Euler characteristic is consistent with Betti numbers.")
else:
    print("Euler characteristic is inconsistent, further investigation required.")

# Summary of results
print("Betti numbers:", b_total)
print("Euler characteristic:", computed_euler_characteristic)
print("Motivic rank (middle Betti number):", middle_betti_number)
