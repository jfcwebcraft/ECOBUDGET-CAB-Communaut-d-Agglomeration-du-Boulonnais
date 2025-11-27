CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS budget_lines (
    exercice INTEGER NOT NULL,
    num_bordereau INTEGER NOT NULL,
    num_piece INTEGER NOT NULL,
    
    libelle TEXT,
    montant_ht NUMERIC(15, 2),
    montant_tva NUMERIC(15, 2),
    montant_ttc NUMERIC(15, 2),
    tiers TEXT,
    nature TEXT,
    fonction TEXT,
    operation TEXT,
    service TEXT,
    gestionnaire TEXT,

    rubrique_axe1 TEXT,
    cotation_axe1 TEXT, -- 'FAVORABLE', 'DEFAVORABLE', 'NEUTRE', 'A_APPROFONDIR'
    justification_axe1 TEXT,
    
    rubrique_axe6 TEXT,
    cotation_axe6 TEXT,
    justification_axe6 TEXT,

    statut TEXT DEFAULT 'A_TRAITER', -- 'A_TRAITER', 'VALIDE', 'A_APPROFONDIR'
    commentaire_agent TEXT,

    PRIMARY KEY (exercice, num_bordereau, num_piece)
);
