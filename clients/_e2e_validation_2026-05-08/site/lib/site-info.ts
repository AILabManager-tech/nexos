import siteInfoData from '@/site/data/site-info.json';
import horairesData from '@/site/data/horaires.json';
import type { HoursConfig, SiteInfo } from '@/types/site-info';

export function getSiteInfo(): SiteInfo {
  return siteInfoData as SiteInfo;
}

export function getHours(): HoursConfig {
  return horairesData as HoursConfig;
}

export const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL ?? 'https://depanneur-nobert.ca';
