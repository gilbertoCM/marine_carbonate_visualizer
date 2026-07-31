# Tests for Marine Carbonate System

Comprehensive test suite verifying the consistency of carbonate chemistry calculations (TA, DIC, pH, pCO₂).

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=carbonate_system --cov-report=html

# Run specific test class
pytest tests/test_carbonate_system.py::TestConsistency -v
```

## Test Coverage

### TestBasicCalculations
- ✅ TA + DIC → System
- ✅ TA + pH → System
- ✅ DIC + pH → System
- ✅ pCO₂ + pH → System
- ✅ TA + pCO₂ → System

### TestConsistency
- ✅ DIC conservation: DIC = CO₂ + HCO₃⁻ + CO₃²⁻
- ✅ Parameter self-consistency (any 2 params → same results)
- ✅ Forward/reverse consistency

### TestValidation
- ✅ Validates consistent calculations
- ✅ Catches DIC conservation errors
- ✅ Catches negative concentrations
- ✅ Validates pH ranges

### TestOceaanicRanges
- ✅ Modern ocean conditions (7.8-8.3 pH)
- ✅ Acidified conditions (pH < 8.0)
- ✅ Alkaline conditions (pH > 8.1)

### TestParameterRanges
- ✅ Temperature effects on pH
- ✅ Salinity effects on system
- ✅ Extreme TA values (1800-3000 μmol/kg)
- ✅ Extreme DIC values (1600-2800 μmol/kg)

### TestPresetConditions
- ✅ Surface waters (warm, low DIC)
- ✅ Deep waters (cold, high DIC)
- ✅ Contemporary global average ocean
- ✅ High CO₂ acidification scenario

### TestEdgeCases
- ✅ Error handling for insufficient parameters
- ✅ Three-parameter calculations
- ✅ Parameter validation

## Key Validations

The test suite verifies:

1. **Internal Consistency**: DIC properly equals sum of species
2. **Parameter Independence**: Any pair of parameters calculates the same system
3. **Physical Validity**: All concentrations positive, pH in realistic range
4. **Oceanographic Reasonableness**: Results match known ocean ranges
5. **Temperature/Salinity Effects**: Proper response to environmental variables

## Integration with Notebooks

The core calculation functions are extracted to `carbonate_system.py` for reusability in:
- Unit tests (this directory)
- Jupyter notebooks (via import)
- Future applications

Example usage in notebooks:
```python
from carbonate_system import calc_system, validate_carbonate_system

# Calculate
result = calc_system(alk=2300, dic=2020)

# Validate
validation = validate_carbonate_system(result)
if validation['valid']:
    print(f"pH = {result['pH']:.2f}")
```

## Standards

- **Framework**: pytest
- **Coverage Target**: >90%
- **Tolerance**: 1% for most calculations (chemical precision)
- **Data Source**: PyCO2SYS library (oceanographic standard)
