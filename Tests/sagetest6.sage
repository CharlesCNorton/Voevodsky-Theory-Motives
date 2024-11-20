# Step 1: Define the Elliptic Curve in Weierstrass Form
R.<x> = QQ[]  # Polynomial ring over rational numbers
f = x^3 - x + 1  # Defining a cubic polynomial for an elliptic curve
# Define the elliptic curve in Weierstrass form using the coefficients (a1, a2, a3, a4, a6)
# y^2 = x^3 - x + 1 => EllipticCurve([a1, a2, a3, a4, a6]) with a1 = a2 = a3 = 0, a4 = -1, a6 = 1
E = EllipticCurve([0, 0, 0, -1, 1])

print("Initial Elliptic Curve E:", E)

# Step 2: Compute Rational Points as Proxy for Chow Group of 0-cycles
print("\nRational Points on E (as an approximation for 0-cycles on E):")
# We can attempt to find a finite set of rational points, but we'll use bounds to avoid infinite searches.
rational_points = E.rational_points(bound=100)
print("Rational Points on E (within bound):", rational_points)

# Alternatively, compute the rank of the elliptic curve
rank_before = E.rank()
print("Rank of E (as a measure of rational point structure):", rank_before)

# Step 3: Introduce Degeneration
# We will consider a family of curves parameterized by t that degenerates into a nodal curve.
t = var('t')
# Define a degenerate family by modifying the cubic polynomial, introducing a parameter t
f_degenerate = x^3 - x^2 + t
print("\nDegenerate Family of Curves:", f_degenerate)

# Define a polynomial ring for two variables x and y
S.<x, y> = PolynomialRing(QQ)

# Testing specific values of t to see degeneration behavior
t_values = [0, 0.5, 1, -1, 2]  # Specific values of t to analyze degeneration
for t_val in t_values:
    print("\nTesting for t =", t_val)
    f_t = f_degenerate.subs(t=t_val)
    
    try:
        # Attempt to define the curve as an elliptic curve (if non-singular)
        degenerate_curve = EllipticCurve([0, 0, 0, -f_t.coefficient(x, 1), f_t.coefficient(x, 0)])
        print("Non-singular curve at t = {}:".format(t_val), degenerate_curve)
        
        # Step 4: Compute Rational Points after Degeneration
        rational_points_after = degenerate_curve.rational_points(bound=100)
        print("Rational Points on degenerate curve (t={}):".format(t_val), rational_points_after)

        # Alternatively, compute the rank of the degenerate curve
        rank_after = degenerate_curve.rank()
        print("Rank of degenerate curve at t = {}:".format(t_val), rank_after)

        # Step 5: Compare Rational Points and Rank Before and After Degeneration
        if len(rational_points) == len(rational_points_after):
            print("Number of rational points is stable at t = {}.".format(t_val))
        else:
            print("Number of rational points differs at t = {}.".format(t_val))

        if rank_before == rank_after:
            print("Rank is stable at t = {}.".format(t_val))
        else:
            print("Rank differs at t = {}.".format(t_val))
    
    except ArithmeticError:
        # If the curve is singular, we use a general plane curve representation
        print("Curve at t = {} is singular, analyzing it as a plane curve.".format(t_val))
        
        # Define the curve as a multivariate polynomial in S
        f_multivar = y^2 - f_t
        singular_curve = Curve(f_multivar)  # Directly passing the polynomial, not the ideal
        print("Singular Curve at t = {}: {}".format(t_val, singular_curve))

        # Check the genus and singularity properties
        genus_singular = singular_curve.genus()
        print("Genus of singular curve at t = {}: {}".format(t_val, genus_singular))
        
        singular_points = singular_curve.singular_points()
        print("Singular points of the curve at t = {}: {}".format(t_val, singular_points))

print("\nTest completed.")
