# DGA Database - Dissolved Gas Analysis for Transformer Fault Diagnosis

A comprehensive database of transformer dissolved gas analysis (DGA) data for research and educational purposes.

## 🎯 Overview

This repository contains a quality-controlled dataset of dissolved gas analysis measurements from transformers, designed to support research in transformer condition monitoring and fault diagnosis. The database provides high-quality DGA data for developing and validating diagnostic algorithms.

## 📊 Dataset Characteristics

- **Gas Parameters**: 5 key dissolved gases (H₂, CH₄, C₂H₄, C₂H₆, C₂H₂)
- **Fault Classifications**: Multiple fault types including electrical, thermal, and discharge faults
- **Data Quality**: Systematic cleaning and validation
- **Statistical Diversity**: Wide range of gas concentrations and fault signatures

## 🌐 Web Interface

Access the interactive database locally by opening `index.html` in your browser.

### Features

- **Interactive Queries**: Filter data using simple expressions
- **Quick Access**: Predefined queries for common scenarios
- **Multiple Downloads**: CSV export options and complete database download
- **Statistical Analysis**: Comprehensive visualizations and correlations
- **Methodology Documentation**: Complete data collection procedures

### Query Examples

```
Hydrogen > 100                    # High hydrogen levels
Fault == "Electrical"            # Electrical fault cases
Hydrogen > 100 AND Methane > 30   # Multiple conditions
Ethylene > 50 OR Acetylene > 5    # Alternative conditions
```

## 📁 Repository Structure

```
DGA_Dataset_Repo/
├── index.html              # Main database interface
├── analysis.html           # Statistical analysis and visualizations
├── collection.html         # Data collection methodology
├── StatDGA.py              # Data analysis and figure generation script
├── FinalDataSet_DGA.xlsx   # Complete dataset (Excel format)
├── FinalFigures1/          # Generated statistical figures
│   ├── 01c2_*_distribution_log_only.png
│   ├── 02_correlation_analysis.png
│   ├── 03c_distribution_analysis_log_only.png
│   ├── 04c_*_histogram_log_y_axis.png
│   ├── 04_5_distribution_analysis_lognormal.png
│   └── 05_fault_analysis.png
└── README.md               # This documentation
```

## 🔧 Usage

### Web Interface Access

1. Open `index.html` in your web browser
2. Use the query interface to filter data
3. Download results in CSV format
4. Explore statistical analysis and methodology sections

### Data Analysis

Run the statistical analysis script:

```bash
python StatDGA.py
```

**Requirements:**
- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

## 📈 Statistical Analysis

The dataset includes comprehensive statistical characterization with key findings on distribution patterns, concentration ranges, inter-gas correlations, and fault signatures.

### Generated Figures

1. **Gas Distributions**: Individual concentration patterns for each gas
2. **Correlation Analysis**: Inter-gas relationship heatmap
3. **Box Plots**: Statistical summaries on logarithmic scales
4. **Frequency Distributions**: Histogram analysis with logarithmic scaling
5. **Distribution Fitting**: Statistical model fitting and parameters
6. **Fault Analysis**: Gas signatures by fault type

## 🔬 Research Applications

### Supported Use Cases

- **Machine Learning**: Training and validation of diagnostic algorithms
- **Benchmarking**: Standardized comparison of diagnostic methods
- **Education**: Real-world data for teaching DGA interpretation
- **Method Validation**: Testing traditional ratio-based approaches
- **Algorithm Development**: Pattern recognition and classification research

### DGA Methods Supported

- Key Gas Method
- Rogers Ratio Method
- Doernenburg Ratio Method
- IEC Ratio Method (IEC 60599)
- Duval Triangle/Pentagon
- Machine Learning Approaches

## 📊 Data Quality

The dataset has undergone systematic quality assurance including source verification, format standardization, duplicate detection, outlier analysis, and integrity verification against established DGA patterns.

## 📚 Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{dga_database_2024,
  title={DGA Database: Comprehensive Dissolved Gas Analysis Dataset for Transformer Fault Diagnosis},
  author={[Authors]},
  year={2024},
  note={Open access dataset for transformer condition monitoring research}
}
```

## 📄 License

This dataset is provided under an **Open Access License** for research and educational purposes.

### Terms of Use

- ✅ Research and academic use
- ✅ Educational purposes
- ✅ Non-commercial applications
- ✅ Method development and validation
- ❌ Commercial redistribution without permission
- ❌ Claims of ownership or exclusivity

---

**Disclaimer**: This dataset is provided for research purposes. Users should validate results against established standards and practices.
