import { useState, useEffect } from 'react';
import { FileUpload } from './components/FileUpload';
import { BudgetTable } from './components/BudgetTable';
import { CorrectionModal } from './components/CorrectionModal';
import { uploadFile, getBudgetLines, updateBudgetLine } from './api';
import * as styles from './styles.css';

function App() {
    const [data, setData] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentLine, setCurrentLine] = useState<any>(null);

    const fetchData = async () => {
        try {
            const result = await getBudgetLines();
            setData(result);
        } catch (err) {
            console.error("Failed to fetch budget lines", err);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleFileSelect = async (file: File) => {
        setIsLoading(true);
        setError(null);
        try {
            await uploadFile(file);
            await fetchData();
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || "Une erreur est survenue lors de l'upload.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleValidate = async (index: number) => {
        const line = data[index];
        try {
            await updateBudgetLine(line.exercice, line.num_bordereau, line.num_piece, {
                statut: 'VALIDE'
            });
            // Optimistic update or refetch
            const newData = [...data];
            newData[index].statut = 'VALIDE';
            setData(newData);
        } catch (err) {
            console.error("Failed to validate line", err);
            alert("Erreur lors de la validation");
        }
    };

    const handleCorrect = (index: number) => {
        setCurrentLine(data[index]);
        setIsModalOpen(true);
    };

    const handleSaveCorrection = async (updatedData: any) => {
        if (!currentLine) return;
        try {
            await updateBudgetLine(currentLine.exercice, currentLine.num_bordereau, currentLine.num_piece, {
                ...updatedData,
                statut: 'VALIDE' // Or 'CORRIGE' if preferred, but user flow suggests validation after correction
            });
            setIsModalOpen(false);
            setCurrentLine(null);
            await fetchData(); // Refetch to get updated data
        } catch (err) {
            console.error("Failed to save correction", err);
            alert("Erreur lors de la sauvegarde");
        }
    };

    return (
        <div className={styles.container}>
            <header className={styles.header}>
                <h1 className={styles.title}>EcoBudget Assistant</h1>
                <p className={styles.subtitle}>Analyse et classification automatique des dépenses (Budget Vert)</p>
            </header>

            <main>
                <FileUpload onFileSelect={handleFileSelect} isLoading={isLoading} />

                {error && (
                    <div style={{ color: 'red', textAlign: 'center', marginBottom: '1rem' }}>
                        {error}
                    </div>
                )}

                <BudgetTable
                    data={data}
                    onValidate={handleValidate}
                    onCorrect={handleCorrect}
                />

                <CorrectionModal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    onSave={handleSaveCorrection}
                    initialData={currentLine}
                />
            </main>
        </div>
    );
}

export default App;
