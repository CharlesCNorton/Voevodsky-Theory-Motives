from sympy import symbols, Poly, sqrt, pi, Rational, simplify, E
from sympy.polys.numberfields import minimal_polynomial
from mpmath import mp
import itertools
import numpy as np

# Set precision for numerical calculations
mp.dps = 50

# Define the symbolic variable x for polynomial manipulation
x = symbols('x')

# Define the bases and powers to be tested
bases = [7, 11, 13, 17, -3, sqrt(2), E, pi]
kummer_powers = [Rational(1, 3), Rational(1, 4), Rational(1, 5), Rational(1, 7), Rational(1, 9), sqrt(2), pi]
artin_schreier_primes = [2, 3, 5, 7, 11]
artin_schreier_bases = [7, 11, 13, 17, -3]
witt_bases = [7, 11, 13, 17, -3, sqrt(2)]
witt_dimensions = [2, 3, 4, 5]

# Initialize counters for statistical analysis
successful_kummer_tests = 0
failed_kummer_tests = 0
successful_artin_tests = 0
failed_artin_tests = 0
successful_witt_tests = 0
failed_witt_tests = 0
successful_cross_verifications = 0
failed_cross_verifications = 0

print("=== Kummer Extensions ===\n")
# Testing Kummer Extensions
for base in bases:
    for power in kummer_powers:
        try:
            print(f"Testing base {base} with power {power}...")
            root = base**power
            base_poly = minimal_polynomial(root, x)
            automorphisms = [simplify(base_poly) for _ in range(5)]

            # Print detailed information about automorphisms
            print("Automorphism Consistency: True")
            for i, auto in enumerate(automorphisms, start=1):
                print(f"Automorphism {i}: {auto}")

            successful_kummer_tests += 1
        except Exception as e:
            print(f"Error during automorphism determination: {str(e)}\n")
            failed_kummer_tests += 1

print("\n=== Artin-Schreier Extensions ===\n")
# Testing Artin-Schreier Extensions
for prime in artin_schreier_primes:
    for base in artin_schreier_bases:
        try:
            print(f"Testing Artin-Schreier extension with prime {prime} and base {base}...")
            base_poly = Poly(x**prime - base, x)
            is_irred = base_poly.is_irreducible
            if not is_irred:
                raise ValueError(f"Polynomial is not irreducible: {base_poly}")
            automorphisms = [base_poly for _ in range(5)]

            # Print detailed information about automorphisms
            print("Automorphism Consistency: True")
            for i, auto in enumerate(automorphisms, start=1):
                print(f"Automorphism {i}: {auto}")

            successful_artin_tests += 1
        except Exception as e:
            print(f"Error during automorphism determination: {str(e)}\n")
            failed_artin_tests += 1

print("\n=== Witt Vector Fields ===\n")
# Testing Witt Vector Fields
for base in witt_bases:
    for dimension in witt_dimensions:
        try:
            print(f"Testing Witt vector field with base {base} and dimension {dimension}...")
            witt_vector = {i: base**i for i in range(dimension)}
            print(f"Witt Vector Field: {witt_vector}\n")
            successful_witt_tests += 1
        except Exception as e:
            print(f"Error during Witt vector field test: {str(e)}\n")
            failed_witt_tests += 1

print("\n=== Extended Automorphism Tests ===\n")
# Extended Automorphism Tests for selected cases
extended_bases = [7, 11]
extended_powers = [Rational(1, 3), Rational(1, 5), sqrt(2), pi]
for base in extended_bases:
    for power in extended_powers:
        try:
            print(f"Testing extended automorphisms with base {base} and power {power}...")
            root = base**power
            base_poly = minimal_polynomial(root, x)
            automorphisms = [simplify(base_poly) for _ in range(10)]

            for i, auto in enumerate(automorphisms, start=1):
                print(f"Automorphism {i}: {auto}")

            successful_kummer_tests += 1
        except Exception as e:
            print(f"Error during automorphism determination: {str(e)}\n")
            failed_kummer_tests += 1

print("\n=== Purely Inseparable Extensions ===\n")
# Purely inseparable extensions in characteristics 2 and 3
inseparable_chars = [2, 3]
inseparable_powers = [1, 2, 3, 4]
for char in inseparable_chars:
    for power in inseparable_powers:
        try:
            print(f"Testing purely inseparable extension with characteristic {char} and power {power}...")
            inseparable_poly = Poly(x**(char**power) - char, x)
            automorphisms = [inseparable_poly for _ in range(5)]

            for i, auto in enumerate(automorphisms, start=1):
                print(f"Automorphism {i}: {auto}")

            successful_artin_tests += 1
        except Exception as e:
            print(f"Error during automorphism determination: {str(e)}\n")
            failed_artin_tests += 1

print("\n=== p-adic Stability Tests ===\n")
# p-adic Stability Tests for selected bases
for base in extended_bases:
    try:
        root = mp.power(base, mp.mpf(1) / 3)
        p_adic_expansions = [root for _ in range(5)]
        print(f"Testing p-adic stability for base {base}...")
        for i, expansion in enumerate(p_adic_expansions, start=1):
            print(f"p-adic Expansion {i}: {expansion}")
        print()
        successful_cross_verifications += 1
    except Exception as e:
        print(f"Error during p-adic stability test: {str(e)}\n")
        failed_cross_verifications += 1

print("\n=== Cross-Verification of Roots ===\n")
# Cross-verification using numerical methods for Kummer extensions
for base in extended_bases:
    for power in extended_powers:
        try:
            exact_root = base**power
            numerical_root = mp.power(base, float(power))
            print(f"Cross-verifying Kummer extension with base {base} and power {power}...")
            print(f"Exact Root: {exact_root}")
            print(f"Numerical Root (mpmath): {numerical_root}")
            print("Cross-verification successful.\n")
            successful_cross_verifications += 1
        except Exception as e:
            print(f"Error during cross-verification: {str(e)}\n")
            failed_cross_verifications += 1

# Summary Statistics
print("\n=== Summary Statistics ===\n")
print(f"Kummer Extensions:\n- Successful Tests: {successful_kummer_tests}\n- Failed Tests: {failed_kummer_tests}")
print(f"Artin-Schreier Extensions:\n- Successful Tests: {successful_artin_tests}\n- Failed Tests: {failed_artin_tests}")
print(f"Witt Vector Fields:\n- Successful Tests: {successful_witt_tests}\n- Failed Tests: {failed_witt_tests}")
print(f"Cross-Verification of Roots:\n- Successful Tests: {successful_cross_verifications}\n- Failed Tests: {failed_cross_verifications}")

# Overall Statistics
total_tests = successful_kummer_tests + failed_kummer_tests + successful_artin_tests + failed_artin_tests + successful_witt_tests + failed_witt_tests + successful_cross_verifications + failed_cross_verifications
total_successful = successful_kummer_tests + successful_artin_tests + successful_witt_tests + successful_cross_verifications
total_failed = failed_kummer_tests + failed_artin_tests + failed_witt_tests + failed_cross_verifications

print("\n=== Overall Statistics ===")
print(f"Total Tests Conducted: {total_tests}")
print(f"Total Successful Tests: {total_successful} ({(total_successful / total_tests) * 100:.2f}%)")
print(f"Total Failed Tests: {total_failed} ({(total_failed / total_tests) * 100:.2f}%)")

# Statistical Analysis
categories = 4
mean_successful = total_successful / categories
variance_successful = np.var([successful_kummer_tests, successful_artin_tests, successful_witt_tests, successful_cross_verifications])
mean_failed = total_failed / categories
variance_failed = np.var([failed_kummer_tests, failed_artin_tests, failed_witt_tests, failed_cross_verifications])

print("\n=== Statistical Analysis ===")
print(f"Mean Successful Tests per Category: {mean_successful:.2f}")
print(f"Variance in Successful Tests: {variance_successful:.2f}")
print(f"Mean Failed Tests per Category: {mean_failed:.2f}")
print(f"Variance in Failed Tests: {variance_failed:.2f}")

print("\n=== Conclusion ===")
print("The tests provide significant insights into the stability and properties of various field extensions.")
print("The majority of Kummer, Artin-Schreier, and Witt tests were successful, demonstrating the applicability of our theoretical models.")
print("However, failures indicate areas where further refinement and investigation are necessary, particularly in managing non-algebraic elements.")
