/**
 * SafeSpace frontend tests.
 *
 * Tests focus on behaviour — what the user experiences —
 * rather than implementation details.
 *
 * API calls are mocked so tests run without a live Django server.
 */

import React from "react";
import { render, screen, fireEvent, waitFor, act } from "@testing-library/react";
import "@testing-library/jest-dom";

// ---------------------------------------------------------------------------
// Mock next/navigation (used by some components)
// ---------------------------------------------------------------------------
jest.mock("next/navigation", () => ({
  notFound: jest.fn(),
  useRouter: () => ({ push: jest.fn(), replace: jest.fn() }),
  usePathname: () => "/",
}));

// ---------------------------------------------------------------------------
// Mock the API module
// ---------------------------------------------------------------------------
jest.mock("@/lib/api", () => ({
  fetchJourneys:       jest.fn(),
  fetchTopics:         jest.fn(),
  fetchRights:         jest.fn(),
  fetchActions:        jest.fn(),
  fetchSupportServices: jest.fn(),
  postSafetyCheck:     jest.fn(),
  ApiError:            class ApiError extends Error {},
}));

import * as api from "@/lib/api";
import QuickExit from "@/app/components/QuickExit";
import RiskBadge from "@/app/components/RiskBadge";
import VerifiedBadge from "@/app/components/VerifiedBadge";
import { LoadingState, EmptyState, ErrorState } from "@/app/components/StateViews";
import SafetyCheckForm from "@/app/safety/SafetyCheckForm";

// Shared fixtures
const mockJourney = {
  id: 1, name: "Child Justice", slug: "child-justice",
  description: "Rights for young people in justice processes.", risk_default: "HIGH" as const,
};

const mockTopic = {
  id: 1, title: "Arrest Rights", slug: "arrest-rights",
  journey_slug: "child-justice", description: "Rights at arrest.",
  default_risk_level: "HIGH" as const, sort_order: 1,
};

const mockSource = {
  id: 1, title: "Constitution of Kenya", source_type: "CONSTITUTION",
  source_type_display: "Constitution", publisher: "Kenya Law",
  jurisdiction: "Kenya", url: "https://kenyalaw.org/const",
  publication_date: "2010-08-27", last_verified: "2026-09-14",
  status: "VERIFIED", status_display: "Verified",
};

const mockRecord = {
  id: 1, record_code: "CJ-001", journey_slug: "child-justice",
  topic_slug: "arrest-rights", jurisdiction: "Kenya",
  title: "Right to be informed of reason for arrest",
  plain_language_summary: "You have the right to know why you are being arrested.",
  legal_reference: "Constitution of Kenya 2010, Article 49",
  section_reference: "Art. 49(1)(a)", source: mockSource,
  risk_level: "HIGH" as const, risk_level_display: "High",
  next_step_text: "Ask the officer clearly.", limitations: "This is not legal advice.",
  last_verified: "2026-09-14", status: "VERIFIED", status_display: "Verified",
};

const mockService = {
  id: 1, name: "Child Helpline 116", slug: "child-helpline-116",
  service_type: "CHILD_PROTECTION", service_type_display: "Child Protection",
  description: "Child protection support and referrals.",
  jurisdiction: "Kenya", phone: "116", whatsapp: "", website: "",
  available_24_7: true, last_verified: "2026-09-14",
  status: "VERIFIED", status_display: "Verified",
};

const mockAction = {
  id: 1, topic_slug: "arrest-rights", title: "Stay calm",
  step_number: 1, instruction: "Ask why you are being arrested.",
  action_type: "RIGHTS_GUIDANCE", action_type_display: "Rights Guidance",
  support_service: mockService, source: null,
  last_verified: "2026-09-14", status: "VERIFIED", status_display: "Verified",
};

// ===========================================================================
// 1. Quick Exit exists and navigates away
// ===========================================================================
describe("QuickExit", () => {
  it("renders a Quick Exit button", () => {
    render(<QuickExit />);
    expect(screen.getByRole("button", { name: /quick exit/i })).toBeInTheDocument();
  });

  it("calls window.location.replace on click", () => {
    const replaceMock = jest.fn();
    Object.defineProperty(window, "location", {
      writable: true,
      value: { replace: replaceMock },
    });
    render(<QuickExit />);
    fireEvent.click(screen.getByRole("button", { name: /quick exit/i }));
    expect(replaceMock).toHaveBeenCalledWith("https://www.google.com");
  });
});

// ===========================================================================
// 2. RiskBadge renders correct label per level
// ===========================================================================
describe("RiskBadge", () => {
  it.each([
    ["LOW",       "General information"],
    ["MEDIUM",    "Some risk"],
    ["HIGH",      "High risk"],
    ["IMMEDIATE", "Immediate safety"],
  ] as const)("renders correct label for %s", (level, expectedText) => {
    render(<RiskBadge level={level} />);
    expect(screen.getByText(new RegExp(expectedText, "i"))).toBeInTheDocument();
  });
});

// ===========================================================================
// 3. VerifiedBadge renders
// ===========================================================================
describe("VerifiedBadge", () => {
  it("renders verified badge", () => {
    render(<VerifiedBadge />);
    expect(screen.getByText(/verified source/i)).toBeInTheDocument();
  });
});

// ===========================================================================
// 4. State views render
// ===========================================================================
describe("State views", () => {
  it("LoadingState renders loading message", () => {
    render(<LoadingState />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("EmptyState renders custom message", () => {
    render(<EmptyState message="Nothing here yet." />);
    expect(screen.getByText("Nothing here yet.")).toBeInTheDocument();
  });

  it("ErrorState renders error message", () => {
    render(<ErrorState message="Could not load." />);
    expect(screen.getByRole("alert")).toBeInTheDocument();
    expect(screen.getByText(/could not load/i)).toBeInTheDocument();
  });
});

// ===========================================================================
// 5. Safety check form behaviour
// ===========================================================================
describe("SafetyCheckForm", () => {
  const mockPostSafetyCheck = api.postSafetyCheck as jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders the message textarea and submit button", () => {
    render(<SafetyCheckForm />);
    expect(screen.getByLabelText(/describe your situation/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /check/i })).toBeInTheDocument();
  });

  it("submit button is disabled when message is empty", () => {
    render(<SafetyCheckForm />);
    expect(screen.getByRole("button", { name: /check/i })).toBeDisabled();
  });

  it("submit button is enabled when message has content", () => {
    render(<SafetyCheckForm />);
    fireEvent.change(screen.getByLabelText(/describe your situation/i), {
      target: { value: "I need help." },
    });
    expect(screen.getByRole("button", { name: /check/i })).not.toBeDisabled();
  });

  it("shows LOW result and clears message on submit", async () => {
    mockPostSafetyCheck.mockResolvedValueOnce({
      risk_level: "LOW", action: "NORMAL_FLOW", matched_rule: null,
    });
    render(<SafetyCheckForm />);
    const textarea = screen.getByLabelText(/describe your situation/i);
    fireEvent.change(textarea, { target: { value: "What are my rights?" } });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /check/i }));
    });
    await waitFor(() => {
      expect(screen.getByText(/here to help/i)).toBeInTheDocument();
    });
    // Message should be cleared from the input
    expect(textarea).not.toBeInTheDocument(); // form hidden after result
  });

  it("shows HIGH risk result with support link", async () => {
    mockPostSafetyCheck.mockResolvedValueOnce({
      risk_level: "HIGH", action: "SHOW_HIGH_RISK_SUPPORT", matched_rule: "abuse-rule",
    });
    render(<SafetyCheckForm />);
    fireEvent.change(screen.getByLabelText(/describe your situation/i), {
      target: { value: "Someone is hurting me." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /check/i }));
    });
    await waitFor(() => {
      expect(screen.getByText(/you may need support right now/i)).toBeInTheDocument();
    });
    expect(screen.getByRole("link", { name: /view support services/i })).toBeInTheDocument();
  });

  it("shows IMMEDIATE result with safety message", async () => {
    mockPostSafetyCheck.mockResolvedValueOnce({
      risk_level: "IMMEDIATE", action: "SHOW_IMMEDIATE_SAFETY", matched_rule: "immediate-danger",
    });
    render(<SafetyCheckForm />);
    fireEvent.change(screen.getByLabelText(/describe your situation/i), {
      target: { value: "I am not safe." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /check/i }));
    });
    await waitFor(() => {
      expect(screen.getByText(/your safety comes first/i)).toBeInTheDocument();
    });
  });

  it("shows error state when API fails", async () => {
    mockPostSafetyCheck.mockRejectedValueOnce(new Error("Network error"));
    render(<SafetyCheckForm />);
    fireEvent.change(screen.getByLabelText(/describe your situation/i), {
      target: { value: "Help me." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /check/i }));
    });
    await waitFor(() => {
      expect(screen.getByRole("alert")).toBeInTheDocument();
    });
  });

  it("does not write message to localStorage or sessionStorage", async () => {
    const localStorageSpy = jest.spyOn(Storage.prototype, "setItem");
    mockPostSafetyCheck.mockResolvedValueOnce({
      risk_level: "LOW", action: "NORMAL_FLOW", matched_rule: null,
    });
    render(<SafetyCheckForm />);
    fireEvent.change(screen.getByLabelText(/describe your situation/i), {
      target: { value: "A sensitive message." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /check/i }));
    });
    await waitFor(() => screen.getByText(/here to help/i));
    expect(localStorageSpy).not.toHaveBeenCalled();
    localStorageSpy.mockRestore();
  });

  it("start over resets form to idle state", async () => {
    mockPostSafetyCheck.mockResolvedValueOnce({
      risk_level: "LOW", action: "NORMAL_FLOW", matched_rule: null,
    });
    render(<SafetyCheckForm />);
    fireEvent.change(screen.getByLabelText(/describe your situation/i), {
      target: { value: "Question." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /check/i }));
    });
    await waitFor(() => screen.getByText(/here to help/i));
    fireEvent.click(screen.getByRole("button", { name: /start over/i }));
    expect(screen.getByLabelText(/describe your situation/i)).toBeInTheDocument();
  });
});
