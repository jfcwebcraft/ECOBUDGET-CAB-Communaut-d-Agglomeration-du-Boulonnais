import { useState } from 'react';
import UploadZone from './components/UploadZone';
import AnalysisResultTable from './components/AnalysisResult';
import { analyzeDevis, AnalysisResult } from './services/api';

function App() {
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleFileSelect = async (file: File) => {
        setIsAnalyzing(true);
        setError(null);
        try {
            const data = await analyzeDevis(file);
            setResult(data);
        } catch (err) {
            console.error(err);
            setError("Une erreur est survenue lors de l'analyse du fichier. Vérifiez que le backend est bien lancé.");
        } finally {
            setIsAnalyzing(false);
        }
    };

    const handleReset = () => {
        setResult(null);
        setError(null);
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8 font-sans text-gray-900">
            <header className="max-w-6xl mx-auto mb-12 flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-green-800 tracking-tight">ECOBUDGET-CAB</h1>
                    <p className="text-gray-500 mt-1">Outil d'analyse budgétaire vert & bas carbone</p>
                </div>
                <div className="text-right hidden md:block">
                    <p className="text-sm text-gray-400">Version Bêta 0.2</p>
                    <p className="text-xs text-gray-300">Propulsé par Ollama Phi-3</p>
                </div>
            </header>

            <main className="max-w-6xl mx-auto">
                {error && (
                    <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg flex items-center gap-3">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        {error}
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
