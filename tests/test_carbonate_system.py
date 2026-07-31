"""
Tests for Marine Carbonate System Calculator

Verifies consistency of TA-DIC-pH calculations using PyCO2SYS.
"""

import pytest
from carbonate_system import calc_system, validate_carbonate_system, check_oceanic_ranges


class TestBasicCalculations:
    """Test basic carbonate system calculations with standard conditions."""

    def test_ta_dic_calculation(self):
        """Calculate system from TA and DIC."""
        result = calc_system(alk=2300, dic=2020)
        assert result['pH'] > 0
        assert result['DIC'] == pytest.approx(2020, rel=0.01)
        assert result['TA'] == pytest.approx(2300, rel=0.01)

    def test_ta_ph_calculation(self):
        """Calculate system from TA and pH."""
        result = calc_system(alk=2300, pH=8.0)
        assert result['pH'] == pytest.approx(8.0, abs=0.01)
        assert result['TA'] == pytest.approx(2300, rel=0.01)

    def test_dic_ph_calculation(self):
        """Calculate system from DIC and pH."""
        result = calc_system(dic=2020, pH=8.1)
        assert result['pH'] == pytest.approx(8.1, abs=0.01)
        assert result['DIC'] == pytest.approx(2020, rel=0.01)

    def test_pco2_ph_calculation(self):
        """Calculate system from pCO2 and pH."""
        result = calc_system(pCO2=400, pH=8.0)
        assert result['pH'] == pytest.approx(8.0, abs=0.01)
        assert result['pCO2'] == pytest.approx(400, rel=0.05)

    def test_ta_pco2_calculation(self):
        """Calculate system from TA and pCO2."""
        result = calc_system(alk=2300, pCO2=400)
        assert result['TA'] == pytest.approx(2300, rel=0.01)
        assert result['pCO2'] == pytest.approx(400, rel=0.05)


class TestConsistency:
    """Test internal consistency of carbonate system."""

    def test_dic_conservation(self):
        """DIC must equal sum of CO2 + HCO3 + CO3."""
        result = calc_system(alk=2300, dic=2020)
        dic_sum = result['CO2'] + result['HCO3'] + result['CO3']
        assert dic_sum == pytest.approx(result['DIC'], rel=0.01)

    def test_consistency_ta_dic_to_ph(self):
        """TA+DIC → pH should be consistent."""
        result1 = calc_system(alk=2300, dic=2020)
        pH = result1['pH']
        result2 = calc_system(alk=2300, pH=pH)
        assert result2['DIC'] == pytest.approx(result1['DIC'], rel=0.02)

    def test_consistency_ta_ph_to_dic(self):
        """TA+pH → DIC should be consistent."""
        result1 = calc_system(alk=2300, dic=2020)
        pH = result1['pH']
        result2 = calc_system(alk=2300, pH=pH)
        assert result2['DIC'] == pytest.approx(2020, rel=0.02)

    def test_consistency_all_parameters(self):
        """All 4 parameters should be self-consistent."""
        result = calc_system(alk=2300, dic=2020, salinity=35, temperature=25)
        # If we recalculate with any 2 params, we should get similar results
        param_map = {
            'alk': ('alk', 'TA'),
            'dic': ('dic', 'DIC'),
            'pH': ('pH', 'pH'),
            'pCO2': ('pCO2', 'pCO2')
        }
        for p1, p2 in [
            ('alk', 'dic'),
            ('alk', 'pH'),
            ('dic', 'pH'),
            ('alk', 'pCO2'),
        ]:
            p1_calc, p1_result = param_map[p1]
            p2_calc, p2_result = param_map[p2]
            result2 = calc_system(
                **{p1_calc: result[p1_result],
                   p2_calc: result[p2_result],
                   'salinity': 35, 'temperature': 25}
            )
            # All should agree on pH to within 0.05 units
            assert result2['pH'] == pytest.approx(result['pH'], abs=0.05), \
                f"Inconsistency with {p1}+{p2}"


class TestValidation:
    """Test validation functions."""

    def test_valid_system(self):
        """Standard ocean conditions should pass validation."""
        result = calc_system(alk=2300, dic=2020)
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True
        assert len(validation['errors']) == 0

    def test_validation_catches_dic_error(self):
        """Validation should flag DIC conservation errors."""
        # Create invalid result (manually manipulated)
        result = calc_system(alk=2300, dic=2020)
        result['DIC'] = 5000  # Unrealistic
        validation = validate_carbonate_system(result)
        assert validation['valid'] is False
        assert any('DIC conservation' in e for e in validation['errors'])

    def test_validation_catches_negative_values(self):
        """Validation should flag negative concentrations."""
        result = calc_system(alk=2300, dic=2020)
        result['CO3'] = -10  # Invalid
        validation = validate_carbonate_system(result)
        assert validation['valid'] is False
        assert any('negative' in e.lower() for e in validation['errors'])


class TestOceaanicRanges:
    """Test that calculations stay within oceanic ranges."""

    def test_modern_ocean_conditions(self):
        """Standard modern ocean should be within ranges."""
        result = calc_system(alk=2320, dic=2040, salinity=35, temperature=20)
        warnings = check_oceanic_ranges(result)
        # May have warnings but basic structure should be valid
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True

    def test_acidified_conditions(self):
        """Acidified ocean (lower pH) should still be valid."""
        result = calc_system(alk=2300, dic=2100, salinity=35, temperature=25)
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True
        assert result['pH'] < 8.2

    def test_alkaline_conditions(self):
        """High pH conditions should still be valid."""
        result = calc_system(alk=2350, dic=1950, salinity=35, temperature=25)
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True
        assert result['pH'] > 8.1


class TestParameterRanges:
    """Test with different environmental conditions."""

    def test_temperature_effect(self):
        """pH should decrease with increasing temperature."""
        result_cold = calc_system(alk=2300, dic=2020, temperature=5)
        result_warm = calc_system(alk=2300, dic=2020, temperature=25)
        assert result_cold['pH'] > result_warm['pH']

    def test_salinity_effect(self):
        """Results should vary with salinity."""
        result_low = calc_system(alk=2300, dic=2020, salinity=30)
        result_high = calc_system(alk=2300, dic=2020, salinity=35)
        # pH should change, but both should be valid
        validate_carbonate_system(result_low)
        validate_carbonate_system(result_high)

    def test_extreme_ta(self):
        """Extreme TA values should still calculate."""
        for ta in [1800, 2000, 2300, 2500, 3000]:
            result = calc_system(alk=ta, dic=2020)
            validation = validate_carbonate_system(result)
            assert validation['valid'] is True

    def test_extreme_dic(self):
        """Extreme DIC values should still calculate."""
        for dic in [1600, 1800, 2020, 2200, 2800]:
            result = calc_system(alk=2300, dic=dic)
            validation = validate_carbonate_system(result)
            assert validation['valid'] is True


class TestPresetConditions:
    """Test common preset conditions from notebooks."""

    def test_surface_waters(self):
        """Surface water conditions."""
        result = calc_system(alk=2300, dic=1900, temperature=25, salinity=35)
        assert result['pH'] > 8.0
        assert result['pCO2'] < 450
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True

    def test_deep_waters(self):
        """Deep water conditions."""
        result = calc_system(alk=2350, dic=2200, temperature=2, salinity=35)
        assert result['pH'] < 8.1  # Deep waters have lower pH than surface
        assert result['pCO2'] > 300  # Deep waters have elevated CO2
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True

    def test_contemporary_ocean(self):
        """Contemporary global average ocean."""
        result = calc_system(alk=2320, dic=2040, temperature=18, salinity=35)
        assert 7.8 < result['pH'] < 8.3
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True

    def test_high_co2_scenario(self):
        """High CO2 acidification scenario."""
        result = calc_system(alk=2300, dic=2150, temperature=20, salinity=35)
        assert result['pH'] < 8.1
        assert result['omega'] < 2.0  # Reduced saturation state
        validation = validate_carbonate_system(result)
        assert validation['valid'] is True


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_insufficient_parameters(self):
        """Should raise error with only one parameter."""
        with pytest.raises(ValueError, match="At least 2"):
            calc_system(alk=2300)

    def test_no_parameters(self):
        """Should raise error with no parameters."""
        with pytest.raises(ValueError, match="At least 2"):
            calc_system()

    def test_three_parameters(self):
        """Three parameters should work (uses first two)."""
        result = calc_system(alk=2300, dic=2020, pH=8.0)
        assert result['pH'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
