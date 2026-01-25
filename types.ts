
export enum RiskPriority {
  Verde = 'Verde',
  Amarelo = 'Amarelo',
  Laranja = 'Laranja',
  Vermelho = 'Vermelho'
}

export enum OutcomeStatus {
  EstabilizadoLocal = 'Estabilizado no Local',
  RemovidoHospital = 'Removido para Hospital',
  Obito = 'Óbito'
}

export enum VTRType {
  USB = 'Unidade de Suporte Básico (USB)',
  USA = 'Unidade de Suporte Avançado (USA)'
}

export enum AtendimentoClassification {
  Imediato = 'Atendimento Imediato',
  Agendado = 'Atendimento Agendado'
}

export interface ABCDEData {
  airway: string;
  cervicalStabilized: string;
  breathing: string;
  satO2: string;
  mv: string;
  pa: string;
  fc: string;
  skin: string;
  glasgow: string;
  pupils: string;
  exposureConditions: string[];
  exposureLocal: string;
}

export interface SAMPLAData {
  symptoms: string;
  allergies: string;
  medications: string;
  pastMedicalHistory: string;
  liquidsFoods: string;
  environment: string;
}

export interface RiskManagementData {
  identificationChecked: boolean;
  confirmedWith: 'Paciente' | 'Familiar' | '';
  confirmedName: string;
  confirmedBirthDate: string;
  fallRiskActive: boolean;
  fallPreventions: string[];
  bronchoaspirationRiskActive: boolean;
  bronchoaspirationPreventions: string[];
  medicationSafetyActive: boolean;
  medicationSafetyChecks: string[];
}

export interface NursingImplementationData {
  procedures: string[];
  medicationsSolutions: string;
  medicationTime: string;
  evolutionResponse: string;
}

export interface SBAROutcome {
  situation: OutcomeStatus | '';
  destinationHospital: string;
  handoverReport: string;
}

export interface MedicalTeam {
  driverName: string;
  nurseName: string;
  nurseCoren: string;
  doctorName: string;
  doctorCrm: string;
}

export interface APHRecord {
  id: string;
  timestamp: string;
  triggerId: string;
  triggerTime: string;
  arrivalTime: string;
  vtrType: VTRType;
  atendimentoClassification: AtendimentoClassification;
  healthInsurance: string;
  collectedCI: boolean;
  numberOfTriggers: number;
  trl: number;
  kpiTarget: string;
  patientName: string;
  patientAge: number;
  location: string;
  priority: RiskPriority;
  painScale: number;
  outcome: SBAROutcome;
  team: MedicalTeam;
  abcde: ABCDEData;
  sampla: SAMPLAData;
  riskManagement: RiskManagementData;
  nursingImplementation: NursingImplementationData;
  temperature: string;
  glucose: string;
  mainComplaint: string;
  observations: string;
}
