import { style } from '@vanilla-extract/css';

export const container = style({
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem',
});

export const header = style({
    marginBottom: '2rem',
    textAlign: 'center',
});

export const title = style({
    fontSize: '2.5rem',
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: '0.5rem',
});

export const subtitle = style({
    fontSize: '1.2rem',
    color: '#7f8c8d',
});

export const uploadZone = style({
    border: '2px dashed #bdc3c7',
    borderRadius: '8px',
    padding: '3rem',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'border-color 0.3s ease, background-color 0.3s ease',
    marginBottom: '2rem',
    ':hover': {
        borderColor: '#3498db',
        backgroundColor: '#f0f8ff',
    },
});

export const uploadActive = style({
    borderColor: '#2ecc71',
    backgroundColor: '#e8f8f5',
});

export const tableContainer = style({
    overflowX: 'auto',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    borderRadius: '8px',
    backgroundColor: 'white',
});

export const table = style({
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '0.9rem',
});

export const th = style({
    backgroundColor: '#f8f9fa',
    color: '#2c3e50',
    fontWeight: '600',
    padding: '1rem',
    textAlign: 'left',
    borderBottom: '2px solid #ecf0f1',
});

export const td = style({
    padding: '1rem',
    borderBottom: '1px solid #ecf0f1',
    color: '#34495e',
});

export const badge = style({
    padding: '0.25rem 0.5rem',
    borderRadius: '4px',
    fontSize: '0.8rem',
    fontWeight: '600',
    textTransform: 'uppercase',
});

export const badgeFavorable = style({
    backgroundColor: '#d4edda',
    color: '#155724',
});

export const badgeDefavorable = style({
    backgroundColor: '#f8d7da',
    color: '#721c24',
});

export const badgeNeutre = style({
    backgroundColor: '#e2e3e5',
    color: '#383d41',
});

export const badgeApprofondir = style({
    backgroundColor: '#fff3cd',
    color: '#856404',
});

export const button = style({
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: '500',
    transition: 'background-color 0.2s',
    marginRight: '0.5rem',
});

export const buttonPrimary = style({
    backgroundColor: '#3498db',
    color: 'white',
    ':hover': {
        backgroundColor: '#2980b9',
    },
});

export const buttonSecondary = style({
    backgroundColor: '#95a5a6',
    color: 'white',
    ':hover': {
        backgroundColor: '#7f8c8d',
    },
});

export const modalOverlay = style({
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
});

export const modalContent = style({
    backgroundColor: 'white',
    padding: '2rem',
    borderRadius: '8px',
    width: '90%',
    maxWidth: '600px',
    maxHeight: '90vh',
    overflowY: 'auto',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
});

export const formGroup = style({
    marginBottom: '1rem',
});

export const label = style({
    display: 'block',
    marginBottom: '0.5rem',
    fontWeight: '600',
    color: '#2c3e50',
});

export const input = style({
    width: '100%',
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #bdc3c7',
    fontSize: '1rem',
    ':focus': {
        borderColor: '#3498db',
        outline: 'none',
    },
});

export const select = style({
    width: '100%',
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #bdc3c7',
    fontSize: '1rem',
    backgroundColor: 'white',
    ':focus': {
        borderColor: '#3498db',
        outline: 'none',
    },
});

export const textarea = style({
    width: '100%',
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #bdc3c7',
    fontSize: '1rem',
    minHeight: '100px',
    resize: 'vertical',
    ':focus': {
        borderColor: '#3498db',
        outline: 'none',
    },
});

export const modalActions = style({
    display: 'flex',
    justifyContent: 'flex-end',
    marginTop: '2rem',
    gap: '1rem',
});
