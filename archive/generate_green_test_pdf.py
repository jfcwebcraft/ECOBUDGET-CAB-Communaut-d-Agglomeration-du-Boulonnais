from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'DEVIS - TRAVAUX VERTS', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Créer le PDF
pdf = PDF()
pdf.add_page()

# En-tête
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 10, 'Entreprise EcoConstruct', 0, 1)
pdf.set_font('Arial', '', 10)
pdf.cell(0, 6, '123 Rue Verte, 62200 Boulogne-sur-Mer', 0, 1)
pdf.ln(5)

pdf.set_font('Arial', 'B', 10)
pdf.cell(0, 6, 'Client: Communaute d\'Agglomeration du Boulonnais', 0, 1)
pdf.cell(0, 6, 'Date: 23/11/2024', 0, 1)
pdf.ln(10)

# Tableau des lignes
pdf.set_font('Arial', 'B', 10)
pdf.cell(120, 8, 'Designation', 1)
pdf.cell(35, 8, 'Quantite', 1)
pdf.cell(35, 8, 'Prix HT', 1, 1)

pdf.set_font('Arial', '', 9)

# Lignes vertes
lines = [
    ("Isolation thermique toiture (100m2)", "100 m2", "15 000.00 EUR"),
    ("Installation panneaux solaires 10kWc", "1 unite", "12 500.00 EUR"),
    ("Vehicule electrique utilitaire", "1 unite", "35 000.00 EUR"),
    ("Plantation arbres fruitiers locaux", "25 arbres", "2 500.00 EUR"),
    ("Systeme recuperation eau de pluie 5000L", "1 unite", "3 200.00 EUR"),
    ("Composteur collectif 800L", "2 unites", "1 800.00 EUR"),
    ("LED eclairage public basse consommation", "50 luminaires", "8 500.00 EUR"),
]

for line in lines:
    pdf.cell(120, 7, line[0], 1)
    pdf.cell(35, 7, line[1], 1)
    pdf.cell(35, 7, line[2], 1, 1, 'R')

# Total
pdf.ln(5)
pdf.set_font('Arial', 'B', 11)
pdf.cell(120, 8, '', 0)
pdf.cell(35, 8, 'TOTAL HT:', 1)
pdf.cell(35, 8, '78 500.00 EUR', 1, 1, 'R')

# Sauvegarder
output_path = r"C:\Users\docje\OneDrive\Documents\Code\CAB\ECOBUDGET-CAB\Devis_Investissements_Verts_Test.pdf"
pdf.output(output_path)
print(f"PDF cree: {output_path}")
