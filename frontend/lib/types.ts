// SafeSpace API type definitions — mirrors Django serializer output

export interface Journey {
  id: number;
  name: string;
  slug: string;
  description: string;
  risk_default: "LOW" | "MEDIUM" | "HIGH" | "IMMEDIATE";
}

export interface Topic {
  id: number;
  title: string;
  slug: string;
  journey_slug: string;
  description: string;
  default_risk_level: "LOW" | "MEDIUM" | "HIGH" | "IMMEDIATE";
  sort_order: number;
}

export interface LegalSource {
  id: number;
  title: string;
  source_type: string;
  source_type_display: string;
  publisher: string;
  jurisdiction: string;
  url: string;
  publication_date: string | null;
  last_verified: string;
  status: string;
  status_display: string;
}

export interface RightsRecord {
  id: number;
  record_code: string;
  journey_slug: string;
  topic_slug: string;
  jurisdiction: string;
  title: string;
  plain_language_summary: string;
  legal_reference: string;
  section_reference: string;
  source: LegalSource;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "IMMEDIATE";
  risk_level_display: string;
  next_step_text: string;
  limitations: string;
  last_verified: string;
  status: string;
  status_display: string;
}

export interface SupportService {
  id: number;
  name: string;
  slug: string;
  service_type: string;
  service_type_display: string;
  description: string;
  jurisdiction: string;
  phone: string;
  whatsapp: string;
  website: string;
  available_24_7: boolean;
  last_verified: string;
  status: string;
  status_display: string;
}

export interface ActionPath {
  id: number;
  topic_slug: string;
  title: string;
  step_number: number;
  instruction: string;
  action_type: string;
  action_type_display: string;
  support_service: SupportService | null;
  source: LegalSource | null;
  last_verified: string;
  status: string;
  status_display: string;
}

export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "IMMEDIATE";
export type RiskAction =
  | "NORMAL_FLOW"
  | "SHOW_SUPPORT"
  | "SHOW_HIGH_RISK_SUPPORT"
  | "SHOW_IMMEDIATE_SAFETY";

export interface SafetyCheckResult {
  risk_level: RiskLevel;
  action: RiskAction;
  matched_rule: string | null;
}

// ---------------------------------------------------------------------------
// Ask endpoint (Day 5)
// ---------------------------------------------------------------------------

export type EvidenceStatus = "SUPPORTED" | "PARTIAL" | "INSUFFICIENT";

export interface AskResponse {
  answer: string;
  evidence_status: EvidenceStatus;
  risk_level: RiskLevel;
  risk_action: RiskAction;
  ai_used: boolean;
  ai_disclosure: string;
  journey: Journey | null;
  topic: Topic | null;
  rights: RightsRecord[];
  sources: LegalSource[];
  actions: ActionPath[];
  support_services: SupportService[];
  error?: string | null;
}
