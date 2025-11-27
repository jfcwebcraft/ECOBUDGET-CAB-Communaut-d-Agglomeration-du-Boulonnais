import React from 'react';
import * as styles from '../styles.css';

// Simple custom hook if we don't want to add dependency, but user asked for Drag & Drop.
// Let's assume we can use a simple HTML5 implementation or just use the style for now.
// Actually, I should check package.json if I can add react-dropzone.
// I didn't add it in the plan, so I'll implement a simple one.

interface FileUploadProps {
    onFileSelect: (file: File) => void;
    isLoading: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, isLoading }) => {
    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            onFileSelect(e.dataTransfer.files[0]);
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            onFileSelect(e.target.files[0]);
        }
    };

    return (
        <div
            className={styles.uploadZone}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => document.getElementById('fileInput')?.click()}
        >
            <input
                type="file"
                id="fileInput"
                style={{ display: 'none' }}
                onChange={handleChange}
                accept=".xlsx,.xls,.csv"
            />
            {isLoading ? (
                <p>Traitement en cours... (Cela peut prendre quelques secondes)</p>
            ) : (
                <>
                    <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
                        Glissez-déposez votre fichier Excel ici
                    </p>
                    <p style={{ color: '#7f8c8d' }}>ou cliquez pour sélectionner</p>
                </>
            )}
        </div>
    );
};
