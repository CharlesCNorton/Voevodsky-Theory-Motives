import numpy as np
from ripser import ripser
from persim import plot_diagrams, bottleneck
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler

def generate_degeneration_space(dimension, n_points=1000, degeneration_type='combined'):
    """
    Generate space with specific degeneration types to test the paper's claims.

    degeneration_type options:
    - 'combined': Multiple simultaneous degenerations (logarithmic + nodal)
    - 'wild_ramification': Simulates wild ramification in characteristic p
    - 'noncommutative': Simulates non-commutative structure
    """
    if degeneration_type == 'combined':
        # Simulate combined logarithmic and nodal degenerations
        base_points = np.random.normal(0, 1, (n_points // 2, dimension))
        log_component = np.exp(base_points)  # Logarithmic degeneration
        nodal_component = np.where(base_points > 0, base_points, -base_points)  # Nodal
        points = np.vstack([log_component, nodal_component])

    elif degeneration_type == 'wild_ramification':
        # Simulate wild ramification in char p
        p = 5  # characteristic
        base_points = np.random.normal(0, 1, (n_points // p, dimension))
        points = np.vstack([base_points + i/p + (i/p)**p for i in range(p)])

    elif degeneration_type == 'noncommutative':
        # Simulate non-commutative structure via matrix operations
        base_points = np.random.normal(0, 1, (n_points // 2, dimension))
        rotated = np.roll(base_points, 1, axis=1)  # Non-commutative action
        points = np.vstack([base_points, rotated])

    return StandardScaler().fit_transform(points)

def analyze_stability_under_degeneration(diagrams1, diagrams2, max_degree=2):
    """
    Analyze stability between two persistence diagrams up to given degree.
    """
    stability_metrics = {}

    for i in range(min(len(diagrams1), len(diagrams2), max_degree + 1)):
        if len(diagrams1[i]) > 0 and len(diagrams2[i]) > 0:
            # Remove infinite values for comparison
            dgm1 = diagrams1[i][~np.isinf(diagrams1[i]).any(axis=1)]
            dgm2 = diagrams2[i][~np.isinf(diagrams2[i]).any(axis=1)]

            if len(dgm1) > 0 and len(dgm2) > 0:
                try:
                    dist = bottleneck(dgm1, dgm2)
                    stability_metrics[f'degree_{i}'] = dist
                except Exception as e:
                    print(f"Warning: Could not compute stability for degree {i}: {e}")
                    stability_metrics[f'degree_{i}'] = np.nan

    return stability_metrics

def verify_core_claims(dimensions=[3, 5, 7]):
    """
    Verify the paper's core claims about degeneration behavior.
    """
    results = {}
    degeneration_types = ['combined', 'wild_ramification', 'noncommutative']

    for deg_type in degeneration_types:
        results[deg_type] = {}
        print(f"\nTesting {deg_type} degeneration:")

        for dim in dimensions:
            print(f"\nDimension {dim}:")

            # Generate base space and degenerated space
            base_points = generate_degeneration_space(dim, degeneration_type=deg_type)

            # Compute persistence diagrams
            base_diagrams = ripser(base_points)['dgms']

            # Add small perturbation to test stability
            perturbed_points = base_points + np.random.normal(0, 0.01, base_points.shape)
            perturbed_diagrams = ripser(perturbed_points)['dgms']

            # Analyze stability
            stability = analyze_stability_under_degeneration(base_diagrams, perturbed_diagrams)

            # Store results
            results[deg_type][dim] = {
                'stability': stability,
                'betti_numbers': [len(dgm) for dgm in base_diagrams],
                'persistence_ranges': [
                    (np.min(dgm[:, 1] - dgm[:, 0]), np.max(dgm[:, 1] - dgm[:, 0]))
                    if len(dgm) > 0 else (0, 0)
                    for dgm in base_diagrams
                ]
            }

            # Print results
            print(f"Stability metrics: {stability}")
            print(f"Betti numbers: {results[deg_type][dim]['betti_numbers']}")
            print(f"Persistence ranges: {results[deg_type][dim]['persistence_ranges']}")

            # Visualize
            plt.figure(figsize=(12, 4))
            plt.subplot(131)
            plot_diagrams(base_diagrams, show=False)
            plt.title(f"{deg_type}\nDim {dim} - Original")

            plt.subplot(132)
            plot_diagrams(perturbed_diagrams, show=False)
            plt.title("Perturbed")

            plt.subplot(133)
            for i, dgm in enumerate(base_diagrams):
                if len(dgm) > 0:
                    pers = dgm[:, 1] - dgm[:, 0]
                    plt.hist(pers[~np.isinf(pers)], bins=30, alpha=0.5, label=f'Degree {i}')
            plt.title("Persistence Distribution")
            plt.legend()

            plt.tight_layout()
            plt.show()

    return results

if __name__ == "__main__":
    # Test core claims
    results = verify_core_claims()

    # Analyze results
    print("\nFinal Analysis of Core Claims:")
    degeneration_types = list(results.keys())
    dimensions = list(results[degeneration_types[0]].keys())

    for deg_type in degeneration_types:
        print(f"\n{deg_type.upper()} DEGENERATION:")
        stability_trend = [
            np.mean(list(results[deg_type][dim]['stability'].values()))
            for dim in dimensions
        ]
        print(f"Stability trend across dimensions: {stability_trend}")
        print(f"Relative stability change: {np.diff(stability_trend) / stability_trend[:-1]}")
