const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface AnalysisLine {
    ligne: string;
    montant_ht: number;
    budget_vert: boolean;
    code_categorie: string | null;
    axe: string | null;
    confiance: number;
    explication: string;
}

export interface AgregatReference {
    code: string;
    libelle: string;
    type: string;
}

export interface AnalysisResult {
    filename: string;
    total_ht: number;
    total_budget_vert: number;
    pourcentage_budget_vert: number;
    lignes: AnalysisLine[];
    metadata?: {
        model: string;
        duration: number;
        lines_input: number;
        lines_output: number;
        error?: string;
    };
    agregats_reference?: Record<string, AgregatReference>;
}

export async function analyzeDevis(file: File): Promise<AnalysisResult> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erreur lors de l\'analyse');
    }

    return response.json();
}
