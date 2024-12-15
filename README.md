# README for Molecule Categorization for Curriculum Learning

## Project Overview

This project aims to predict **Canonical SMILES** for molecules using a **large language model (LLM)**, compute fallback metrics using RDKit, and categorize molecules into difficulty levels based on their properties. The categorization facilitates **curriculum learning**, where molecules are processed and classified as **Easy**, **Medium**, or **Hard**, enabling a structured progression in learning tasks.

---

## Features

1. **Prediction of Canonical SMILES**:
   - Uses an LLM to predict Canonical SMILES strings for molecules based on their properties.
   - Implements a timeout mechanism for API calls to handle latency issues.

2. **Fallback Metrics Calculation**:
   - Computes molecular metrics using RDKit when SMILES predictions fail.
   - Includes:
     - **LogP**: Octanol-water partition coefficient.
     - **SA**: Synthetic Accessibility (approximated using the number of rotatable bonds).
     - **QED**: Quantitative Estimate of Drug-Likeness.
     - **Weight**: Molecular weight.

3. **Categorization for Curriculum Learning**:
   - Molecules are categorized into **Easy**, **Medium**, or **Hard** levels based on their metrics:
     - Weight and rotatable bonds thresholds.

4. **Dataset Processing**:
   - Cleans and processes a dataset of molecular properties.
   - Removes unnecessary fields like `IsomericSMILES`.

5. **Output**:
   - Saves results in a structured JSON file, including:
     - Predicted SMILES.
     - Fallback metrics.
     - Difficulty level.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- API key for **OpenAI Nebius** platform.
- Libraries:
  - `openai`
  - `rdkit`
  - `json`
  - `threading`

### Setup
1. Clone the repository and navigate to the project folder:
   ```bash
   git clone https://github.com/your-username/molecule-categorization.git
   cd molecule-categorization
   ```
2. Install required libraries:
   ```bash
   pip install openai rdkit
   ```
3. Add your **OpenAI API key** in the `client` initialization:
   ```python
   api_keyyy = "your_api_key_here"
   ```

---

## Usage

1. **Prepare Dataset**:
   - Place your dataset file (`extended_molecules_properties.json`) in the project directory.
   - Ensure it contains the necessary molecular properties.

2. **Run the Script**:
   ```bash
   python molecule_categorization.py
   ```

3. **Output**:
   - Results will be saved in `categorized_molecules.json`.

---

## File Structure

- `molecule_categorization.py`: Main script for processing molecules.
- `extended_molecules_properties.json`: Input dataset (required).
- `categorized_molecules.json`: Output file with categorized molecules.

---

## Key Functions

- **`predict_smiles(molecule)`**:
  - Generates SMILES strings using an LLM.
  - Returns `None` if the prediction fails.

- **`compute_metrics(smiles)`**:
  - Computes fallback metrics for a given SMILES string.

- **`categorize_difficulty(metrics)`**:
  - Categorizes molecules into `Easy`, `Medium`, or `Hard` difficulty levels.

- **`call_api_with_timeout(prompt, client, model_name, timeout)`**:
  - Calls the OpenAI API with a specified timeout.

---

## Example Input

```json
{
    "CID": 12345,
    "MolecularFormula_PubChem": "C7H6O2",
    "MolecularWeight_PubChem": 122.12,
    "MolecularWeight_RDKit": 122.12,
    "ExactMass": 122.03678,
    "TPSA": 37.3,
    "LogP": 1.6,
    "NumHDonors": 1,
    "NumHAcceptors": 2,
    "NumRotatableBonds": 0,
    "RingCount": 1,
    "AromaticRingCount": 1,
    "AtomCount": 15,
    "BondCount": 14,
    "Charge": 0,
    "ChiralCenters": 0,
    "BondTypes": ["single", "double"],
    "FunctionalGroups": ["phenol", "hydroxy"]
}
```

---

## Example Output

```json
{
    "CID": 12345,
    "PredictedSMILES": "C1=CC=C(C=C1)O",
    "Metrics": {
        "valid": true,
        "logP": 1.6,
        "SA": 0,
        "QED": 0.91,
        "weight": 122.12
    },
    "Difficulty": "Easy"
}
```

---

## Limitations

1. Predictions depend on the performance of the LLM and dataset quality.
2. Fallback metrics may not always accurately capture molecular complexity.
3. Timeout for API calls is fixed at 5 seconds (configurable).

---

## Future Improvements

- Enhance error handling for invalid input data.
- Implement support for larger datasets with efficient batch processing.
- Add visualization of molecular properties.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
