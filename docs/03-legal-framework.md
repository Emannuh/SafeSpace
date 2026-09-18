# Legal Framework

## Purpose

This document records the verified legal, policy, and institutional sources that form the SafeSpace knowledge base.

SafeSpace does not generate legal information from general AI model knowledge. Every rights record must be traceable to an entry in this document.

---

## Source-to-Journey Mapping

### A. Teenage Pregnancy

| Journey | Topic | Primary Source | Source Type | Institution | Verified In SafeSpace |
|---|---|---|---|---|---|
| Teenage Pregnancy | Staying in School While Pregnant | National School Re-entry Guidelines, 2020 | Government Guidance / Policy | Ministry of Education, Kenya | ✅ TP-SCHOOL-001 |
| Teenage Pregnancy | School Re-entry After Delivery | National School Re-entry Guidelines, 2020 | Government Guidance / Policy | Ministry of Education, Kenya | ✅ TP-REENTRY-001 |
| Teenage Pregnancy | National Examinations | National School Re-entry Guidelines, 2020 | Government Guidance / Policy | Ministry of Education, Kenya | ✅ TP-EXAMS-001 |
| Teenage Pregnancy | Getting Appropriate Support | Children Act, 2022 | Legislation | Kenya Law | ✅ TP-SUPPORT-001 |

**Important distinction — Policy vs Legislation:**
The National School Re-entry Guidelines are Ministry of Education policy/guidance, not primary legislation. Claims arising from these guidelines should be described as policy obligations or guidelines, not as statutory legal rights enforceable in the same way as a constitutional provision or Act of Parliament. SafeSpace preserves this distinction in every record's `limitations` field and `source_type` (GOVERNMENT_GUIDANCE).

### B. Sexual Exploitation and Abuse

| Journey | Topic | Primary Source | Source Type | Institution | Verified In SafeSpace |
|---|---|---|---|---|---|
| Sexual Exploitation | Understanding Sexual Exploitation | Sexual Offences Act, Cap. 63A, s.8 | Legislation | Kenya Law | ✅ SEA-UNDERSTAND-001 |
| Sexual Exploitation | Sexual Abuse Involving a Child | Children Act, 2022, s.16 | Legislation | Kenya Law | ✅ SEA-ABUSE-001 |
| Sexual Exploitation | Safe Reporting Options | Children Act, 2022, s.16 | Legislation | Kenya Law | ✅ SEA-REPORT-001 |
| Sexual Exploitation | Getting Protection and Support | Constitution of Kenya, Art. 53; Children Act 2022, s.16 | Constitution + Legislation | Kenya Law | ✅ SEA-PROTECT-001 |

### C. Child Justice

| Journey | Topic | Primary Source | Source Type | Institution | Verified In SafeSpace |
|---|---|---|---|---|---|
| Child Justice | Arrest Rights | Constitution of Kenya, Art. 49 | Constitution | Kenya Law | ✅ CJ-001 |
| Child Justice | Legal Representation | Constitution of Kenya, Art. 50(2)(g) and Art. 50(2)(h) | Constitution | Kenya Law | ✅ CJ-LEGAL-001 |
| Child Justice | Parent or Guardian Involvement | Children Act, 2022, s.222 | Legislation | Kenya Law | ✅ CJ-PARENT-001 |
| Child Justice | Detention Protections | Constitution of Kenya, Art. 53(1)(f) | Constitution | Kenya Law | ✅ CJ-DETAIN-001 |
| Child Justice | Diversion | Children Act, 2022, s.227 | Legislation | Kenya Law | ✅ CJ-DIVERT-001 |

---

## Authoritative Sources Used

### 1. Constitution of Kenya, 2010
- **Publisher:** Kenya Law / Republic of Kenya
- **Source type:** CONSTITUTION
- **URL:** https://www.kenyalaw.org/lex/actview.xql?actid=Const2010
- **Relevant articles used:** Art. 49 (arrest rights), Art. 50 (fair trial / legal representation — Art. 50(2)(g) right to choose lawyer; Art. 50(2)(h) state-funded representation), Art. 51 (rights of detained persons — general), Art. 53 (rights of the child — Art. 53(1)(d) protection from abuse; Art. 53(1)(f) child detention as last resort, separate from adults)

### 2. Children Act, 2022
- **Publisher:** Kenya Law / Republic of Kenya
- **Source type:** LEGISLATION
- **URL:** https://www.kenyalaw.org/lex/actview.xql?actid=No.29of2022
- **Relevant sections used:** s.13 (child's right to care and protection), s.16 (protection from abuse and exploitation), s.222 (parental notification on arrest), s.227 (diversion eligibility and procedure), s.228 (preliminary inquiry)
- **Note:** s.226 concerns diversion objectives and is not used as authority for the separate-from-adults detention proposition (that is Art. 53(1)(f) of the Constitution).

### 3. Sexual Offences Act, Cap. 63A
- **Publisher:** Kenya Law / Republic of Kenya
- **Source type:** LEGISLATION
- **URL:** https://www.kenyalaw.org/lex/actview.xql?actid=Cap.63A
- **Relevant sections used:** s.8 (defilement — sexual penetration involving a child under 18; a child cannot consent to such an act)
- **Sections reviewed but NOT seeded:** ss.9, 11, 12, 14, 15, 16, 16A, 20 — these cover other sexual offences against children but require careful framing to avoid overstatement and are flagged for human legal review before inclusion. SEA-UNDERSTAND-001 is deliberately narrowed to what s.8 explicitly provides.

### 4. National School Re-entry Guidelines, 2020
- **Publisher:** Ministry of Education, Kenya
- **Source type:** GOVERNMENT_GUIDANCE
- **URL:** https://www.education.go.ke
- **Relevant provisions:** Continuation in school during pregnancy; school re-entry after delivery; examination access where health permits; school responsibilities
- **Note:** These are policy guidelines, not primary legislation. SafeSpace records based on this source explicitly state this limitation.

---

## Sources Reviewed But Not Yet Seeded

| Source | Reason |
|---|---|
| National Reproductive Health Policy 2022–2032 | Claims overlap with already-supported records. Specific propositions require human review before a VERIFIED record can be created. |
| Sexual Offences Act ss.9, 11, 12, 14–16, 16A, 20 | Individual provisions require careful legal framing to avoid overstatement. Flagged for human legal review. |
| Children Act Part XV (additional child justice provisions) | Specific procedural claims beyond ss.222, 226–228 require human verification. |

---

## Trusted Support Services

### Child Helpline 116
- **Institution:** State Department for Children Services
- **Phone:** 116 (toll-free, 24/7)
- **Purpose:** Child protection, counselling, referrals, escalation

### GBV Helpline 1195
- **Institution:** Government of Kenya GBV response service
- **Phone:** 1195 (toll-free, 24/7)
- **Purpose:** Support and referral for gender-based violence cases

### National Legal Aid Service
- **Institution:** National Legal Aid Service (established under Legal Aid Act)
- **Purpose:** Legal aid and support for eligible persons who cannot afford private legal representation

### Independent Policing Oversight Authority (IPOA)
- **Institution:** IPOA
- **Purpose:** Complaints about police misconduct. Not a substitute for legal representation.

---

## Legal Content Rule

Every SafeSpace rights record must include:
- title
- jurisdiction
- source (linked LegalSource record)
- legal/section reference
- plain-language summary
- appropriate next step
- support pathway where relevant
- last verification date
- verification status

SafeSpace must not present EXPIRED or ARCHIVED information as current guidance. REVIEW_REQUIRED records must never appear in the verified public API.

---

## Verification Status Values

| Status | Meaning |
|---|---|
| VERIFIED | Content has been reviewed against the source and is approved for public use |
| REVIEW_REQUIRED | Content needs re-verification before use |
| EXPIRED | Source has been superseded or repealed |
| ARCHIVED | No longer actively maintained; not for public display |
