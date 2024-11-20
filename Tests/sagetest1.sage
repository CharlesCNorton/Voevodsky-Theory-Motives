from sage.all import *

def analyze_affine_patch(F, patch_name, coords, P3):
    """
    Analyze singularities on a single affine patch of the projective space P3.
    """
    try:
        # Replace projective coordinates with affine ones
        substitutions = {P3.gen(i): coords[i] for i in range(len(coords))}
        affine_F = F.subs(substitutions)

        # Clear denominators and simplify
        affine_numerator = affine_F.numerator()
        affine_denominator = affine_F.denominator()

        if affine_denominator != 1:
            affine_numerator *= affine_denominator  # Clear denominators explicitly

        # Define an affine polynomial ring
        affine_ring = PolynomialRing(QQ, names="u,v,w")
        u, v, w = affine_ring.gens()

        # Map variables explicitly to the affine ring
        mapped_vars = {
            P3.gen(0): 1,
            P3.gen(1): u,
            P3.gen(2): v,
            P3.gen(3): w,
        }
        mapped_F = affine_numerator.subs(mapped_vars)

        # Map explicitly to the affine polynomial ring
        affine_polynomial = affine_ring(mapped_F)

        print(f"DEBUG ({patch_name}): Mapped polynomial: {affine_polynomial}")

        # Compute the partial derivatives
        partials = [affine_polynomial.derivative(var) for var in affine_ring.gens()]
        print(f"DEBUG ({patch_name}): Partial derivatives: {partials}")

        # Construct the Jacobian ideal
        jacobian_ideal = affine_ring.ideal(partials + [affine_polynomial])
        print(f"DEBUG ({patch_name}): Jacobian ideal: {jacobian_ideal}")

        # Compute the dimension of the singular locus
        singular_dim = jacobian_ideal.dimension()
        return singular_dim
    except Exception as e:
        return f"Error: {e}"

def analyze_affine_patches(F, P3):
    """
    Analyze singularities of F on all affine patches of the projective space P3.
    """
    patches = {
        "x != 0": [1, P3.gen(1)/P3.gen(0), P3.gen(2)/P3.gen(0), P3.gen(3)/P3.gen(0)],
        "y != 0": [P3.gen(0)/P3.gen(1), 1, P3.gen(2)/P3.gen(1), P3.gen(3)/P3.gen(1)],
        "z != 0": [P3.gen(0)/P3.gen(2), P3.gen(1)/P3.gen(2), 1, P3.gen(3)/P3.gen(2)],
        "w != 0": [P3.gen(0)/P3.gen(3), P3.gen(1)/P3.gen(3), P3.gen(2)/P3.gen(3), 1],
    }
    affine_results = []
    for patch_name, coords in patches.items():
        singular_dim = analyze_affine_patch(F, patch_name, coords, P3)
        affine_results.append((patch_name, singular_dim))
    return affine_results

def analyze_hypersurface(F, P3):
    """
    Analyze the hypersurface defined by F in the projective space P3.
    """
    try:
        # Compute Jacobian partial derivatives
        partials = [F.derivative(var) for var in P3.gens()]
        print(f"DEBUG: Partial derivatives in projective space: {partials}")

        # Construct the Jacobian ideal
        jacobian_ideal = P3.coordinate_ring().ideal(partials + [F])
        print(f"DEBUG: Jacobian ideal in projective space: {jacobian_ideal}")

        # Attempt to compute the singular locus dimension
        singular_dim = jacobian_ideal.dimension()
        print(f"Singular Locus in Projective Space: Dimension = {singular_dim}")
    except Exception as e:
        print(f"Singular Locus in Projective Space: Dimension = Error: {e}")
    
    try:
        # Analyze singularities on affine patches
        affine_singularities = analyze_affine_patches(F, P3)
        print(f"Affine Patch Analysis:")
        for patch, dim in affine_singularities:
            print(f"  {patch}: Singular Locus Dimension = {dim}")
    except Exception as e:
        print(f"Error analyzing affine patches: {e}")

def main():
    """
    Main function to define hypersurfaces and analyze them.
    """
    # Define projective space and polynomial ring
    P3 = ProjectiveSpace(3, QQ, names="x,y,z,w")
    x, y, z, w = P3.gens()
    
    # Define a family of hypersurfaces
    t_values = [1/i for i in range(1, 11)] + [0]
    for t in t_values:
        print(f"\nProcessing hypersurface with t = {t}...")
        try:
            # Define the hypersurface equation
            F = 3*x^3 + 3*y^3 + 3*z^3 + 3*w^3 + t*x*y*z*w
            print(f"DEBUG: Hypersurface equation: {F}")
            
            # Analyze the hypersurface
            analyze_hypersurface(F, P3)
        except Exception as e:
            print(f"Error processing hypersurface for t = {t}: {e}")

# Run the main function
main()
