import numpy as np, time
from multiprocessing import Pool

_udp = None
def _nis():
    global _udp
    from morphing_udp import morphing_rover_UDP
    _udp = morphing_rover_UDP()

def _nota(x):
    return _udp.fitness(x)[0]

class Vleresuesi:
    """Vlereson disa rovera njekohesisht ne CPU dhe i numeron vleresimet."""
    def __init__(self, procese=4):
        _nis()
        self.lb, self.ub = map(np.array, _udp.get_bounds())
        self.pool = Pool(procese, initializer=_nis)
        self.vleresime = 0
    def __call__(self, rovera):
        self.vleresime += len(rovera)
        return self.pool.map(_nota, rovera)

def _ndrysho(v, x, sigma, rng):
    y = x.copy()
    y[:-7] = np.clip(x[:-7] + sigma * rng.standard_normal(len(x) - 7), v.lb[:-7], v.ub[:-7])
    return y

def random_search(v, x0, buxheti, seed=0):
    rng = np.random.default_rng(seed)
    x_best, f_best = x0, v([x0])[0]
    historia = [(v.vleresime, f_best)]
    while v.vleresime < buxheti:
        X = []
        for _ in range(4):
            y = x0.copy()
            y[:-7] = rng.uniform(v.lb[:-7], v.ub[:-7])
            X.append(y)
        for x, f in zip(X, v(X)):
            if f < f_best: x_best, f_best = x, f
        historia.append((v.vleresime, f_best))
    return x_best, f_best, historia

def hill_climbing(v, x0, buxheti, sigma=0.02, seed=0):
    rng = np.random.default_rng(seed)
    x_best, f_best = x0, v([x0])[0]
    historia = [(v.vleresime, f_best)]
    while v.vleresime < buxheti:
        X = [_ndrysho(v, x_best, sigma, rng) for _ in range(4)]
        F = v(X)
        i = int(np.argmin(F))
        if F[i] < f_best: x_best, f_best = X[i], F[i]
        historia.append((v.vleresime, f_best))
    return x_best, f_best, historia

def algoritmi_gjenetik(v, x0, buxheti, pop=8, sigma=0.02, seed=0):
    rng = np.random.default_rng(seed)
    P = [x0] + [_ndrysho(v, x0, sigma, rng) for _ in range(pop - 1)]
    F = v(P)
    historia = [(v.vleresime, min(F))]
    while v.vleresime < buxheti:
        rend = np.argsort(F)
        prinderit = [P[i] for i in rend[:pop // 2]]
        femijet = []
        for _ in range(pop - 1):
            a, b = rng.choice(len(prinderit), 2, replace=False)
            maska = rng.random(len(x0)) < 0.5
            femijet.append(_ndrysho(v, np.where(maska, prinderit[a], prinderit[b]), sigma, rng))
        P = [P[rend[0]]] + femijet          # elitizmi: me i miri mbetet
        F = [F[rend[0]]] + v(femijet)
        historia.append((v.vleresime, min(F)))
    i = int(np.argmin(F))
    return P[i], F[i], historia

def cmaes(v, x0, buxheti, sigma=0.02, pop=8, seed=0):
    import cma
    n = len(x0) - 7
    def rover(z):
        return np.concatenate([np.clip(z, v.lb[:n], v.ub[:n]), x0[-7:]])
    es = cma.CMAEvolutionStrategy(x0[:n], sigma,
            {"CMA_diagonal": True, "popsize": pop, "seed": seed + 1, "verbose": -9})
    x_best, f_best = x0, v([x0])[0]
    historia = [(v.vleresime, f_best)]
    while v.vleresime < buxheti:
        Z = es.ask()
        F = v([rover(z) for z in Z])
        es.tell(Z, F)
        i = int(np.argmin(F))
        if F[i] < f_best: x_best, f_best = rover(Z[i]), F[i]
        historia.append((v.vleresime, f_best))
    return x_best, f_best, historia
