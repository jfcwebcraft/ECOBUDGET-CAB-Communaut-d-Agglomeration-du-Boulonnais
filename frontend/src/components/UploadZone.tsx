import React, { useState, useRef } from 'react';

interface UploadZoneProps {
    onFileSelect: (file: File) => void;
    isAnalyzing: boolean;
}

const UploadZone: React.FC<UploadZoneProps> = ({ onFileSelect, isAnalyzing }) => {
    const [dragActive, setDragActive] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onFileSelect(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            onFileSelect(e.target.files[0]);
        }
    };

    const onButtonClick = () => {
        inputRef.current?.click();
    };

    return (
        <div
            className={`w-full max-w-2xl mx-auto p-8 border-2 border-dashed rounded-xl text-center transition-all duration-200 ${dragActive ? "border-green-500 bg-green-50" : "border-gray-300 bg-white"
                } ${isAnalyzing ? "opacity-50 pointer-events-none" : ""}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
        >
            <input
                ref={inputRef}
                type="file"
                className="hidden"
                accept=".pdf"
                onChange={handleChange}
            />

            <div className="flex flex-col items-center justify-center gap-4">
                <div className="p-4 bg-green-100 rounded-full">
                    <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                </div>

                <div>
                    <h3 className="text-lg font-semibold text-gray-700">
                        {isAnalyzing ? "Analyse en cours..." : "Déposez votre devis PDF ici"}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                        ou <button onClick={onButtonClick} className="text-green-600 font-medium hover:underline">parcourez vos fichiers</button>
                    </p>
                </div>

                <p className="text-xs text-gray-400">PDF uniquement (max 10MB)</p>
            </div>
        </div>
    );
};

export default UploadZone;
