
import { APHRecord } from '../types';

const STORAGE_KEY = 'bioconnect_aph_records';

export const storageService = {
  saveRecord: (record: APHRecord): void => {
    const records = storageService.getRecords();
    records.push(record);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
  },

  getRecords: (): APHRecord[] => {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  },

  clearAll: (): void => {
    localStorage.removeItem(STORAGE_KEY);
  }
};
