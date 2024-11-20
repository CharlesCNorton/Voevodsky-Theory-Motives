from sage.all import *

def analyze_elliptic_curve(base_field):
    print(f"Analyzing Elliptic Curve over {base_field}:")
    E = EllipticCurve(base_field, [0, 0, 0, -1, 1])  # y^2 = x^3 - x + 1
    print(E)

    # Rational points
    print("\nRational Points (within bound):")
    points = E.rational_points(bound=10)
    print(points)

    # Rank of the elliptic curve
    rank = E.rank()
    print("\nRank of E:", rank)
    return E

def analyze_degenerate_family(base_field):
    print(f"\nDegenerate Family of Curves over {base_field}: x^3 - x^2 + t")
    R.<x, y, z, t> = PolynomialRing(base_field)  # Include 'z' in the ring for projective cases
    f_base = x^3 - x^2

    # Test different values of t
    results = []
    for t_val in [0, 1, 2]:
        print(f"\nTesting for t = {t_val}")
        f_t = f_base + t_val
        f_t_univariate = f_t.subs(t=t_val)  # Specialize t to get a univariate polynomial

        try:
            # Convert to proper univariate polynomial
            f_t_univariate = PolynomialRing(base_field, 'x')(f_t_univariate)

            # Attempt to define the curve as an elliptic curve (if non-singular)
            degenerate_curve = EllipticCurve(base_field, [0, 0, 0, -f_t_univariate[1], f_t_univariate[0]])
            print(f"Non-singular curve at t = {t_val}: {degenerate_curve}")

            # Compute invariants
            results.append({
                't': t_val,
                'curve': degenerate_curve,
                'genus': degenerate_curve.genus(),
                'singularities': []
            })
        except ArithmeticError:
            print(f"Curve at t = {t_val} is singular, analyzing it as a plane curve.")
            try:
                projective_ring = PolynomialRing(base_field, 'x,y,z')
                x, y, z = projective_ring.gens()
                homogenized_curve = Curve(-x^3 + x^2*z + y^2*z)
                print(f"Singular Curve at t = {t_val}: {homogenized_curve}")
                print(f"  Genus: {homogenized_curve.genus()}")
                singularities = homogenized_curve.singular_points()
                print(f"  Singularities: {singularities}")
                results.append({
                    't': t_val,
                    'curve': homogenized_curve,
                    'genus': homogenized_curve.genus(),
                    'singularities': singularities
                })
            except Exception as e:
                print(f"Error analyzing singular curve at t = {t_val}: {e}")

    return results

# Example: Exotic field extensions
def analyze_exotic_fields():
    fields = [QQ, NumberField(x^2 - 2, 'sqrt2')]
    for field in fields:
        print(f"\nAnalysis over {field}:")
        analyze_elliptic_curve(field)
        analyze_degenerate_family(field)

# Run analysis
analyze_exotic_fields()
