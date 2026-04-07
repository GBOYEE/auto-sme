# auto-sme API & CLI

## CLI

```bash
# Generate a unit
auto-sme generate -t TEMPLATE.j2 -o OUTPUT.pdf

# Validate only
auto-sme validate -t TEMPLATE.j2 -c CONTENT.yaml

# List templates
auto-sme list-templates
```

## Python API

```python
from auto_sme.pipeline import Pipeline

pipe = Pipeline(template="science_earth_water_cycle.j2")
result = pipe.run(output_path="unit.pdf")
print(f"Generated {result.pdf_path}, QA pass: {result.qa_passed}")
```

## Configuration

- `auto-sme.yaml` for default LLM settings, QA thresholds
- Environment: `OPENROUTER_API_KEY`, `OLLAMA_HOST`
