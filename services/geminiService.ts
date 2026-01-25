
import { GoogleGenAI } from "@google/genai";
import { APHRecord } from "../types";

export const generateInsights = async (records: APHRecord[]): Promise<string> => {
  if (records.length === 0) return "Nenhum dado disponível para análise.";

  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || "" });
  
  const summaryData = records.map(r => ({
    vtr: r.vtrType,
    classificacao_geral: r.atendimentoClassification,
    convenio: r.healthInsurance,
    numero_acionamentos: r.numberOfTriggers,
    prioridade_manchester: r.priority,
    trl: r.trl,
    kpi_alvo: r.kpiTarget,
    desfecho_sbar: r.outcome,
    equipe: r.team,
    idade: r.patientAge,
    queixa: r.mainComplaint,
    sampla: r.sampla,
    riscos: r.riskManagement,
    exame_primario: r.abcde,
    sinais: { temp: r.temperature, glicemia: r.glucose, dor: r.painScale },
    implementacao: r.nursingImplementation
  }));

  const prompt = `
    Como um consultor sênior de gestão hospitalar e especialista em APH, analise os seguintes dados detalhados de atendimentos recentes:
    ${JSON.stringify(summaryData)}

    Forneça um relatório executivo estruturado em Markdown com:
    1. Análise da gravidade clínica vs. tempo de resposta (TRL) e adesão ao KPI, considerando atendimentos imediatos e agendados.
    2. Identificação de padrões nas queixas principais, histórico clínico (SAMPLA), convênios e riscos assistenciais.
    3. Avaliação dos desfechos via método SBAR e correlação com o tipo de VTR e equipe alocada.
    4. Recomendações para aprimorar o atendimento clínico com base nos sinais vitais e protocolos de segurança.
    5. Sugestões operacionais para otimizar o uso das VTRs e gestão da equipe frente aos perfis de risco e demanda de agendamento.
    
    Responda em Português do Brasil de forma clara e profissional.
  `;

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: prompt,
    });
    return response.text || "Não foi possível gerar insights no momento.";
  } catch (error) {
    console.error("Gemini API Error:", error);
    return "Erro ao conectar com o motor de IA. Verifique as configurações.";
  }
};
