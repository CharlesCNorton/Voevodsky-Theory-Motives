import numpy as np
from ripser import ripser
from persim import plot_diagrams, bottleneck
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from scipy.stats import wasserstein_distance

def generate_advanced_degeneration_space(dimension, n_points=1000, degeneration_type='wild', p_char=5):
    """
    Enhanced degeneration space generator with more sophisticated modeling.
    """
    if degeneration_type == 'wild':
        # Enhanced wild ramification simulation
        base_points = np.random.normal(0, 1, (n_points // p_char, dimension))
        # Model Artin-Schreier-Witt extensions
        witt_vectors = [base_points + (i/p_char) + (i/p_char)**p_char for i in range(p_char)]
        # Add higher-order terms
        higher_order = [(i/p_char)**(p_char + 1) for i in range(p_char)]
        points = np.vstack([w + h for w, h in zip(witt_vectors, higher_order)])

    elif degeneration_type == 'combined':
        # Enhanced combined degeneration
        base_points = np.random.normal(0, 1, (n_points // 3, dimension))
        log_component = np.exp(base_points)  # Logarithmic
        nodal_component = np.where(base_points > 0, base_points, -base_points)  # Nodal
        # Add cusps
        cusp_component = np.sign(base_points) * np.abs(base_points)**(2/3)
        points = np.vstack([log_component, nodal_component, cusp_component])

    elif degeneration_type == 'noncommutative':
        # Enhanced non-commutative structure
        base_points = np.random.normal(0, 1, (n_points // 3, dimension))
        # Simulate matrix algebra actions
        rot_1 = np.roll(base_points, 1, axis=1)
        rot_2 = np.roll(base_points, 2, axis=1)
        # Add non-trivial braiding
        braid = rot_1 + np.roll(rot_2, 1, axis=0)
        points = np.vstack([base_points, rot_1, braid])

    return StandardScaler().fit_transform(points)

def analyze_advanced_stability(diagrams1, diagrams2, max_degree=3):
    """
    Enhanced stability analysis using multiple metrics.
    """
    metrics = {}

    for i in range(min(len(diagrams1), len(diagrams2), max_degree + 1)):
        if len(diagrams1[i]) > 0 and len(diagrams2[i]) > 0:
            # Clean infinite values
            dgm1 = diagrams1[i][~np.isinf(diagrams1[i]).any(axis=1)]
            dgm2 = diagrams2[i][~np.isinf(diagrams2[i]).any(axis=1)]

            if len(dgm1) > 0 and len(dgm2) > 0:
                try:
                    # Bottleneck distance
                    metrics[f'bottleneck_deg_{i}'] = bottleneck(dgm1, dgm2)

                    # Wasserstein distance on persistence
                    pers1 = dgm1[:, 1] - dgm1[:, 0]
                    pers2 = dgm2[:, 1] - dgm2[:, 0]
                    metrics[f'wasserstein_deg_{i}'] = wasserstein_distance(pers1, pers2)

                    # Persistence ratio stability
                    ratio1 = np.mean(pers1) / np.max(pers1) if len(pers1) > 0 else 0
                    ratio2 = np.mean(pers2) / np.max(pers2) if len(pers2) > 0 else 0
                    metrics[f'ratio_stability_deg_{i}'] = abs(ratio1 - ratio2)

                except Exception as e:
                    print(f"Warning: Metric computation failed for degree {i}: {e}")

    return metrics

def examine_higher_dimensions(dimensions=[3, 5, 7, 9, 11], degeneration_types=['wild', 'combined', 'noncommutative']):
    """
    Examine behavior in higher dimensions with detailed analysis.
    """
    results = {}

    for deg_type in degeneration_types:
        results[deg_type] = {}
        print(f"\nAnalyzing {deg_type} degeneration across dimensions:")

        for dim in dimensions:
            print(f"\nDimension {dim}:")

            # Generate spaces
            base_points = generate_advanced_degeneration_space(dim, degeneration_type=deg_type)
            perturbed_points = base_points + np.random.normal(0, 0.01, base_points.shape)

            # Compute persistence
            base_diagrams = ripser(base_points)['dgms']
            perturbed_diagrams = ripser(perturbed_points)['dgms']

            # Advanced stability analysis
            stability = analyze_advanced_stability(base_diagrams, perturbed_diagrams)

            # Store results
            results[deg_type][dim] = {
                'stability_metrics': stability,
                'betti_numbers': [len(dgm) for dgm in base_diagrams],
                'persistence_statistics': [
                    {
                        'mean': np.mean(dgm[:, 1] - dgm[:, 0]) if len(dgm) > 0 else 0,
                        'max': np.max(dgm[:, 1] - dgm[:, 0]) if len(dgm) > 0 else 0,
                        'variance': np.var(dgm[:, 1] - dgm[:, 0]) if len(dgm) > 0 else 0
                    }
                    for dgm in base_diagrams
                ]
            }

            # Print detailed results
            print(f"Stability metrics: {stability}")
            print(f"Betti numbers: {results[deg_type][dim]['betti_numbers']}")

            # Visualize
            plt.figure(figsize=(15, 5))

            plt.subplot(131)
            plot_diagrams(base_diagrams, show=False)
            plt.title(f"{deg_type}\nDim {dim} - Original")

            plt.subplot(132)
            for i, dgm in enumerate(base_diagrams):
                if len(dgm) > 0:
                    pers = dgm[:, 1] - dgm[:, 0]
                    plt.hist(pers[~np.isinf(pers)], bins=30, alpha=0.5, label=f'Degree {i}')
            plt.title("Persistence Distribution")
            plt.legend()

            plt.subplot(133)
            # Plot stability trends
            degrees = range(min(3, len(base_diagrams)))
            if stability:
                bottleneck_values = [stability.get(f'bottleneck_deg_{i}', np.nan) for i in degrees]
                plt.plot(degrees, bottleneck_values, 'o-', label='Bottleneck')
                wasserstein_values = [stability.get(f'wasserstein_deg_{i}', np.nan) for i in degrees]
                plt.plot(degrees, wasserstein_values, 's-', label='Wasserstein')
            plt.title("Stability Metrics vs Degree")
            plt.legend()

            plt.tight_layout()
            plt.show()

    return results

if __name__ == "__main__":
    # Run enhanced analysis
    results = examine_higher_dimensions()

    # Final analysis
    print("\nComprehensive Analysis of Results:")
    for deg_type in results:
        print(f"\n{deg_type.upper()} DEGENERATION:")

        # Analyze stability trends
        dimensions = sorted(results[deg_type].keys())
        bottleneck_trends = [
            np.mean([v for k, v in results[deg_type][dim]['stability_metrics'].items()
                    if 'bottleneck' in k])
            for dim in dimensions
        ]
        print(f"Bottleneck stability trend: {bottleneck_trends}")
        print(f"Relative stability changes: {np.diff(bottleneck_trends) / bottleneck_trends[:-1]}")

        # Analyze Betti number growth
        betti_growth = [results[deg_type][dim]['betti_numbers'][1] /
                       results[deg_type][dim]['betti_numbers'][0]
                       for dim in dimensions]
        print(f"Betti number growth ratios: {betti_growth}")

        # Analyze persistence statistics
        persistence_trends = [
            results[deg_type][dim]['persistence_statistics'][1]['mean']
            for dim in dimensions
        ]
        print(f"Mean persistence trends: {persistence_trends}")# Write your code here :-)
