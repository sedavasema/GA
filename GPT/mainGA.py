import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from algorithms.nsga2_optimizer import NSGA2Optimizer, Solution


def ensure_result_dir() -> Path:
    base = Path(__file__).resolve().parent / "Result"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = base / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def write_pareto_csv(out_dir: Path, solutions: list[Solution]) -> None:
    csv_path = out_dir / "pareto_front_filtered.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("f1,f2,variables\n")
        for s in solutions:
            f1, f2 = s.objectives
            f.write(f"{f1},{f2},\"{json.dumps(s.variables)}\"\n")


def write_best_json(out_dir: Path, solutions: list[Solution]) -> None:
    # Select best by simple sum of normalized objectives as placeholder
    best = min(solutions, key=lambda s: s.objectives[0] + s.objectives[1])
    data: Dict[str, Any] = {
        "best_solution": {
            "variables": best.variables,
            "f1": best.objectives[0],
            "f2": best.objectives[1],
        },
        "count": len(solutions),
    }
    json_path = out_dir / "best_solutions.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    optimizer = NSGA2Optimizer(population_size=21, num_variables=3)
    solutions = optimizer.optimize(max_generations=5)

    out_dir = ensure_result_dir()
    write_pareto_csv(out_dir, solutions)
    write_best_json(out_dir, solutions)
    print(f"Results written to: {out_dir}")


if __name__ == "__main__":
    main()