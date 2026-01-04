import random
import time

class MockCoherenceAdapter:
    """Simulates degrading coherence over time"""
def get_beta(self):
    return 1.1

    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.start = time.time()

    def get_coherence(self):
        elapsed = time.time() - self.start

        if elapsed < 30:
            return 0.6 + self.rng.gauss(0, 0.03)
        elif elapsed < 60:
            decline = (elapsed - 30) / 30
            return 0.6 - 0.3 * decline + self.rng.gauss(0, 0.02)
        else:
            return 0.2 + self.rng.gauss(0, 0.01)

    def get_beta(self):
        return 1.1
