import React from 'react';

interface AnalysisLine {
    ligne: string;
    montant_ht: number;
    budget_vert: boolean;
    code_categorie: string | null;
    axe: string | null;
    confiance: number;
    explication: string;
}

interface AnalysisResultData {
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
}

interface AnalysisResultProps {
    result: AnalysisResultData;
    onReset: () => void;
}

const AnalysisResult: React.FC<AnalysisResultProps> = ({ result, onReset }) => {
    return (
        <div className="w-full max-w-6xl mx-auto mt-8 animate-fade-in">
            {/* En-tête des résultats */}
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6 border border-gray-100">
                <div className="flex justify-between items-start mb-6">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-800 mb-1">Résultat de l'analyse</h2>
                        <p className="text-gray-500 text-sm">Fichier : {result.filename}</p>
                    </div>
                    <button
                        onClick={onReset}
                        className="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                    >
                        Nouvelle analyse
                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <p className="text-sm text-gray-500 mb-1">Total HT</p>
                        <p className="text-2xl font-bold text-gray-900">{result.total_ht.toLocaleString('fr-FR')} €</p>
                    </div>
                    <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                        <p className="text-sm text-green-600 mb-1">Budget Vert Éligible</p>
                        <p className="text-2xl font-bold text-green-700">{result.total_budget_vert.toLocaleString('fr-FR')} €</p>
                    </div>
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <p className="text-sm text-blue-600 mb-1">Part Verte</p>
                        <div className="flex items-end gap-2">
                            <p className="text-2xl font-bold text-blue-700">{result.pourcentage_budget_vert}%</p>
                            <div className="w-full bg-blue-200 h-2 rounded-full mb-2">
                                <div
                                    className="bg-blue-600 h-2 rounded-full transition-all duration-1000"
                                    style={{ width: `${result.pourcentage_budget_vert}%` }}
                                ></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Tableau détaillé */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-gray-50 border-b border-gray-200 text-xs uppercase text-gray-500 font-semibold">
                                <th className="p-4">Désignation</th>
                                <th className="p-4 text-right">Montant HT</th>
                                <th className="p-4 text-center">Statut</th>
                                <th className="p-4">Catégorie</th>
                                <th className="p-4">Explication IA</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {result.lignes.map((line, index) => (
                                <tr key={index} className="hover:bg-gray-50 transition-colors">
                                    <td className="p-4 text-sm text-gray-800 font-medium">{line.ligne}</td>
                                    <td className="p-4 text-sm text-gray-600 text-right font-mono">
                                        {line.montant_ht.toLocaleString('fr-FR')} €
                                    </td>
                                    <td className="p-4 text-center">
                                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${line.budget_vert
                                            ? "bg-green-100 text-green-800"
                                            : "bg-gray-100 text-gray-800"
                                            }`}>
                                            {line.budget_vert ? "VERT" : "NON"}
                                        </span>
                                    </td>
                                    <td className="p-4 text-sm">
                                        {line.code_categorie ? (
                                            <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-100">
                                                {line.code_categorie}
                                            </span>
                                        ) : (
                                            <span className="text-gray-400">-</span>
                                        )}
                                    </td>
                                    <td className="p-4 text-sm text-gray-500 italic max-w-xs truncate" title={line.explication}>
                                        {line.explication}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                {result.lignes.length === 0 && (
                    <div className="p-8 text-center text-gray-500">
                        Aucune ligne détectée dans ce document.
                    </div>
                )}
            </div>

            {/* Détails Techniques */}
            <div className="mt-8 bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Détails Techniques</h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                        <span className="text-gray-500">Modèle IA :</span>
                        <span className="ml-2 font-mono text-blue-600">{result.metadata?.model || "Inconnu"}</span>
                    </div>
                    <div>
                        <span className="text-gray-500">Temps de traitement :</span>
                        <span className="ml-2 font-mono text-blue-600">{result.metadata?.duration ? `${result.metadata.duration}s` : "N/A"}</span>
                    </div>
                    <div>
                        <span className="text-gray-500">Lignes analysées :</span>
                        <span className="ml-2 font-mono text-blue-600">
                            {result.metadata?.lines_output}/{result.metadata?.lines_input || "?"}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AnalysisResult;
