
import React, { useState, useEffect } from 'react';
import { APHForm } from './components/APHForm';
import { Dashboard } from './components/Dashboard';
import { storageService } from './services/storageService';
import { generateInsights } from './services/geminiService';
import { APHRecord } from './types';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'form' | 'dashboard' | 'insights'>('form');
  const [records, setRecords] = useState<APHRecord[]>([]);
  const [insights, setInsights] = useState<string>('');
  const [loadingInsights, setLoadingInsights] = useState(false);

  useEffect(() => {
    setRecords(storageService.getRecords());
  }, []);

  const handleSaveRecord = (record: APHRecord) => {
    storageService.saveRecord(record);
    setRecords(prev => [...prev, record]);
  };

  const handleGenerateInsights = async () => {
    setLoadingInsights(true);
    const result = await generateInsights(records);
    setInsights(result);
    setLoadingInsights(false);
    setActiveTab('insights');
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-3 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white text-xl shadow-lg shadow-blue-100">
              <i className="fas fa-bolt"></i>
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900 tracking-tight">BioConnect APH</h1>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-widest">Cloud Management System</p>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <nav className="flex items-center bg-slate-100 p-1 rounded-xl">
              <button 
                onClick={() => setActiveTab('form')}
                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${activeTab === 'form' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <i className="fas fa-file-medical mr-2"></i> Nova Ficha
              </button>
              <button 
                onClick={() => setActiveTab('dashboard')}
                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${activeTab === 'dashboard' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <i className="fas fa-chart-pie mr-2"></i> Dashboard
              </button>
              <button 
                onClick={handleGenerateInsights}
                className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all ${activeTab === 'insights' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
                disabled={loadingInsights || records.length === 0}
              >
                {loadingInsights ? <i className="fas fa-spinner fa-spin"></i> : <i className="fas fa-lightbulb mr-2"></i>}
                IA Insights
              </button>
            </nav>

            {/* Logo KRSaude no Canto Superior Direito */}
            <img 
              src="KRSaude.jpg" 
              alt="KRSaude" 
              className="h-10 w-auto object-contain hidden lg:block"
              onError={(e) => { e.currentTarget.style.display = 'none'; }}
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-6xl mx-auto w-full px-4 py-8">
        {activeTab === 'form' && (
          <div className="animate-in fade-in duration-500">
            <div className="mb-6 flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">Novo Atendimento</h2>
                <p className="text-slate-500">Preencha os dados do protocolo e sincronize com a central.</p>
              </div>
            </div>
            <APHForm onSave={handleSaveRecord} />
          </div>
        )}

        {activeTab === 'dashboard' && (
          <div className="animate-in fade-in duration-500">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">Visão Geral do Gestor</h2>
                <p className="text-slate-500">Indicadores de performance e volumetria em tempo real.</p>
              </div>
              <button 
                onClick={() => { if(confirm('Limpar histórico?')) { storageService.clearAll(); setRecords([]); } }}
                className="text-xs text-red-500 hover:underline"
              >
                Limpar Banco de Dados
              </button>
            </div>
            <Dashboard records={records} />
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="animate-in slide-in-from-bottom duration-500">
            <div className="bg-white p-8 rounded-2xl shadow-xl border border-blue-50 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-8 opacity-5 text-8xl text-blue-600">
                <i className="fas fa-brain"></i>
              </div>
              <h2 className="text-2xl font-bold text-slate-800 mb-6 flex items-center gap-3">
                <i className="fas fa-wand-magic-sparkles text-blue-500"></i> Análise Inteligente Gemini
              </h2>
              <div className="prose prose-slate max-w-none">
                {insights.split('\n').map((line, i) => (
                  <p key={i} className="mb-2 text-slate-700 leading-relaxed">
                    {line}
                  </p>
                ))}
              </div>
              <button 
                onClick={() => setActiveTab('dashboard')}
                className="mt-8 text-blue-600 font-bold flex items-center gap-2 hover:gap-3 transition-all"
              >
                Voltar ao Dashboard <i className="fas fa-arrow-right"></i>
              </button>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-100 py-6">
        <div className="max-w-6xl mx-auto px-4 flex justify-between items-center text-slate-400 text-xs uppercase tracking-widest font-bold">
          <span>&copy; 2024 BIOCONNECT HEALTH TECH</span>
          <div className="flex items-center gap-4">
            <img 
              src="KRSaude.jpg" 
              alt="KRSaude" 
              className="h-6 w-auto opacity-50 grayscale hover:grayscale-0 transition-all"
              onError={(e) => { e.currentTarget.style.display = 'none'; }}
            />
            <span className="flex items-center gap-1"><i className="fas fa-shield-halved"></i> GDPR COMPLIANT</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
