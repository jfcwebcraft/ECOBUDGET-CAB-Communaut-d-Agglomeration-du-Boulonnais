import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Configuration de l'instance Axios
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface AnalysisLine {
    ligne: string;
    montant_ht: number;
    budget_vert: boolean;
    code_categorie: string | null;
    confiance: number;
    explication: string;
}

export interface AnalysisResult {
    status: string;
    filename: string;
    lignes: AnalysisLine[];
    total_ht: number;
    total_budget_vert: number;
    pourcentage_budget_vert: number;
}

export const analyzeDevis = async (file: File): Promise<AnalysisResult> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<AnalysisResult>('/analyze', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export default api;
