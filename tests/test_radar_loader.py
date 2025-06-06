from app.services.radar_loader import load_radar_schema

def test_radar_yaml_valid():
    schema = load_radar_schema()
    assert "Striker" in schema
    assert len(schema["Striker"]) == 8
