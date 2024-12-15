import json
from openai import OpenAI
from rdkit import Chem
from rdkit.Chem import Descriptors, QED
import threading

# Initialize OpenAI client

client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=api_keyyy  
)
# Load dataset
with open("extended_molecules_properties.json", "r") as f:
    dataset = json.load(f)
dataset = dataset[:1000]

# Remove IsomericSMILES
for molecule in dataset:
    molecule.pop("IsomericSMILES", None)

# Define the function to call the OpenAI API with a timeout
def call_api_with_timeout(prompt, client, model_name, timeout=5):
    result = {"response": None, "error": None}

    def api_call():
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            result["response"] = response.choices[0].message.content.strip().split("\n")[0]
            print(result["response"])
        except Exception as e:
            result["error"] = str(e)
            print(e)

    api_thread = threading.Thread(target=api_call)
    api_thread.start()

    api_thread.join(timeout=timeout)

    if api_thread.is_alive():
        return None, "Timeout: API call took longer than allowed time"
    else:
        return result["response"], result["error"]


# Define function to predict CanonicalSMILES using LLM
def predict_smiles(molecule):
    prompt = (
        f"Based on the following properties, predict the Canonical SMILES of the molecule. Dont generate any other text . only the SMILES string \n"
        f"Molecular Formula: {molecule['MolecularFormula_PubChem']}\n"
        f"Molecular Weight (PubChem): {molecule['MolecularWeight_PubChem']}\n"
        f"Molecular Weight (RDKit): {molecule['MolecularWeight_RDKit']}\n"
        f"Exact Mass: {molecule['ExactMass']}\n"
        f"TPSA: {molecule['TPSA']}\n"
        f"LogP: {molecule['LogP']}\n"
        f"NumHDonors: {molecule['NumHDonors']}\n"
        f"NumHAcceptors: {molecule['NumHAcceptors']}\n"
        f"NumRotatableBonds: {molecule['NumRotatableBonds']}\n"
        f"RingCount: {molecule['RingCount']}\n"
        f"AromaticRingCount: {molecule['AromaticRingCount']}\n"
        f"AtomCount: {molecule['AtomCount']}\n"
        f"BondCount: {molecule['BondCount']}\n"
        f"Charge: {molecule['Charge']}\n"
        f"Chiral Centers: {molecule['ChiralCenters']}\n"
        f"Bond Types: {', '.join(molecule['BondTypes'])}\n"
        f"Functional Groups: {', '.join(molecule['FunctionalGroups'])}\n"
    )
    model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-fast"

    response, error = call_api_with_timeout(prompt, client, model_name)
    return response if error is None else None

# Define fallback metrics (if Moses fails)
def compute_metrics(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        return {"valid": False}

    metrics = {
        "valid": True,
        "logP": Descriptors.MolLogP(mol),
        "SA": Descriptors.NumRotatableBonds(mol),
        "QED": QED.qed(mol),
        "weight": Descriptors.MolWt(mol)
    }
    return metrics

# Categorize molecules into difficulty levels
def categorize_difficulty(metrics):
    if not metrics["valid"]:
        return "Hard"

    # Use thresholds to categorize
    if metrics["weight"] < 200 and metrics["SA"] <= 3:
        return "Easy"
    elif metrics["weight"] < 400 and metrics["SA"] <= 6:
        return "Medium"
    else:
        return "Hard"

# Process dataset
results = []
for molecule in dataset:
    smiles = predict_smiles(molecule)
    if not smiles:
        difficulty = "Hard"  # Default to Hard if prediction fails
        metrics = {}
    else:
        metrics = compute_metrics(smiles)
        difficulty = categorize_difficulty(metrics)

    results.append({
        "CID": molecule["CID"],
        "PredictedSMILES": smiles,
        "Metrics": metrics,
        "Difficulty": difficulty
    })

# Save categorized dataset
with open("categorized_molecules.json", "w") as f:
    json.dump(results, f, indent=4)
