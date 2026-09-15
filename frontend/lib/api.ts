/**
 * SafeSpace API client.
 *
 * All calls go to the Django backend via NEXT_PUBLIC_API_BASE_URL.
 * No legal or support content is hard-coded here — everything comes from
 * the verified backend database.
 *
 * Handles: 200 OK, 404 (returns null), network failure (throws ApiError).
 */

import type {
  ActionPath,
  Journey,
  RightsRecord,
  SafetyCheckResult,
  SupportService,
  Topic,
} from "./types";

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function baseUrl(): string {
  const url = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!url) throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  return url.replace(/\/$/, "");
}

async function get<T>(path: string): Promise<T | null> {
  const res = await fetch(`${baseUrl()}${path}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new ApiError(res.status, `API error ${res.status}: ${path}`);
  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Journeys
// ---------------------------------------------------------------------------

export async function fetchJourneys(): Promise<Journey[]> {
  const data = await get<Journey[]>("/journeys/");
  return data ?? [];
}

export async function fetchTopics(journeySlug: string): Promise<Topic[] | null> {
  return get<Topic[]>(`/journeys/${journeySlug}/topics/`);
}

// ---------------------------------------------------------------------------
// Rights
// ---------------------------------------------------------------------------

export async function fetchRights(
  journeySlug: string,
  topicSlug: string
): Promise<RightsRecord[] | null> {
  return get<RightsRecord[]>(
    `/journeys/${journeySlug}/topics/${topicSlug}/rights/`
  );
}

export async function fetchRightsDetail(
  recordCode: string
): Promise<RightsRecord | null> {
  return get<RightsRecord>(`/rights/${recordCode}/`);
}

// ---------------------------------------------------------------------------
// Actions
// ---------------------------------------------------------------------------

export async function fetchActions(
  journeySlug: string,
  topicSlug: string
): Promise<ActionPath[] | null> {
  return get<ActionPath[]>(
    `/journeys/${journeySlug}/topics/${topicSlug}/actions/`
  );
}

// ---------------------------------------------------------------------------
// Support services
// ---------------------------------------------------------------------------

export async function fetchSupportServices(): Promise<SupportService[]> {
  const data = await get<SupportService[]>("/support-services/");
  return data ?? [];
}

// ---------------------------------------------------------------------------
// Safety check
// Message is sent to backend and result returned.
// Message is NOT stored anywhere by this function.
// ---------------------------------------------------------------------------

export async function postSafetyCheck(
  message: string
): Promise<SafetyCheckResult> {
  const res = await fetch(`${baseUrl()}/safety/check/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new ApiError(res.status, "Safety check failed");
  return res.json() as Promise<SafetyCheckResult>;
}
