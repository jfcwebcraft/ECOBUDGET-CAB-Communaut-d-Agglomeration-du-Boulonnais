const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function analyzeDevis(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Erreur inconnue' }));
        throw new Error(errorData.detail || `Erreur HTTP ${response.status}`);
    }

    return response.json();
}
