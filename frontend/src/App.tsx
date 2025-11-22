import { useState } from 'react'

function App() {
    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-green-700">ECOBUDGET-CAB</h1>
                <p className="text-gray-600">Outil d'analyse budgétaire vert</p>
            </header>

            <main className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold mb-4">Bienvenue</h2>
                <p>Le système est en cours d'initialisation.</p>
            </main>
        </div>
    )
}

export default App
