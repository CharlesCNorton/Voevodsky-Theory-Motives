import numpy as np
from ripser import ripser
from sklearn.preprocessing import StandardScaler
from persim import bottleneck
from scipy.stats import ks_2samp
from itertools import combinations

def generate_algebraic_controls(dimension, n_points=1000):
    """Generate control spaces based on algebraic varieties."""
    t = np.linspace(0, 2 * np.pi, n_points)
    a, b = 2, 3
    x = t
    y = np.sqrt(x**3 + a * x + b + 1e-10)
    elliptic = np.column_stack([x, y])
    if dimension > 2:
        elliptic = np.hstack([elliptic, np.zeros((n_points, dimension - 2))])

    u = np.linspace(-1, 1, int(np.sqrt(n_points)))
    v = np.linspace(-1, 1, int(np.sqrt(n_points)))
    U, V = np.meshgrid(u, v)
    U, V = U.flatten(), V.flatten()
    W = U**4 + V**4 - 1
    k3 = np.column_stack([U, V, W])
    if dimension > 3:
        k3 = np.hstack([k3, np.zeros((len(U), dimension - 3))])

    basis = np.random.normal(0, 1, (dimension, 2))
    Q, _ = np.linalg.qr(basis)
    grass_points = []
    for _ in range(n_points):
        theta = np.random.uniform(0, 2 * np.pi)
        point = Q @ np.array([[np.cos(theta)], [np.sin(theta)]])
        grass_points.append(point.flatten())
    grassmannian = np.array(grass_points)

    return {
        'elliptic': StandardScaler().fit_transform(elliptic),
        'k3': StandardScaler().fit_transform(k3),
        'grassmannian': StandardScaler().fit_transform(grassmannian)
    }

def wild_field_action(points, p=5):
    """Simulate wild ramification."""
    base = points.copy()
    for _ in range(p):
        frob = np.clip(np.power(base, p) - base, -1e6, 1e6) / (p + 1e-10)
        base += frob
        if np.isnan(base).any() or np.isinf(base).any():
            raise ValueError("Invalid values encountered in wild field action.")
    return base

def create_singularity(points, sing_type):
    """Apply specific singularities."""
    if sing_type == 'node':
        return np.abs(points) * np.sign(points)
    elif sing_type == 'cusp':
        return np.sign(points) * np.power(np.abs(points), 2/3)
    elif sing_type == 'log':
        return np.log(np.abs(points) + 1) * np.sign(points)
    return points

def matrix_action(points, dim):
    """Simulate non-commutative group action."""
    A = np.random.normal(0, 1, (dim, dim))
    B = np.random.normal(0, 1, (dim, dim))
    if np.allclose(A @ B, B @ A):
        B += np.eye(dim)
    return np.vstack([
        points,
        points @ A,
        points @ B,
        points @ (A @ B - B @ A)
    ])

def generate_motivic_spaces(dimension, n_points=1000, char_p=5):
    """Generate motivic spaces."""
    base_wild = np.random.normal(0, 1, (n_points // char_p, dimension))
    wild = wild_field_action(base_wild, p=char_p)

    base_combined = np.random.normal(0, 1, (n_points // 3, dimension))
    nodal = create_singularity(base_combined, 'node')
    cuspidal = create_singularity(base_combined, 'cusp')
    log_sing = create_singularity(base_combined, 'log')
    combined = np.vstack([nodal, cuspidal, log_sing])

    base_noncomm = np.random.normal(0, 1, (n_points // 4, dimension))
    noncommutative = matrix_action(base_noncomm, dimension)

    return {
        'wild': StandardScaler().fit_transform(wild),
        'combined': StandardScaler().fit_transform(combined),
        'noncommutative': StandardScaler().fit_transform(noncommutative)
    }

def compute_rigorous_metrics(diagrams1, diagrams2=None):
    """Compute persistence-related metrics."""
    metrics = {}
    for i, dgm in enumerate(diagrams1):
        finite_dgm = dgm[~np.isinf(dgm).any(axis=1)]
        if len(finite_dgm) > 0:
            pers = finite_dgm[:, 1] - finite_dgm[:, 0]
            weights = np.log(pers + 1)
            metrics[f'dim_{i}_weight_mean'] = np.mean(weights)
            metrics[f'dim_{i}_weight_std'] = np.std(weights)
            metrics[f'dim_{i}_complexity'] = len(finite_dgm) * np.mean(pers)
            metrics[f'dim_{i}_field_measure'] = np.sum(pers) / len(finite_dgm)
    if diagrams2 is not None:
        for i in range(min(len(diagrams1), len(diagrams2))):
            dgm1 = diagrams1[i][~np.isinf(diagrams1[i]).any(axis=1)]
            dgm2 = diagrams2[i][~np.isinf(diagrams2[i]).any(axis=1)]
            if len(dgm1) > 0 and len(dgm2) > 0:
                metrics[f'dim_{i}_bottleneck'] = bottleneck(dgm1, dgm2)
                pers1 = dgm1[:, 1] - dgm1[:, 0]
                pers2 = dgm2[:, 1] - dgm2[:, 0]
                weights1 = np.log(pers1 + 1)
                weights2 = np.log(pers2 + 1)
                stat, pval = ks_2samp(weights1, weights2)
                metrics[f'dim_{i}_weight_ks_stat'] = stat
                metrics[f'dim_{i}_weight_ks_pval'] = pval
                metrics[f'dim_{i}_field_diff'] = abs(
                    np.sum(pers1) / len(pers1) - np.sum(pers2) / len(pers2)
                )
    return metrics

def verify_paper_claims(dimensions=[3, 5, 7, 9, 11]):
    """Verify the paper's claims."""
    results = {}
    for dim in dimensions:
        print(f"Analyzing dimension {dim}")
        controls = generate_algebraic_controls(dim)
        motivic = generate_motivic_spaces(dim)
        results[dim] = {'controls': {}, 'motivic': {}, 'comparisons': {}}
        for name, space in controls.items():
            diagrams = ripser(space)['dgms']
            results[dim]['controls'][name] = compute_rigorous_metrics(diagrams)
        for name, space in motivic.items():
            diagrams = ripser(space)['dgms']
            results[dim]['motivic'][name] = compute_rigorous_metrics(diagrams)
        for mot_name, mot_space in motivic.items():
            mot_diagrams = ripser(mot_space)['dgms']
            for ctrl_name, ctrl_space in controls.items():
                ctrl_diagrams = ripser(ctrl_space)['dgms']
                comp_key = f"{mot_name}_vs_{ctrl_name}"
                results[dim]['comparisons'][comp_key] = compute_rigorous_metrics(
                    mot_diagrams, ctrl_diagrams
                )
    return results

if __name__ == "__main__":
    results = verify_paper_claims()
    print("\nFinal Results:")
    print(results)
