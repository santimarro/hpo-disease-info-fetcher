# -*- coding: utf-8 -*-
"""
## Overview

This notebook allows you to search for diseases and retrieve information about them, including associated symptoms, by providing a list of disease names. The program uses the Human Phenotype Ontology (HPO) API to search for diseases and fetch the relevant data. It employs fuzzy string matching to select the closest matching disease when multiple results are found.

## Dependencies

To run the program, make sure you have the following Python libraries installed:

- requests
- fuzzywuzzy
- python-Levenshtein

You can install them using pip:

```
pip install requests fuzzywuzzy python-Levenshtein
```

## How to use

1. Import the `get_disease_data` function from the program:

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

## Example usage

```python
from disease_info_fetcher import get_disease_data

disease_names = ["Marfan syndrome", "Ehlers-Danlos syndrome"]
disease_data = get_disease_data(disease_names)
print(disease_data)
```

This example demonstrates how to search for two diseases, "Marfan syndrome" and "Ehlers-Danlos syndrome," and print the retrieved information and associated symptoms.
"""

import requests
from fuzzywuzzy import process

def search_diseases(disease_name):
    url = "https://hpo.jax.org/api/hpo/search"
    params = {"q": disease_name, "category": "diseases"}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        search_results = response.json()
        return search_results["diseases"]
    else:
        print(f"Error searching diseases for {disease_name}: {response.status_code}")
        return []

def select_closest_disease(disease_name, search_results):
    disease_names = [entry["dbName"] for entry in search_results]
    closest_name, _ = process.extractOne(disease_name, disease_names)
    closest_names = process.extract(disease_name, disease_names, limit=2)
  
    find_orpha = False
    max_score = 0
    first_name, first_score = closest_names[0]
    second_name, second_score = closest_names[1]

    if first_name == second_name:
      # we have the same disease repeated. This means two ids, orpha and omim
      find_orpha = True
    
    for entry in search_results:
        if entry["dbName"] == closest_name:
          if find_orpha:
            if entry["db"] == "ORPHA":
              return entry["diseaseId"]
          else:
            return entry["diseaseId"]

    return None

def get_disease_info(disease_id):
    url = f"https://hpo.jax.org/api/hpo/disease/{disease_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching disease info for {disease_id}: {response.status_code}")
        return None

def get_disease_symptoms(disease_id):
    url = f"https://hpo.jax.org/api/hpo/disease/{disease_id}/phenotypes"
    response = requests.get(url)
    
    if response.status_code == 200:
        return [entry["phenotype"] for entry in response.json()]
    else:
        print(f"Error fetching symptoms for {disease_id}: {response.status_code}")
        return []

def get_disease_data(disease_names):
    disease_data = []
    
    for disease_name in disease_names:
        search_results = search_diseases(disease_name)
        closest_disease_id = select_closest_disease(disease_name, search_results)
        
        if closest_disease_id is not None:
            disease_info = get_disease_info(closest_disease_id)
            if disease_info is not None:
                # disease_info["symptoms"] = get_disease_symptoms(closest_disease_id)
                disease_data.append(disease_info)
    
    return disease_data

# Example usage
disease_names = ["Sarcoidosis", "Marfan syndrome", "Ehlers-Danlos syndrome"]
disease_data = get_disease_data(disease_names)
print(disease_data)

# Symptoms can be found under the catTermsMap key
print("Disease {}\n".format(disease_data[0]["disease"]["diseaseName"]))

print("Symptoms:\n")
print(disease_data[0]["catTermsMap"])

