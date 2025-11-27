import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
    baseURL: `${API_URL}/api/v1`,
});

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const getBudgetLines = async () => {
    const response = await api.get('/budget-lines');
    return response.data;
};

export const updateBudgetLine = async (
    exercice: number,
    num_bordereau: number,
    num_piece: number,
    data: any
) => {
    const response = await api.put(
        `/budget-lines/${exercice}/${num_bordereau}/${num_piece}`,
        data
    );
    return response.data;
};
