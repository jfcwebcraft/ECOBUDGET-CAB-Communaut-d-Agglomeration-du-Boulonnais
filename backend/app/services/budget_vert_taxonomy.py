import json

class BudgetVertTaxonomy:
    def load_taxonomy(self, path: str):
        with open(path, 'r') as f:
            return json.load(f)
