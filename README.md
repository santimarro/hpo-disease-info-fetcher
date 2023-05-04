# Disease Information Fetcher

Disease Information Fetcher is a Python program that searches for diseases and retrieves information about them, including associated symptoms, using the Human Phenotype Ontology (HPO) API. It uses fuzzy string matching to select the closest matching disease when multiple results are found.

## Requirements

- Python 3.6 or higher

## Installation

1. Clone the repository:

```
git clone https://github.com/santimarro/disease-info-fetcher.git
```

2. Change into the `disease-info-fetcher` directory:

```
cd disease-info-fetcher
```

3. Install the required Python libraries:

```
pip install -r requirements.txt
```

## Usage

1. Import the `get_disease_data` function from `disease_info_fetcher.py`:

```python
from disease_info_fetcher import get_disease_data
```

2. Provide a list of disease names that you want to search for:

```python
disease_names = ["Marfan syndrome", "Ehlers-Danlos syndrome"]
```

3. Call the `get_disease_data` function with the list of disease names. This function returns a list of dictionaries containing the disease information and associated symptoms:

```python
disease_data = get_disease_data(disease_names)
```

4. Process the returned `disease_data` as needed. Each dictionary in the list contains the disease information and its associated symptoms. For example, you can print the disease data:

```python
print(disease_data)
```

## Example

```python
from disease_info_fetcher import get_disease_data

disease_names = ["Marfan syndrome", "Ehlers-Danlos syndrome"]
disease_data = get_disease_data(disease_names)
print(disease_data)
```

This example demonstrates how to search for two diseases, "Marfan syndrome" and "Ehlers-Danlos syndrome," and print the retrieved information and associated symptoms.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
