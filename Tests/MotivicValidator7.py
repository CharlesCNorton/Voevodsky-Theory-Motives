import numpy as np
from ripser import ripser
from persim import plot_diagrams, bottleneck
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler

def generate_motivic_sample_space(dimension, n_points=1000, structure_type='standard'):
    if structure_type == 'standard':
        points = np.random.normal(0, 1, (n_points, dimension))
    elif structure_type == 'kummer':
        base_points = np.random.normal(0, 1, (n_points // 2, dimension))
        rotated_points = np.roll(base_points, 1, axis=1)
        points = np.vstack([base_points, rotated_points])
    elif structure_type == 'artin_schreier':
        p = 5
        base_points = np.random.normal(0, 1, (n_points // p, dimension))
        points = np.vstack([base_points + i for i in range(p)])

    points = StandardScaler().fit_transform(points)
    return points

def compute_persistence_with_stability(points, max_diameter=2.0):
    distance_matrix = squareform(pdist(points))
    distance_matrix[distance_matrix > max_diameter] = max_diameter
    diagrams = ripser(distance_matrix, distance_matrix=True, thresh=max_diameter)['dgms']

    noise = np.random.normal(0, 0.01, points.shape)
    noisy_points = points + noise
    noisy_distance_matrix = squareform(pdist(noisy_points))
    noisy_distance_matrix[noisy_distance_matrix > max_diameter] = max_diameter
    noisy_diagrams = ripser(noisy_distance_matrix, distance_matrix=True, thresh=max_diameter)['dgms']

    return diagrams, noisy_diagrams

def filter_infinite_persistence(diagram):
    """Filter out points with infinite persistence."""
    if len(diagram) == 0:
        return diagram
    finite_mask = ~np.isinf(diagram[:, 1])
    return diagram[finite_mask]

def analyze_stability_metrics(diagrams, noisy_diagrams):
    stability_metrics = {}

    for i in range(len(diagrams)):
        if len(diagrams[i]) > 0 and len(noisy_diagrams[i]) > 0:
            # Filter infinite values before computing bottleneck distance
            filtered_dgm1 = filter_infinite_persistence(diagrams[i])
            filtered_dgm2 = filter_infinite_persistence(noisy_diagrams[i])

            if len(filtered_dgm1) > 0 and len(filtered_dgm2) > 0:
                try:
                    dist = bottleneck(filtered_dgm1, filtered_dgm2)
                    stability_metrics[f'dim_{i}_stability'] = dist
                except Exception as e:
                    print(f"Warning: Could not compute bottleneck distance for dimension {i}: {e}")
                    stability_metrics[f'dim_{i}_stability'] = np.nan

    return stability_metrics

def compute_persistence_statistics(diagram):
    """Compute statistical measures of persistence diagram, handling infinite values."""
    filtered_diagram = filter_infinite_persistence(diagram)

    if len(filtered_diagram) == 0:
        return {
            'mean_persistence': 0,
            'max_persistence': 0,
            'persistence_ratio': 0,
            'n_points': len(diagram),
            'n_infinite': len(diagram) - len(filtered_diagram)
        }

    persistences = filtered_diagram[:, 1] - filtered_diagram[:, 0]
    return {
        'mean_persistence': np.mean(persistences),
        'max_persistence': np.max(persistences),
        'persistence_ratio': np.mean(persistences) / np.max(persistences) if np.max(persistences) > 0 else 0,
        'n_points': len(diagram),
        'n_infinite': len(diagram) - len(filtered_diagram)
    }

def verify_motivic_claims(dimensions=[3, 5, 7], structure_types=['standard', 'kummer', 'artin_schreier']):
    results = {}

    for structure in structure_types:
        results[structure] = {}
        print(f"\nAnalyzing {structure} structure:")

        for dim in dimensions:
            print(f"\nDimension {dim}:")
            points = generate_motivic_sample_space(dim, structure_type=structure)
            diagrams, noisy_diagrams = compute_persistence_with_stability(points)

            # Compute metrics
            stability_metrics = analyze_stability_metrics(diagrams, noisy_diagrams)
            persistence_stats = [compute_persistence_statistics(dgm) for dgm in diagrams]

            # Store results
            results[structure][dim] = {
                'betti_numbers': [len(dgm) for dgm in diagrams],
                'stability_metrics': stability_metrics,
                'persistence_statistics': persistence_stats
            }

            # Print results
            print(f"Betti numbers: {results[structure][dim]['betti_numbers']}")
            print(f"Stability metrics: {stability_metrics}")
            for i, stats in enumerate(persistence_stats):
                print(f"Dimension {i} persistence statistics:")
                for key, value in stats.items():
                    if isinstance(value, float):
                        print(f"  {key}: {value:.4f}")
                    else:
                        print(f"  {key}: {value}")

            # Visualize
            plt.figure(figsize=(12, 4))

            plt.subplot(131)
            plot_diagrams(diagrams, show=False)
            plt.title(f"{structure}\nDim {dim} - Original")

            plt.subplot(132)
            plot_diagrams(noisy_diagrams, show=False)
            plt.title("Perturbed")

            # Add persistence length histogram for finite values only
            plt.subplot(133)
            for i, dgm in enumerate(diagrams):
                filtered_dgm = filter_infinite_persistence(dgm)
                if len(filtered_dgm) > 0:
                    persistences = filtered_dgm[:, 1] - filtered_dgm[:, 0]
                    plt.hist(persistences, bins=30, alpha=0.5, label=f'Dim {i}')
            plt.title("Finite Persistence Lengths")
            plt.legend()

            plt.tight_layout()
            plt.show()

    return results

if __name__ == "__main__":
    results = verify_motivic_claims()

    print("\nStability Analysis Summary:")
    for structure in results:
        print(f"\n{structure} structure:")
        for dim in results[structure]:
            metrics = results[structure][dim]['stability_metrics']
            stats = results[structure][dim]['persistence_statistics']
            print(f"\nDimension {dim}:")
            if len(metrics) > 0:
                print(f"Average stability: {np.mean(list(metrics.values())):.4f}")
            print("Persistence statistics:")
            for i, stat in enumerate(stats):
                print(f"  Dimension {i}:")
                for key, value in stat.items():
                    if isinstance(value, float):
                        print(f"    {key}: {value:.4f}")
                    else:
                        print(f"    {key}: {value}")
