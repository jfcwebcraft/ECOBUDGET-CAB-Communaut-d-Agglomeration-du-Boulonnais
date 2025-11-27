import React from 'react';
import * as styles from '../styles.css';
import clsx from 'clsx';

interface BudgetLine {
    libelle: string;
    montant_ht: number;
    nature: string;
    fonction: string;
    rubrique_axe1: string;
    cotation_axe1: string;
    justification_axe1: string;
    rubrique_axe6: string;
    cotation_axe6: string;
    justification_axe6: string;
    statut: string;
}

interface BudgetTableProps {
    data: BudgetLine[];
    onValidate: (index: number) => void;
    onCorrect: (index: number) => void;
}

const getBadgeStyle = (cotation: string) => {
    switch (cotation) {
        case 'FAVORABLE': return styles.badgeFavorable;
        case 'DEFAVORABLE': return styles.badgeDefavorable;
        case 'NEUTRE': return styles.badgeNeutre;
        case 'A_APPROFONDIR': return styles.badgeApprofondir;
        default: return styles.badgeNeutre;
    }
};

export const BudgetTable: React.FC<BudgetTableProps> = ({ data, onValidate, onCorrect }) => {
    if (!data || data.length === 0) return null;

    return (
        <div className={styles.tableContainer}>
            <table className={styles.table}>
                <thead>
                    <tr>
                        <th className={styles.th}>Libellé</th>
                        <th className={styles.th}>Montant HT</th>
                        <th className={styles.th}>Nature / Fonction</th>
                        <th className={styles.th}>Axe 1 (Climat)</th>
                        <th className={styles.th}>Axe 6 (Biodiversité)</th>
                        <th className={styles.th}>Statut</th>
                        <th className={styles.th}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={index}>
                            <td className={styles.td}>{row.libelle}</td>
                            <td className={styles.td}>{row.montant_ht.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })}</td>
                            <td className={styles.td}>
                                <div>{row.nature}</div>
                                <div style={{ fontSize: '0.8rem', color: '#7f8c8d' }}>{row.fonction}</div>
                            </td>
                            <td className={styles.td}>
                                <span className={clsx(styles.badge, getBadgeStyle(row.cotation_axe1))}>
                                    {row.cotation_axe1}
                                </span>
                                {row.rubrique_axe1 && <div style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>{row.rubrique_axe1}</div>}
                            </td>
                            <td className={styles.td}>
                                <span className={clsx(styles.badge, getBadgeStyle(row.cotation_axe6))}>
                                    {row.cotation_axe6}
                                </span>
                                {row.rubrique_axe6 && <div style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>{row.rubrique_axe6}</div>}
                            </td>
                            <td className={styles.td}>{row.statut}</td>
                            <td className={styles.td}>
                                <button className={clsx(styles.button, styles.buttonPrimary)} onClick={() => onValidate(index)}>
                                    Valider
                                </button>
                                <button className={clsx(styles.button, styles.buttonSecondary)} onClick={() => onCorrect(index)}>
                                    Corriger
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};
