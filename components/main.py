
import React, { useState, useEffect } from 'react';
import { APHRecord, RiskPriority, OutcomeStatus, VTRType, AtendimentoClassification, ABCDEData, SAMPLAData, RiskManagementData, NursingImplementationData, SBAROutcome, MedicalTeam } from '../types';

interface APHFormProps {
  onSave: (record: APHRecord) => void;
}

export const APHForm: React.FC<APHFormProps> = ({ onSave }) => {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    patientName: '',
    patientBirthDate: '',
    motherName: '',
    patientAge: 0,
    triggerId: '',
    triggerTime: '08:00',
    arrivalTime: '08:10',
    vtrType: VTRType.USB,
    atendimentoClassification: AtendimentoClassification.Imediato,
    healthInsurance: '',
    collectedCI: false,
    numberOfTriggers: 1,
    location: '',
    priority: RiskPriority.Verde,
    painScale: 0,
    temperature: '',
    glucose: '',
    mainComplaint: '',
    observations: ''
  });

  const [abcde, setAbcde] = useState<ABCDEData>({
    airway: '', cervicalStabilized: '', breathing: '', satO2: '', mv: '', pa: '', fc: '', skin: '', glasgow: '', pupils: '', exposureConditions: [], exposureLocal: ''
  });

  const [sampla, setSampla] = useState<SAMPLAData>({
    symptoms: '', allergies: '', medications: '', pastMedicalHistory: '', liquidsFoods: '', environment: ''
  });

  const [riskManagement, setRiskManagement] = useState<RiskManagementData>({
    identificationChecked: false,
    confirmedWith: '',
    confirmedName: '',
    confirmedBirthDate: '',
    fallRiskActive: false,
    fallPreventions: [],
    bronchoaspirationRiskActive: false,
    bronchoaspirationPreventions: [],
    medicationSafetyActive: false,
    medicationSafetyChecks: []
  });

  const [nursingImplementation, setNursingImplementation] = useState<NursingImplementationData>({
    procedures: [],
    medicationsSolutions: '',
    medicationTime: '',
    evolutionResponse: ''
  });

  const [sbarOutcome, setSbarOutcome] = useState<SBAROutcome>({
    situation: '',
    destinationHospital: '',
    handoverReport: ''
  });

  const [team, setTeam] = useState<MedicalTeam>({
    driverName: '',
    nurseName: '',
    nurseCoren: '',
    doctorName: '',
    doctorCrm: ''
  });

  const [locating, setLocating] = useState(false);
  const [trl, setTrl] = useState(0);
  const [kpiTarget, setKpiTarget] = useState('');

  // Sincronização de TRL e KPI
  useEffect(() => {
    const [tH, tM] = formData.triggerTime.split(':').map(Number);
    const [aH, aM] = formData.arrivalTime.split(':').map(Number);
    const triggerInMinutes = tH * 60 + tM;
    const arrivalInMinutes = aH * 60 + aM;
    let diff = arrivalInMinutes - triggerInMinutes;
    if (diff < 0) diff += 1440;
    setTrl(diff);
    setKpiTarget(formData.vtrType === VTRType.USA ? '< 15 minutos' : '< 30 minutos');
  }, [formData.triggerTime, formData.arrivalTime, formData.vtrType]);

  // Cálculo automático da idade baseado na data de nascimento
  useEffect(() => {
    if (formData.patientBirthDate) {
      const birth = new Date(formData.patientBirthDate);
      const today = new Date();
      let age = today.getFullYear() - birth.getFullYear();
      const m = today.getMonth() - birth.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
        age--;
      }
      setFormData(prev => ({ ...prev, patientAge: Math.max(0, age) }));
    }
  }, [formData.patientBirthDate]);

  const captureGPS = () => {
    setLocating(true);
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          setFormData(prev => ({ ...prev, location: `Lat: ${latitude.toFixed(6)}, Lng: ${longitude.toFixed(6)}` }));
          setLocating(false);
        },
        () => { alert("Erro GPS."); setLocating(false); }
      );
    }
  };

  const handleExposureToggle = (condition: string) => {
    setAbcde(prev => ({
      ...prev,
      exposureConditions: prev.exposureConditions.includes(condition)
        ? prev.exposureConditions.filter(c => c !== condition)
        : [...prev.exposureConditions, condition]
    }));
  };

  const toggleRiskList = (key: keyof RiskManagementData, value: string) => {
    setRiskManagement(prev => {
      const currentList = prev[key] as string[];
      return {
        ...prev,
        [key]: currentList.includes(value)
          ? currentList.filter(v => v !== value)
          : [...currentList, value]
      };
    });
  };

  const toggleProcedure = (procedure: string) => {
    setNursingImplementation(prev => ({
      ...prev,
      procedures: prev.procedures.includes(procedure)
        ? prev.procedures.filter(p => p !== procedure)
        : [...prev.procedures, procedure]
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newRecord: APHRecord = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      ...formData,
      trl,
      kpiTarget,
      abcde,
      sampla,
      riskManagement,
      nursingImplementation,
      outcome: sbarOutcome,
      team
    };
    onSave(newRecord);
    alert('Atendimento salvo com sucesso!');
    // Reset fields
    setFormData({
      date: new Date().toISOString().split('T')[0],
      patientName: '',
      patientBirthDate: '',
      motherName: '',
      patientAge: 0,
      triggerId: '',
      triggerTime: '08:00',
      arrivalTime: '08:10',
      vtrType: VTRType.USB,
      atendimentoClassification: AtendimentoClassification.Imediato,
      healthInsurance: '',
      collectedCI: false,
      numberOfTriggers: 1,
      location: '',
      priority: RiskPriority.Verde,
      painScale: 0,
      temperature: '',
      glucose: '',
      mainComplaint: '',
      observations: ''
    });
    setAbcde({ airway: '', cervicalStabilized: '', breathing: '', satO2: '', mv: '', pa: '', fc: '', skin: '', glasgow: '', pupils: '', exposureConditions: [], exposureLocal: '' });
    setSampla({ symptoms: '', allergies: '', medications: '', pastMedicalHistory: '', liquidsFoods: '', environment: '' });
    setRiskManagement({ identificationChecked: false, confirmedWith: '', confirmedName: '', confirmedBirthDate: '', fallRiskActive: false, fallPreventions: [], bronchoaspirationRiskActive: false, bronchoaspirationPreventions: [], medicationSafetyActive: false, medicationSafetyChecks: [] });
    setNursingImplementation({ procedures: [], medicationsSolutions: '', medicationTime: '', evolutionResponse: '' });
    setSbarOutcome({ situation: '', destinationHospital: '', handoverReport: '' });
    setTeam({ driverName: '', nurseName: '', nurseCoren: '', doctorName: '', doctorCrm: '' });
  };

  const SectionTitle = ({ children }: { children: React.ReactNode }) => (
    <h3 className="text-lg font-bold text-slate-900 border-b border-slate-100 pb-2 mb-4 uppercase tracking-tight flex items-center gap-2">
      {children}
    </h3>
  );

  const SubTitle = ({ children }: { children: React.ReactNode }) => (
    <h4 className="text-sm font-bold text-slate-600 mb-4 mt-2 border-l-4 border-blue-500 pl-2">
      {children}
    </h4>
  );

  const ChoiceButton = ({ label, selected, onClick }: { label: string, selected: boolean, onClick: () => void }) => (
    <button
      type="button"
      onClick={onClick}
      className={`px-3 py-1.5 rounded-md text-xs font-medium border transition-all ${
        selected ? 'bg-blue-600 text-white border-blue-600 shadow-sm' : 'bg-white text-slate-600 border-slate-200 hover:border-blue-300'
      }`}
    >
      {label}
    </button>
  );

  const ManchesterButton = ({ priority }: { priority: RiskPriority }) => {
    const isSelected = formData.priority === priority;
    const colors = {
      [RiskPriority.Vermelho]: isSelected ? 'bg-red-600 text-white border-red-700' : 'bg-white text-red-600 border-red-100 hover:bg-red-50',
      [RiskPriority.Laranja]: isSelected ? 'bg-orange-500 text-white border-orange-600' : 'bg-white text-orange-500 border-orange-100 hover:bg-orange-50',
      [RiskPriority.Amarelo]: isSelected ? 'bg-yellow-400 text-slate-900 border-yellow-500' : 'bg-white text-yellow-600 border-yellow-100 hover:bg-yellow-50',
      [RiskPriority.Verde]: isSelected ? 'bg-green-600 text-white border-green-700' : 'bg-white text-green-600 border-green-100 hover:bg-green-50'
    };

    return (
      <button
        type="button"
        onClick={() => setFormData({ ...formData, priority })}
        className={`flex-1 py-3 px-2 rounded-lg border-2 font-bold text-xs uppercase tracking-tighter transition-all flex flex-col items-center gap-1 shadow-sm ${colors[priority]}`}
      >
        <div className={`w-3 h-3 rounded-full ${isSelected ? 'bg-white' : colors[priority].split(' ')[1].replace('text-', 'bg-')}`}></div>
        {priority}
      </button>
    );
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-8 rounded-xl shadow-sm border border-slate-100 space-y-10 relative">
      <img 
        src="KRSaude.jpg" 
        alt="KRSaude Logo" 
        className="absolute top-8 right-8 w-32 h-auto opacity-90 hidden md:block"
        onError={(e) => { e.currentTarget.style.display = 'none'; }}
      />
      
      {/* SECTION 1 - CONTROLE */}
      <div>
        <SectionTitle>1. DADOS DE CONTROLE E REGULAÇÃO</SectionTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Data</label>
            <input type="date" required className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.date} onChange={e => setFormData({...formData, date: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">ID do Acionamento</label>
            <input type="text" required className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.triggerId} onChange={e => setFormData({...formData, triggerId: e.target.value})} placeholder="Ex: AC-2024-001" />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Tipo de Viatura (VTR)</label>
            <select className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm" value={formData.vtrType} onChange={e => setFormData({...formData, vtrType: e.target.value as VTRType})}>
              {Object.values(VTRType).map(v => <option key={v} value={v}>{v}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Classificação</label>
            <select className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm font-medium text-blue-700" value={formData.atendimentoClassification} onChange={e => setFormData({...formData, atendimentoClassification: e.target.value as AtendimentoClassification})}>
              {Object.values(AtendimentoClassification).map(v => <option key={v} value={v}>{v}</option>)}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Hora Acion.</label>
              <input type="time" required className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm" value={formData.triggerTime} onChange={e => setFormData({...formData, triggerTime: e.target.value})} />
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Hora Cheg.</label>
              <input type="time" required className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none text-sm" value={formData.arrivalTime} onChange={e => setFormData({...formData, arrivalTime: e.target.value})} />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="md:col-span-2">
            <label className="block text-sm font-semibold text-slate-700 mb-1">Convênio</label>
            <input type="text" className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.healthInsurance} onChange={e => setFormData({...formData, healthInsurance: e.target.value})} placeholder="Nome do convênio ou particular..." />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Recolheu C.I.?</label>
              <div className="flex gap-4 mt-2">
                <label className="flex items-center gap-2 text-xs text-slate-600">
                  <input type="radio" checked={formData.collectedCI === true} onChange={() => setFormData({...formData, collectedCI: true})} /> SIM
                </label>
                <label className="flex items-center gap-2 text-xs text-slate-600">
                  <input type="radio" checked={formData.collectedCI === false} onChange={() => setFormData({...formData, collectedCI: false})} /> NÃO
                </label>
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-1">Nº Acion.</label>
              <input type="number" min="1" className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.numberOfTriggers} onChange={e => setFormData({...formData, numberOfTriggers: parseInt(e.target.value) || 1})} />
            </div>
          </div>
        </div>

        <div className="mt-4 flex gap-4">
          <div className="flex-1 bg-blue-50 p-4 rounded-lg flex items-center justify-between border border-blue-100">
             <div>
                <p className="text-xs font-bold text-blue-600 uppercase tracking-widest">Tempo de Resposta (TRL)</p>
                <p className="text-2xl font-black text-blue-800">{trl} min</p>
             </div>
             <i className="fas fa-stopwatch text-blue-300 text-3xl"></i>
          </div>
          <div className="flex-1 bg-slate-50 p-4 rounded-lg border border-slate-200">
             <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">KPI Alvo</p>
             <p className={`text-xl font-bold ${trl > (formData.vtrType === VTRType.USA ? 15 : 30) ? 'text-red-500' : 'text-green-600'}`}>
                {kpiTarget}
             </p>
          </div>
        </div>
      </div>

      {/* SECTION 2 - IDENTIFICAÇÃO (ATUALIZADO) */}
      <div>
        <SectionTitle>2. IDENTIFICAÇÃO DO PACIENTE</SectionTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-2">
            <label className="block text-sm font-semibold text-slate-700 mb-1">Nome Completo</label>
            <input type="text" required className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.patientName} onChange={e => setFormData({...formData, patientName: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Data de Nascimento</label>
            <input type="date" required className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.patientBirthDate} onChange={e => setFormData({...formData, patientBirthDate: e.target.value})} />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-1">Idade</label>
            <input type="number" readOnly className="w-full p-2.5 bg-slate-100 border border-slate-200 rounded-lg outline-none text-sm font-bold text-blue-800 cursor-not-allowed" value={formData.patientAge} />
          </div>
          <div className="lg:col-span-2">
            <label className="block text-sm font-semibold text-slate-700 mb-1">Nome da Mãe/Genitora</label>
            <input type="text" className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.motherName} onChange={e => setFormData({...formData, motherName: e.target.value})} placeholder="Texto Curto" />
          </div>
        </div>
        {/* Localização em linha separada */}
        <div className="mt-6">
          <label className="block text-sm font-semibold text-slate-700 mb-1">Localização (GPS/Endereço)</label>
          <div className="flex gap-2">
            <input type="text" className="flex-1 p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs" value={formData.location} onChange={e => setFormData({...formData, location: e.target.value})} placeholder="Endereço ou GPS" />
            <button type="button" onClick={captureGPS} disabled={locating} className="p-2.5 bg-slate-900 text-white rounded-lg hover:bg-slate-700 transition-all shadow-lg">
              {locating ? <i className="fas fa-spinner fa-spin"></i> : <i className="fas fa-map-marker-alt"></i>}
            </button>
          </div>
        </div>
      </div>

      {/* SECTION 3 - ABCDE */}
      <div>
        <SectionTitle>3. EXAME FÍSICO ESTRUTURADO (PROTOCOLOS GLOBAIS)</SectionTitle>
        <SubTitle>A. Avaliação Primária (ABCDE)</SubTitle>
        <div className="space-y-4 bg-slate-50 p-6 rounded-xl border border-slate-200">
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-sm font-bold text-blue-800 w-32">A (Vias Aéreas):</span>
            <div className="flex gap-2">{['Pérvias', 'Obstruídas'].map(v => (<ChoiceButton key={v} label={v} selected={abcde.airway === v} onClick={() => setAbcde({...abcde, airway: v})} />))}</div>
            <div className="flex items-center gap-2 ml-4"><span className="text-xs text-slate-500 font-bold">Cervical Estabilizada?</span>{['S', 'N'].map(v => (<ChoiceButton key={v} label={v} selected={abcde.cervicalStabilized === v} onClick={() => setAbcde({...abcde, cervicalStabilized: v})} />))}</div>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-sm font-bold text-blue-800 w-32">B (Respiração):</span>
            <div className="flex gap-2">{['Regular', 'Dispneico'].map(v => (<ChoiceButton key={v} label={v} selected={abcde.breathing === v} onClick={() => setAbcde({...abcde, breathing: v})} />))}</div>
            <div className="flex items-center gap-2 ml-4"><span className="text-xs text-slate-500 font-bold">SatO2:</span><input type="text" className="w-16 p-1 bg-white border border-slate-200 rounded text-center text-xs" placeholder="%" value={abcde.satO2} onChange={e => setAbcde({...abcde, satO2: e.target.value})} /></div>
            <div className="flex items-center gap-2"><span className="text-xs text-slate-500 font-bold">MV:</span>{['Presente', 'Diminuído'].map(v => (<ChoiceButton key={v} label={v} selected={abcde.mv === v} onClick={() => setAbcde({...abcde, mv: v})} />))}</div>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-sm font-bold text-blue-800 w-32">C (Circulação):</span>
            <div className="flex items-center gap-2"><span className="text-xs text-slate-500 font-bold">PA:</span><input type="text" className="w-20 p-1 bg-white border border-slate-200 rounded text-center text-xs" placeholder="00x00" value={abcde.pa} onChange={e => setAbcde({...abcde, pa: e.target.value})} /></div>
            <div className="flex items-center gap-2"><span className="text-xs text-slate-500 font-bold">FC:</span><input type="text" className="w-16 p-1 bg-white border border-slate-200 rounded text-center text-xs" placeholder="bpm" value={abcde.fc} onChange={e => setAbcde({...abcde, fc: e.target.value})} /></div>
            <div className="flex items-center gap-2 ml-4"><span className="text-xs text-slate-500 font-bold">Pele:</span>{['Corada', 'Cianótica', 'Pálida'].map(v => (<ChoiceButton key={v} label={v} selected={abcde.skin === v} onClick={() => setAbcde({...abcde, skin: v})} />))}</div>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-sm font-bold text-blue-800 w-32">D (Neurologia):</span>
            <div className="flex items-center gap-2"><span className="text-xs text-slate-500 font-bold">Glasgow:</span><input type="text" className="w-16 p-1 bg-white border border-slate-200 rounded text-center text-xs font-bold" placeholder=" /15" value={abcde.glasgow} onChange={e => setAbcde({...abcde, glasgow: e.target.value})} /></div>
            <div className="flex items-center gap-2 ml-4"><span className="text-xs text-slate-500 font-bold">Pupilas:</span>{['Isocóricas', 'Fotorreagentes'].map(v => (<ChoiceButton key={v} label={v} selected={abcde.pupils === v} onClick={() => setAbcde({...abcde, pupils: v})} />))}</div>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-sm font-bold text-blue-800 w-32">E (Exposição):</span>
            <div className="flex gap-2">{['Escoriações', 'Fraturas', 'Edemas'].map(v => (<ChoiceButton key={v} label={v} selected={abcde.exposureConditions.includes(v)} onClick={() => handleExposureToggle(v)} />))}</div>
            <div className="flex items-center gap-2 ml-4 flex-1"><span className="text-xs text-slate-500 font-bold">Local:</span><input type="text" className="flex-1 min-w-[200px] p-1 bg-white border border-slate-200 rounded text-xs" value={abcde.exposureLocal} onChange={e => setAbcde({...abcde, exposureLocal: e.target.value})} /></div>
          </div>
        </div>

        <SubTitle>B. Avaliação de Sinais Vitais e Dor</SubTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 bg-slate-50 p-6 rounded-xl border border-slate-200">
          <div><label className="block text-xs font-bold text-slate-500 uppercase mb-1">Temperatura</label><input type="text" className="w-full p-2 bg-white border border-slate-200 rounded-lg text-sm" placeholder="°C" value={formData.temperature} onChange={e => setFormData({...formData, temperature: e.target.value})} /></div>
          <div><label className="block text-xs font-bold text-slate-500 uppercase mb-1">Glicemia</label><input type="text" className="w-full p-2 bg-white border border-slate-200 rounded-lg text-sm" placeholder="mg/dL" value={formData.glucose} onChange={e => setFormData({...formData, glucose: e.target.value})} /></div>
          <div className="md:col-span-2">
            <label className="block text-xs font-bold text-slate-500 uppercase mb-2">Avaliação da DOR (Escala Visual)</label>
            <div className="flex justify-between items-center gap-1">
              {[0,1,2,3,4,5,6,7,8,9,10].map(n => (<button key={n} type="button" onClick={() => setFormData({...formData, painScale: n})} className={`w-7 h-7 sm:w-8 sm:h-8 rounded flex items-center justify-center text-[10px] font-bold transition-all ${formData.painScale === n ? 'bg-red-500 text-white shadow-lg scale-110' : 'bg-white text-slate-400 border border-slate-200'}`}>{n}</button>))}
            </div>
          </div>
          <div className="lg:col-span-4 mt-2"><label className="block text-xs font-bold text-slate-500 uppercase mb-1">Queixa Principal</label><textarea rows={2} className="w-full p-2.5 bg-white border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 text-sm" value={formData.mainComplaint} onChange={e => setFormData({...formData, mainComplaint: e.target.value})} placeholder="Descreva a queixa..." /></div>
        </div>
      </div>

      {/* SECTION 4 - SAMPLA */}
      <div>
        <SectionTitle>4. HISTÓRICO CLÍNICO (S.A.M.P.L.A)</SectionTitle>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50 p-6 rounded-xl border border-slate-200">
          {[
            { label: 'S (Sintomas)', key: 'symptoms' },
            { label: 'A (Alergias)', key: 'allergies' },
            { label: 'M (Medicamentos)', key: 'medications' },
            { label: 'P (Passado Médico)', key: 'pastMedicalHistory' },
            { label: 'L (Líquidos/Alimentos)', key: 'liquidsFoods' },
            { label: 'A (Ambiente do Evento)', key: 'environment' }
          ].map(field => (
            <div key={field.key}>
              <label className="block text-xs font-bold text-slate-500 uppercase mb-1">{field.label}</label>
              <textarea 
                rows={3} 
                className="w-full p-2.5 bg-white border border-slate-200 rounded-lg outline-none text-sm focus:ring-2 focus:ring-blue-500" 
                value={(sampla as any)[field.key]} 
                onChange={e => setSampla({...sampla, [field.key]: e.target.value})}
              />
            </div>
          ))}
        </div>
      </div>

      {/* SECTION 5 - RISCOS */}
      <div>
        <SectionTitle>5. GERENCIAMENTO DE RISCOS ASSISTENCIAIS</SectionTitle>
        <div className="space-y-6 bg-slate-50 p-6 rounded-xl border border-slate-200">
          <div className="flex flex-col gap-4 border-b border-slate-200 pb-4">
            <div className="flex items-center gap-3">
              <input type="checkbox" className="w-5 h-5 accent-blue-600" checked={riskManagement.identificationChecked} onChange={e => setRiskManagement({...riskManagement, identificationChecked: e.target.checked})} />
              <span className="text-sm font-bold text-slate-700">Protocolo de Identificação Verificado</span>
            </div>
          </div>
          <div className="flex flex-col gap-4 border-b border-slate-200 pb-4">
            <div className="flex items-center gap-3">
              <input type="checkbox" className="w-5 h-5 accent-blue-600" checked={riskManagement.fallRiskActive} onChange={e => setRiskManagement({...riskManagement, fallRiskActive: e.target.checked})} />
              <span className="text-sm font-bold text-slate-700">Risco de Queda Detectado</span>
            </div>
            {riskManagement.fallRiskActive && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pl-8 animate-in slide-in-from-left duration-200">
                {['Grades elevadas', 'Cinto de segurança', 'Pulseira de risco', 'Orientação paciente/familiar'].map(opt => (<ChoiceButton key={opt} label={opt} selected={riskManagement.fallPreventions.includes(opt)} onClick={() => toggleRiskList('fallPreventions', opt)} />))}
              </div>
            )}
          </div>
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-3">
              <input type="checkbox" className="w-5 h-5 accent-blue-600" checked={riskManagement.medicationSafetyActive} onChange={e => setRiskManagement({...riskManagement, medicationSafetyActive: e.target.checked})} />
              <span className="text-sm font-bold text-slate-700">Segurança Medicamentosa (9 Certos)</span>
            </div>
          </div>
        </div>
      </div>

      {/* SECTION 6 - ENFERMAGEM */}
      <div>
        <SectionTitle>6. IMPLEMENTAÇÃO DA ASSISTÊNCIA (ENFERMAGEM)</SectionTitle>
        <div className="space-y-6 bg-slate-50 p-6 rounded-xl border border-slate-200">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Procedimentos Realizados</label>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
              {['Acesso Venoso', 'Oxigênio (O2)', 'Imobilização', 'Curativo', 'Monitorização'].map(proc => (
                <ChoiceButton 
                  key={proc} 
                  label={proc} 
                  selected={nursingImplementation.procedures.includes(proc)} 
                  onClick={() => toggleProcedure(proc)} 
                />
              ))}
            </div>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-1">Evolução e Resposta ao Tratamento</label>
            <textarea 
              rows={3}
              className="w-full p-2.5 bg-white border border-slate-200 rounded-lg outline-none text-sm focus:ring-2 focus:ring-blue-500" 
              value={nursingImplementation.evolutionResponse}
              onChange={e => setNursingImplementation({...nursingImplementation, evolutionResponse: e.target.value})}
              placeholder="Descreva a estabilização e evolução clínica..."
            />
          </div>
        </div>
      </div>

      {/* SECTION 7 - SBAR */}
      <div>
        <SectionTitle>7. DESFECHO (MÉTODO SBAR)</SectionTitle>
        <div className="space-y-6 bg-slate-50 p-6 rounded-xl border border-slate-200">
          <div className="border-b border-slate-200 pb-6">
            <SubTitle>CLASSIFICAÇÃO DO ATENDIMENTO</SubTitle>
            <label className="block text-xs font-bold text-slate-500 uppercase mb-3">Manchester: Prioridade Final</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {Object.values(RiskPriority).map(priority => (
                <ManchesterButton key={priority} priority={priority} />
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Situação Final</label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
              {Object.values(OutcomeStatus).map(status => (
                <ChoiceButton 
                  key={status} 
                  label={status} 
                  selected={sbarOutcome.situation === status} 
                  onClick={() => setSbarOutcome({...sbarOutcome, situation: status})} 
                />
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-xs font-bold text-slate-500 uppercase mb-1">Hospital de Destino</label><textarea rows={2} className="w-full p-2.5 bg-white border border-slate-200 rounded-lg outline-none text-sm" value={sbarOutcome.destinationHospital} onChange={e => setSbarOutcome({...sbarOutcome, destinationHospital: e.target.value})} /></div>
            <div><label className="block text-xs font-bold text-slate-500 uppercase mb-1">Passagem de Plantão</label><input type="text" className="w-full p-2.5 bg-white border border-slate-200 rounded-lg outline-none text-sm" value={sbarOutcome.handoverReport} onChange={e => setSbarOutcome({...sbarOutcome, handoverReport: e.target.value})} /></div>
          </div>

          <div className="border-t border-slate-200 pt-6">
            <p className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
              <i className="fas fa-users text-blue-500"></i> Equipe KRSaude
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <label className="block text-[10px] font-bold text-slate-400 uppercase">Condutor</label>
                <input type="text" className="w-full text-xs font-medium outline-none" value={team.driverName} onChange={e => setTeam({...team, driverName: e.target.value})} placeholder="Nome" />
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <label className="block text-[10px] font-bold text-slate-400 uppercase">Enfermeiro</label>
                <input type="text" className="w-full text-xs font-medium outline-none" value={team.nurseName} onChange={e => setTeam({...team, nurseName: e.target.value})} placeholder="Nome" />
              </div>
              <div className="bg-white p-3 rounded-lg border border-slate-200">
                <label className="block text-[10px] font-bold text-slate-400 uppercase">Médico</label>
                <input type="text" className="w-full text-xs font-medium outline-none" value={team.doctorName} onChange={e => setTeam({...team, doctorName: e.target.value})} placeholder="Nome" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="pt-6">
        <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-black py-4 px-6 rounded-xl shadow-xl transition-all flex items-center justify-center gap-3 text-lg uppercase tracking-tight">
          <i className="fas fa-cloud-upload-alt"></i> Sincronizar Ficha APH Cloud
        </button>
      </div>
    </form>
  );
};
