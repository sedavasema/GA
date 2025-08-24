import random
import math
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Solution:
    variables: List[float]
    objectives: Tuple[float, float]


class NSGA2Optimizer:
    def __init__(self, population_size: int = 20, num_variables: int = 3, seed: int | None = 42) -> None:
        self.population_size = population_size
        self.num_variables = num_variables
        if seed is not None:
            random.seed(seed)

    def evaluate_objectives(self, variables: List[float]) -> Tuple[float, float]:
        # Dummy bi-objective: f1=sum(x^2), f2=sum((x-1)^2)
        f1 = sum(v * v for v in variables)
        f2 = sum((v - 1.0) * (v - 1.0) for v in variables)
        return (f1, f2)

    def optimize(self, max_generations: int = 10) -> List[Solution]:
        # Produce a simple trade-off front along a line between 0 and 1 in each variable
        pareto_solutions: List[Solution] = []
        for alpha in [i / (self.population_size - 1) for i in range(self.population_size)]:
            variables = [alpha for _ in range(self.num_variables)]
            objectives = self.evaluate_objectives(variables)
            pareto_solutions.append(Solution(variables=variables, objectives=objectives))
        return pareto_solutions