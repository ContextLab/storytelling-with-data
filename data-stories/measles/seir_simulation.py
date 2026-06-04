"""
Neighbor-based SEIR outbreak simulation on a 10x10 grid.

Matches the parameters documented in the companion measles_sim.html visualization:
- 100 people arranged on a 10x10 grid
- Moore neighborhood (up to 8 neighbors)
- Latent period: 10 days; infectious period: 8 days
- MMR vaccine efficacy: 97%
- 3 unvaccinable individuals (newborns / immunocompromised) per run

The HTML visualization plays back a single canned run for each state. This module lets
us run the same model thousands of times to characterize the *distribution* of
outbreak outcomes rather than relying on a single illustrative example.

R0 caveat: the HTML labels the model as "R0=15", but with at most 8 neighbors per
agent and a finite infectious window, R0=15 cannot be realized as a per-neighbor
transmission probability on this grid. In practice the per-day-per-neighbor
infection probability saturates well below 1 and the dynamics are dominated by
network structure (who has a susceptible neighbor) rather than transmissibility.
We use P_INFECT = 0.9 per susceptible neighbor per day; results are insensitive
to this once it is sufficiently large.
"""
import numpy as np

# --- Model parameters ---------------------------------------------------------
GRID = 10
N = GRID * GRID
LATENT_DAYS = 10
INFECTIOUS_DAYS = 8
VACCINE_EFFICACY = 0.97
N_UNVACCINABLE = 3
MAX_DAYS = 120
P_INFECT = 0.9   # per susceptible neighbor per day during the infectious period

# Compartment codes
S, E, I, R = 0, 1, 2, 3


def _moore_neighbors(idx):
    """Up to 8 neighbor indices for a flat-index grid position."""
    r, c = divmod(idx, GRID)
    out = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if 0 <= rr < GRID and 0 <= cc < GRID:
                out.append(rr * GRID + cc)
    return out


# Precompute neighbor lists (same for every run)
_NEIGHBORS = [_moore_neighbors(i) for i in range(N)]


def run_one(coverage, rng):
    """Run a single outbreak and return summary statistics.

    Args:
        coverage: fraction of the (non-unvaccinable) population that is vaccinated.
        rng: a numpy Generator.

    Returns:
        dict with keys: total_infected, vulnerable_infected, days_until_done.
    """
    state = np.full(N, S, dtype=np.int8)
    days_in_state = np.zeros(N, dtype=np.int16)

    # Randomly place the 3 unvaccinable people
    perm = rng.permutation(N)
    unvaccinable = set(perm[:N_UNVACCINABLE].tolist())

    # Of the rest, `coverage` fraction get vaccinated;
    # of those vaccinated, VACCINE_EFFICACY become immune (move to R)
    eligible = [i for i in range(N) if i not in unvaccinable]
    n_vacc = int(round(coverage * len(eligible)))
    vacc_order = rng.permutation(eligible)
    for v in vacc_order[:n_vacc]:
        if rng.random() < VACCINE_EFFICACY:
            state[v] = R

    # Patient zero: a random susceptible person
    susceptibles = np.where(state == S)[0]
    if len(susceptibles) == 0:
        return {"total_infected": 0, "vulnerable_infected": 0, "days_until_done": 0}
    patient_zero = rng.choice(susceptibles)
    state[patient_zero] = E
    infected_ever = {int(patient_zero)}

    last_day = 0
    for day in range(1, MAX_DAYS + 1):
        last_day = day
        new_state = state.copy()
        new_days = days_in_state + 1

        # E -> I after latent period
        for i in np.where(state == E)[0]:
            if days_in_state[i] >= LATENT_DAYS:
                new_state[i] = I
                new_days[i] = 0

        # I -> R after infectious period
        for i in np.where(state == I)[0]:
            if days_in_state[i] >= INFECTIOUS_DAYS:
                new_state[i] = R
                new_days[i] = 0

        # Transmission: each currently-infectious agent attempts to infect each susceptible neighbor
        for i in np.where(state == I)[0]:
            for nb in _NEIGHBORS[i]:
                if new_state[nb] == S and rng.random() < P_INFECT:
                    new_state[nb] = E
                    new_days[nb] = 0
                    infected_ever.add(int(nb))

        state = new_state
        days_in_state = new_days

        # Done when no exposed or infectious individuals remain
        if not np.any((state == E) | (state == I)):
            break

    vulnerable_infected = len(infected_ever & unvaccinable)
    return {
        "total_infected": len(infected_ever),
        "vulnerable_infected": vulnerable_infected,
        "days_until_done": last_day,
    }


def run_many(coverage, n_runs, seed=0):
    """Run many outbreaks and return arrays of total / vulnerable infections per run."""
    rng = np.random.default_rng(seed)
    results = [run_one(coverage, rng) for _ in range(n_runs)]
    totals = np.array([r["total_infected"] for r in results])
    vulns = np.array([r["vulnerable_infected"] for r in results])
    return totals, vulns
