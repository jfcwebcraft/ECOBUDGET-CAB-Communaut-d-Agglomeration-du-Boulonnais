import React, { useState, useEffect } from 'react';
import * as styles from '../styles.css.ts';

interface CorrectionModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave: (data: any) => void;
    initialData: any;
}

export const CorrectionModal: React.FC<CorrectionModalProps> = ({ isOpen, onClose, onSave, initialData }) => {
    const [formData, setFormData] = useState(initialData || {});

    useEffect(() => {
        setFormData(initialData || {});
    }, [initialData]);

    if (!isOpen) return null;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSave(formData);
    };

    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modalContent}>
                <h2 className={styles.title} style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Correction de la ligne</h2>
                <form onSubmit={handleSubmit}>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Rubrique Axe 1 (Climat)</label>
                        <input
                            type="text"
                            name="rubrique_axe1"
                            value={formData.rubrique_axe1 || ''}
                            onChange={handleChange}
                            className={styles.input}
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Cotation Axe 1</label>
                        <select
                            name="cotation_axe1"
                            value={formData.cotation_axe1 || ''}
                            onChange={handleChange}
                            className={styles.select}
                        >
                            <option value="">Sélectionner...</option>
                            <option value="FAVORABLE">FAVORABLE</option>
                            <option value="DEFAVORABLE">DEFAVORABLE</option>
                            <option value="NEUTRE">NEUTRE</option>
                            <option value="A_APPROFONDIR">A_APPROFONDIR</option>
                        </select>
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Justification Axe 1</label>
                        <textarea
                            name="justification_axe1"
                            value={formData.justification_axe1 || ''}
                            onChange={handleChange}
                            className={styles.textarea}
                        />
                    </div>

                    <hr style={{ margin: '1.5rem 0', border: '0', borderTop: '1px solid #eee' }} />

                    <div className={styles.formGroup}>
                        <label className={styles.label}>Rubrique Axe 6 (Biodiversité)</label>
                        <input
                            type="text"
                            name="rubrique_axe6"
                            value={formData.rubrique_axe6 || ''}
                            onChange={handleChange}
                            className={styles.input}
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Cotation Axe 6</label>
                        <select
                            name="cotation_axe6"
                            value={formData.cotation_axe6 || ''}
                            onChange={handleChange}
                            className={styles.select}
                        >
                            <option value="">Sélectionner...</option>
                            <option value="FAVORABLE">FAVORABLE</option>
                            <option value="DEFAVORABLE">DEFAVORABLE</option>
                            <option value="NEUTRE">NEUTRE</option>
                            <option value="A_APPROFONDIR">A_APPROFONDIR</option>
                        </select>
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Justification Axe 6</label>
                        <textarea
                            name="justification_axe6"
                            value={formData.justification_axe6 || ''}
                            onChange={handleChange}
                            className={styles.textarea}
                        />
                    </div>

                    <div className={styles.formGroup}>
                        <label className={styles.label}>Commentaire Agent</label>
                        <textarea
                            name="commentaire_agent"
                            value={formData.commentaire_agent || ''}
                            onChange={handleChange}
                            className={styles.textarea}
                        />
                    </div>

                    <div className={styles.modalActions}>
                        <button type="button" onClick={onClose} className={styles.buttonSecondary}>Annuler</button>
                        <button type="submit" className={styles.buttonPrimary}>Enregistrer</button>
                    </div>
                </form>
            </div>
        </div>
    );
};
