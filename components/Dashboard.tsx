
import React, { useMemo } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
  PieChart, Pie, Cell
} from 'recharts';
import { APHRecord, RiskPriority, VTRType } from '../types';

interface DashboardProps {
  records: APHRecord[];
}

const COLORS = {
  [RiskPriority.Verde]: '#22c55e',
  [RiskPriority.Amarelo]: '#eab308',
  [RiskPriority.Laranja]: '#f97316',
  [RiskPriority.Vermelho]: '#ef4444',
};

const VTR_COLORS = ['#3b82f6', '#8b5cf6'];

export const Dashboard: React.FC<DashboardProps> = ({ records }) => {
  const stats = useMemo(() => {
    const total = records.length;
    if (total === 0) return null;

    const avgTrl = records.reduce((acc, curr) => acc + curr.trl, 0) / total;
    
    const kpiMet = records.filter(r => {
      const target = r.vtrType === VTRType.USA ? 15 : 30;
      return r.trl <= target;
    }).length;

    const priorityCounts = Object.values(RiskPriority).map(p => ({
      name: p,
      value: records.filter(r => r.priority === p).length
    }));

    const vtrPerformance = Object.values(VTRType).map(type => {
      const vRecords = records.filter(r => r.vtrType === type);
      return {
        name: type === VTRType.USA ? 'USA' : 'USB',
        avgTrl: vRecords.length > 0 ? vRecords.reduce((a, b) => a + b.trl, 0) / vRecords.length : 0
      };
    });

    return { total, avgTrl, kpiMet, priorityCounts, vtrPerformance };
  }, [records]);

  if (!stats) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-slate-400">
        <i className="fas fa-chart-line text-4xl mb-4"></i>
        <p>Aguardando dados para gerar o dashboard...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Atendimentos</p>
          <p className="text-3xl font-black text-slate-900">{stats.total}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">TRL Médio (Geral)</p>
          <p className="text-3xl font-black text-blue-600">{stats.avgTrl.toFixed(1)} <span className="text-lg">min</span></p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Adesão KPI Alvo</p>
          <p className="text-3xl font-black text-green-600">{((stats.kpiMet / stats.total) * 100).toFixed(0)}%</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <h3 className="text-lg font-black mb-6 uppercase tracking-tight text-slate-800">Volumetria Manchester</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats.priorityCounts}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {stats.priorityCounts.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[entry.name as RiskPriority]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
          <h3 className="text-lg font-black mb-6 uppercase tracking-tight text-slate-800">Eficiência por VTR (TRL)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.vtrPerformance}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis label={{ value: 'Minutos', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Bar dataKey="avgTrl" radius={[4, 4, 0, 0]}>
                  {stats.vtrPerformance.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={VTR_COLORS[index % VTR_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
