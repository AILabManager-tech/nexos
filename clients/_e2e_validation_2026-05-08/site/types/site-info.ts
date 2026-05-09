export interface SiteInfo {
  legalName: string;
  city: string;
  streetAddress: string;
  postalCode: string;
  country: string;
  region: string;
  phone: string;
  email: string;
  rppName: string;
  rppEmail: string;
  rppTitle: string;
  neq: string;
  geo: {
    latitude: number;
    longitude: number;
  };
}

export interface DayHours {
  day: 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday' | 'saturday' | 'sunday';
  open: string;
  close: string;
  closed?: boolean;
}

export interface Holiday {
  date: string;
  name_fr: string;
  name_en: string;
  closed: boolean;
}

export interface HoursConfig {
  weekly: DayHours[];
  holidays: Holiday[];
}
