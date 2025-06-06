import yaml, pathlib

CONFIG_PATH = pathlib.Path(__file__).parents[1] / "config" / "radar_config.yml"

def load_radar_schema() -> dict[str, list[str]]:
    """Return {role: [metric1…metric8]} dict from YAML; raises if invalid."""
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for role, metrics in data.items():
        if not isinstance(metrics, list) or len(metrics) != 8:
            raise ValueError(f"Role '{role}' must have exactly 8 metrics.")
    return data
