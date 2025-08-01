# Marine Carbonate System Visualizer - Bjerrum Plot

Interactive Jupyter notebook for visualizing marine carbonate chemistry with Bjerrum plots.

## Features

- **Interactive Bjerrum Plot**: Species fractions vs pH showing CO2, HCO3-, and CO3-2 distribution
- **Real-time Visualization**: Adjustable Total Alkalinity (TA) and Dissolved Inorganic Carbon (DIC) parameters
- **Complete System Analysis**: Current composition, saturation states, and detailed calculations
- **Educational Tool**: Perfect for marine chemistry courses and ocean acidification studies

## Launch in Binder

Click to launch the interactive notebook in your browser:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/[YOUR_USERNAME]/marine_carbonate_visualizer/HEAD?urlpath=%2Fvoila%2Frender%2Fmarine_carbonate_binder_clean.ipynb)

*Replace [YOUR_USERNAME] with your GitHub username after uploading*

## Local Installation

If you want to run locally:

```bash
git clone https://github.com/[YOUR_USERNAME]/marine_carbonate_visualizer.git
cd marine_carbonate_visualizer
conda env create -f environment_clean.yml
conda activate marine-carbonate
jupyter notebook marine_carbonate_binder_clean.ipynb
```

## Dependencies

- Python 3.10
- PyCO2SYS 1.8.3 (Marine carbonate system calculations)
- matplotlib 3.10.3 (Plotting)
- ipywidgets 8.1.5 (Interactive controls)
- Voila 0.5.8 (Web app conversion)

## Usage

1. Launch the notebook using the Binder link above
2. Adjust the sliders for Total Alkalinity (1800-3500 μmol/kg) and DIC (1600-3500 μmol/kg)  
3. Observe real-time changes in:
   - Bjerrum plot showing species distribution vs pH
   - Current system composition (pie chart)
   - Aragonite saturation state
   - Complete numerical analysis

## Educational Applications

- Marine chemistry courses
- Ocean acidification studies  
- Carbonate system equilibria
- Seawater buffer capacity analysis
- Climate change impact visualization

## Technical Details

The tool uses PyCO2SYS for accurate marine carbonate system calculations at:
- **Salinity**: 35 PSU (fixed)
- **Temperature**: 25°C (fixed)
- **Input parameters**: Total Alkalinity and DIC (variable)

Results include pH, pCO2, individual species concentrations, and saturation states.

## Author & License

**Author:** Cardoso-Mohedano JG  
**Institution:** Instituto de Ciencias del Mar y Limnologia, UNAM, Estacion El Carmen  
**ORCID:** [0000-0002-2918-972X](https://orcid.org/0000-0002-2918-972X)

**License:** [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

## References

- [PyCO2SYS Documentation](https://pyco2sys.readthedocs.io/en/latest/)
- [Binder Documentation](https://mybinder.readthedocs.io/en/latest/)
- [Voila Documentation](https://voila.readthedocs.io/en/stable/)

---
*This tool was developed with assistance from AI tools and Python scientific computing libraries.*
