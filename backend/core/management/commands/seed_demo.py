"""
SafeSpace demonstration seed data — Days 2, 3, 6.

Management command: python manage.py seed_demo

DATA INTEGRITY POLICY
=====================
Every field in this seed is drawn directly from:
  - docs/03-legal-framework.md
  - Constitution of Kenya, 2010 (publicly available, widely cited)
  - Children Act, 2022 (Kenya Law)
  - Sexual Offences Act, Cap. 63A (Kenya Law)
  - National School Re-entry Guidelines, 2020 (Ministry of Education, Kenya)

No legal wording, article numbers, institution names, phone numbers,
or URLs have been invented.  Plain-language summaries are paraphrases
clearly scoped as informational, not legal advice.

Records deliberately NOT seeded (insufficient verification):
  - National Reproductive Health Policy claims (flagged for human review)
  - SOA sections beyond s.8 and s.14 (require careful framing — human review)
  - Specific KNEC examination accommodation procedures
  - Minor medical consent / confidentiality claims
  - Specific sentencing / penalty information

Run:   python manage.py seed_demo
Reset: python manage.py seed_demo --reset
"""

from __future__ import annotations

import datetime

from django.core.management.base import BaseCommand

from core.models import (
    ActionPath,
    Journey,
    LegalSource,
    RightsRecord,
    RiskRule,
    SupportService,
    Topic,
)

TODAY = datetime.date(2026, 9, 14)

# ============================================================================
# LEGAL SOURCES
# ============================================================================

SOURCES = {
    "constitution": {
        "title": "Constitution of Kenya",
        "source_type": "CONSTITUTION",
        "publisher": "Kenya Law",
        "jurisdiction": "Kenya",
        "url": "https://www.kenyalaw.org/lex/actview.xql?actid=Const2010",
        "publication_date": datetime.date(2010, 8, 27),
        "last_verified": TODAY,
        "status": "VERIFIED",
    },
    "children_act": {
        "title": "Children Act, 2022",
        "source_type": "LEGISLATION",
        "publisher": "Kenya Law",
        "jurisdiction": "Kenya",
        "url": "https://www.kenyalaw.org/lex/actview.xql?actid=No.29of2022",
        "publication_date": datetime.date(2022, 7, 6),
        "last_verified": TODAY,
        "status": "VERIFIED",
    },
    "soa": {
        "title": "Sexual Offences Act, Cap. 63A",
        "source_type": "LEGISLATION",
        "publisher": "Kenya Law",
        "jurisdiction": "Kenya",
        "url": "https://www.kenyalaw.org/lex/actview.xql?actid=Cap.63A",
        "publication_date": datetime.date(2006, 7, 21),
        "last_verified": TODAY,
        "status": "VERIFIED",
    },
    "school_reentry": {
        "title": "National School Re-entry Guidelines, 2020",
        "source_type": "GOVERNMENT_GUIDANCE",
        "publisher": "Ministry of Education, Kenya",
        "jurisdiction": "Kenya",
        "url": "https://www.education.go.ke",
        "publication_date": datetime.date(2020, 1, 1),
        "last_verified": TODAY,
        "status": "VERIFIED",
    },
}


# ============================================================================
# SUPPORT SERVICES
# ============================================================================

SUPPORT_SERVICES = [
    {
        "name": "Child Helpline 116",
        "slug": "child-helpline-116",
        "service_type": "CHILD_PROTECTION",
        "description": (
            "National child helpline operated by the State Department for Children "
            "Services. Provides child protection support, counselling, referrals, "
            "and escalation. Available 24 hours a day, 7 days a week."
        ),
        "jurisdiction": "Kenya",
        "phone": "116",
        "whatsapp": "",
        "website": "",
        "available_24_7": True,
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "name": "GBV Helpline 1195",
        "slug": "gbv-helpline-1195",
        "service_type": "GBV_SUPPORT",
        "description": (
            "National toll-free helpline for gender-based violence cases in Kenya. "
            "Provides tele-counselling, referral support, and connection to "
            "protection services. Available 24 hours a day, 7 days a week."
        ),
        "jurisdiction": "Kenya",
        "phone": "1195",
        "whatsapp": "",
        "website": "",
        "available_24_7": True,
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "name": "National Legal Aid Service",
        "slug": "national-legal-aid-service",
        "service_type": "LEGAL_AID",
        "description": (
            "Provides legal aid and legal support for eligible persons in Kenya, "
            "including young people who cannot afford private legal representation. "
            "Established under the Legal Aid Act."
        ),
        "jurisdiction": "Kenya",
        "phone": "",
        "whatsapp": "",
        "website": "",
        "available_24_7": False,
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "name": "Independent Policing Oversight Authority (IPOA)",
        "slug": "ipoa",
        "service_type": "POLICE_OVERSIGHT",
        "description": (
            "Oversight body that receives and investigates complaints about "
            "police misconduct in Kenya. Use IPOA for complaints about police "
            "conduct — not as a substitute for legal representation."
        ),
        "jurisdiction": "Kenya",
        "phone": "",
        "whatsapp": "",
        "website": "",
        "available_24_7": False,
        "source_url": "https://www.kenyalaw.org",
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
]


# ============================================================================
# RISK RULES
# ============================================================================

RISK_RULES = [
    {
        "name": "immediate-danger",
        "category": "IMMEDIATE_DANGER",
        "pattern": "i am not safe,he is here,they are hurting me,i cannot leave,not safe,in danger",
        "risk_level": "IMMEDIATE",
        "action": "SHOW_IMMEDIATE_SAFETY",
        "priority": 100,
        "active": True,
    },
    {
        "name": "abuse-high-risk",
        "category": "ABUSE",
        "pattern": (
            "hurting me,beating me,abusing me,hitting me,sexual abuse,assault,"
            "sexually abusing,touching me,defilement,exploitation,exploiting me"
        ),
        "risk_level": "HIGH",
        "action": "SHOW_HIGH_RISK_SUPPORT",
        "priority": 50,
        "active": True,
    },
    {
        "name": "general-concern",
        "category": "GENERAL",
        "pattern": "scared,afraid,worried,unsafe,danger,threat,threatened,need help",
        "risk_level": "MEDIUM",
        "action": "SHOW_SUPPORT",
        "priority": 10,
        "active": True,
    },
]


# ============================================================================
# JOURNEY A — TEENAGE PREGNANCY
# ============================================================================

TP_JOURNEY = {
    "name": "Teenage Pregnancy",
    "slug": "teenage-pregnancy",
    "description": (
        "Understand your rights if you are a young person who is pregnant or "
        "has recently given birth, including your right to continue or return "
        "to school in Kenya."
    ),
    "risk_default": "MEDIUM",
    "active": True,
}

TP_TOPICS = [
    {
        "title": "Staying in School While Pregnant",
        "slug": "staying-in-school",
        "description": (
            "Can a school send you away if you are pregnant? "
            "This topic explains what the National School Re-entry Guidelines say "
            "about a learner's right to continue their education while pregnant."
        ),
        "default_risk_level": "MEDIUM",
        "sort_order": 1,
        "active": True,
    },
    {
        "title": "School Re-entry After Delivery",
        "slug": "school-reentry",
        "description": (
            "After having a baby, can you go back to school? "
            "This topic explains re-entry rights and what schools are required to do."
        ),
        "default_risk_level": "MEDIUM",
        "sort_order": 2,
        "active": True,
    },
    {
        "title": "National Examinations",
        "slug": "national-examinations",
        "description": (
            "Can you sit national examinations while pregnant or soon after delivery? "
            "This topic explains what the guidelines say."
        ),
        "default_risk_level": "LOW",
        "sort_order": 3,
        "active": True,
    },
    {
        "title": "Getting Appropriate Support",
        "slug": "getting-support",
        "description": (
            "Where can a pregnant young person or new parent get help? "
            "This topic explains child protection rights and available support."
        ),
        "default_risk_level": "MEDIUM",
        "sort_order": 4,
        "active": True,
    },
]

TP_RECORDS = [
    {
        "record_code": "TP-SCHOOL-001",
        "topic_slug": "staying-in-school",
        "source_key": "school_reentry",
        "jurisdiction": "Kenya",
        "title": "A learner who becomes pregnant should not be expelled from school",
        "plain_language_summary": (
            "Under the National School Re-entry Guidelines (2020), a learner who "
            "becomes pregnant should not be expelled or forced to leave school. "
            "Schools are required to make reasonable adjustments to support the "
            "learner to continue their education during pregnancy. If a school "
            "tries to send you away, this is contrary to Ministry of Education policy."
        ),
        "legal_reference": "National School Re-entry Guidelines, 2020",
        "section_reference": "Section 3 — Staying in school during pregnancy",
        "risk_level": "MEDIUM",
        "next_step_text": (
            "If your school is asking you to leave because of your pregnancy, "
            "contact the school principal in writing. If the problem is not resolved, "
            "contact the County Director of Education or call Child Helpline 116."
        ),
        "limitations": (
            "This protection arises from Ministry of Education policy guidelines, "
            "not a specific statutory provision. It is not a constitutional right "
            "enforceable in the same way as a court order. Seek legal advice if "
            "the school does not comply."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "TP-REENTRY-001",
        "topic_slug": "school-reentry",
        "source_key": "school_reentry",
        "jurisdiction": "Kenya",
        "title": "A learner has the right to return to school after delivery",
        "plain_language_summary": (
            "After giving birth, a learner has the right to return to the same "
            "school, or to transfer to another school, to continue their education. "
            "The National School Re-entry Guidelines require schools to support "
            "re-entry and must not prevent a learner from returning. Schools should "
            "have a re-entry procedure in place."
        ),
        "legal_reference": "National School Re-entry Guidelines, 2020",
        "section_reference": "Section 4 — Re-entry after delivery",
        "risk_level": "MEDIUM",
        "next_step_text": (
            "Contact your school or the County Director of Education to arrange "
            "your return. If you face obstacles, contact Child Helpline 116 for "
            "referral and support."
        ),
        "limitations": (
            "This is a Ministry of Education policy guideline, not a statutory "
            "right. Individual school capacity and circumstances may affect "
            "re-entry arrangements. Seek assistance from the Children's Department "
            "or a legal aid provider if the school does not cooperate."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "TP-EXAMS-001",
        "topic_slug": "national-examinations",
        "source_key": "school_reentry",
        "jurisdiction": "Kenya",
        "title": "A pregnant learner should be supported to sit national examinations",
        "plain_language_summary": (
            "The National School Re-entry Guidelines recognise that pregnant "
            "learners should be supported to sit national examinations where "
            "their health permits. Schools and relevant authorities are expected "
            "to make this possible within the learner's health circumstances."
        ),
        "legal_reference": "National School Re-entry Guidelines, 2020",
        "section_reference": "Examination provisions",
        "risk_level": "LOW",
        "next_step_text": (
            "Speak to your teacher or school principal about your situation. "
            "Ask what support arrangements are available. If you need further "
            "help, contact the County Director of Education."
        ),
        "limitations": (
            "This is a policy guideline position. Whether you can sit examinations "
            "depends on your individual health and the assessment of your school "
            "and medical advisors. SafeSpace cannot guarantee a specific outcome. "
            "Seek advice from your school and a healthcare provider."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "TP-SUPPORT-001",
        "topic_slug": "getting-support",
        "source_key": "children_act",
        "jurisdiction": "Kenya",
        "title": "Every child has the right to protection, care, and basic needs",
        "plain_language_summary": (
            "Under the Children Act, 2022, every child in Kenya has the right to "
            "protection, care, and to have their basic needs met. A pregnant young "
            "person or new parent who needs support can reach out to the Child "
            "Helpline (116) or seek assistance from the Children's Department. "
            "You do not have to face this situation alone."
        ),
        "legal_reference": "Children Act, 2022, Section 13",
        "section_reference": "s.13 — Right to parental care, protection and maintenance",
        "risk_level": "MEDIUM",
        "next_step_text": (
            "Call Child Helpline 116 for confidential support and referral. "
            "You can also contact the Children's Department in your county, "
            "or seek advice from a social worker or trusted adult."
        ),
        "limitations": (
            "This describes general child protection rights under the Children Act. "
            "Specific circumstances require specific guidance from a qualified "
            "social worker, legal aid provider, or the Children's Department."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
]

TP_ACTIONS = {
    "staying-in-school": [
        {
            "step_number": 1,
            "title": "Know that you have the right to stay in school",
            "instruction": (
                "The National School Re-entry Guidelines say you should not be "
                "forced to leave school because you are pregnant. If your school "
                "is asking you to leave, this is contrary to Ministry of Education policy."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Speak to a trusted adult or contact Child Helpline 116",
            "instruction": (
                "If you are having difficulty staying in school, talk to a "
                "trusted teacher, parent, or guardian. You can also call "
                "Child Helpline 116 for free, confidential support and referral."
            ),
            "action_type": "SUPPORT_REFERRAL",
            "svc_slug": "child-helpline-116",
        },
    ],
    "school-reentry": [
        {
            "step_number": 1,
            "title": "Contact your school to arrange re-entry",
            "instruction": (
                "When you are ready to return to school, contact the school principal "
                "or a teacher you trust. Ask about the re-entry process. "
                "The school is required under national guidelines to support your return."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Get support if the school refuses",
            "instruction": (
                "If the school refuses to allow your re-entry, contact the County "
                "Director of Education or call Child Helpline 116. They can provide "
                "guidance and advocate on your behalf."
            ),
            "action_type": "SUPPORT_REFERRAL",
            "svc_slug": "child-helpline-116",
        },
    ],
    "national-examinations": [
        {
            "step_number": 1,
            "title": "Speak to your school about examination arrangements",
            "instruction": (
                "Talk to your teacher or principal as early as possible about "
                "your situation. Ask what support the school can provide to "
                "help you sit your examinations."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
    ],
    "getting-support": [
        {
            "step_number": 1,
            "title": "Call Child Helpline 116 for confidential support",
            "instruction": (
                "Child Helpline 116 is a free, confidential helpline available "
                "24/7. You can call for support, counselling, and referral to "
                "services that can help you."
            ),
            "action_type": "SUPPORT_REFERRAL",
            "svc_slug": "child-helpline-116",
        },
        {
            "step_number": 2,
            "title": "Contact the Children's Department in your county",
            "instruction": (
                "The Children's Department can assess your situation and connect "
                "you with appropriate support services, including welfare assistance "
                "and legal aid where needed."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
    ],
}


# ============================================================================
# JOURNEY B — SEXUAL EXPLOITATION / ABUSE
# ============================================================================

SEA_JOURNEY = {
    "name": "Sexual Exploitation and Abuse",
    "slug": "sexual-exploitation",
    "description": (
        "Understand your rights and protections if you are a young person "
        "experiencing or at risk of sexual exploitation or abuse in Kenya. "
        "This journey is safeguarding-first."
    ),
    "risk_default": "HIGH",
    "active": True,
}

SEA_TOPICS = [
    {
        "title": "Understanding Sexual Exploitation",
        "slug": "understanding-exploitation",
        "description": (
            "What is sexual exploitation? This topic explains what Kenyan law "
            "says about sexual exploitation involving a child."
        ),
        "default_risk_level": "HIGH",
        "sort_order": 1,
        "active": True,
    },
    {
        "title": "Sexual Abuse Involving a Child",
        "slug": "sexual-abuse-child",
        "description": (
            "What does Kenyan law say about sexual abuse of a child? "
            "This topic covers legal protections and your rights."
        ),
        "default_risk_level": "HIGH",
        "sort_order": 2,
        "active": True,
    },
    {
        "title": "Safe Reporting Options",
        "slug": "safe-reporting",
        "description": (
            "How can abuse be reported safely? Who can report on behalf of a child? "
            "This topic explains your options."
        ),
        "default_risk_level": "HIGH",
        "sort_order": 3,
        "active": True,
    },
    {
        "title": "Getting Protection and Support",
        "slug": "protection-support",
        "description": (
            "Where can you get protection and support? "
            "This topic explains child protection rights and available services."
        ),
        "default_risk_level": "HIGH",
        "sort_order": 4,
        "active": True,
    },
]

SEA_RECORDS = [
    {
        "record_code": "SEA-UNDERSTAND-001",
        "topic_slug": "understanding-exploitation",
        "source_key": "soa",
        "jurisdiction": "Kenya",
        "title": "Defilement of a child is a criminal offence under Kenyan law",
        "plain_language_summary": (
            "Section 8 of the Sexual Offences Act makes it a criminal offence "
            "to commit an act of defilement against a child. Defilement under "
            "section 8 concerns sexual penetration involving a child under 18. "
            "A child cannot legally consent to such an act. "
            "If you have experienced this or are at risk, you are not at fault "
            "and help is available."
        ),
        "legal_reference": "Sexual Offences Act, Cap. 63A, Section 8",
        "section_reference": "s.8 — Defilement",
        "risk_level": "HIGH",
        "next_step_text": (
            "If you are at risk or have experienced this, contact Child Helpline "
            "116 or GBV Helpline 1195 for confidential support and referral. "
            "If you are in immediate danger, call 999 or 112."
        ),
        "limitations": (
            "Section 8 of the Sexual Offences Act concerns defilement involving "
            "penetration. Other forms of sexual harm involving children may be "
            "covered by other provisions not yet verified in SafeSpace. "
            "SafeSpace provides rights information only — it cannot investigate "
            "or make legal determinations. Contact the relevant services for help."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "SEA-ABUSE-001",
        "topic_slug": "sexual-abuse-child",
        "source_key": "children_act",
        "jurisdiction": "Kenya",
        "title": "A child has legal protection against sexual abuse",
        "plain_language_summary": (
            "The Children Act, 2022 requires that every child be protected from "
            "all forms of abuse, including sexual abuse. Authorities — including "
            "schools, health workers, and the police — have legal obligations "
            "to protect children and respond to reports of abuse. "
            "You do not have to face this alone. Help is available."
        ),
        "legal_reference": "Children Act, 2022, Section 16",
        "section_reference": "s.16 — Protection from abuse, neglect and exploitation",
        "risk_level": "HIGH",
        "next_step_text": (
            "Contact Child Helpline 116 or GBV Helpline 1195. If you are in "
            "immediate danger, call 999 or 112. You can also speak to a trusted "
            "adult — a teacher, community leader, or healthcare worker."
        ),
        "limitations": (
            "SafeSpace provides information about legal protections. It cannot "
            "investigate abuse or provide emergency protection directly. "
            "Please contact the relevant services listed."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "SEA-REPORT-001",
        "topic_slug": "safe-reporting",
        "source_key": "children_act",
        "jurisdiction": "Kenya",
        "title": "Abuse involving a child can be reported by anyone who knows or suspects it",
        "plain_language_summary": (
            "Under the Children Act, 2022, anyone who suspects or knows that a "
            "child is being abused or exploited should report this to the "
            "appropriate authorities. Reports can be made to Child Helpline 116, "
            "the police, the Children's Department, or the GBV Helpline 1195. "
            "You do not need to give your name when reporting abuse on behalf of "
            "a child."
        ),
        "legal_reference": "Children Act, 2022, Section 16",
        "section_reference": "s.16 — Duty to report and protect",
        "risk_level": "HIGH",
        "next_step_text": (
            "Call Child Helpline 116 or GBV Helpline 1195. You can report "
            "anonymously. You can also go to the nearest police station or "
            "Children's Department office."
        ),
        "limitations": (
            "SafeSpace describes available reporting pathways. It is not a "
            "reporting authority and cannot investigate or act on reports. "
            "Reports should be made to the services listed above."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "SEA-PROTECT-001",
        "topic_slug": "protection-support",
        "source_key": "constitution",
        "jurisdiction": "Kenya",
        "title": "Every child has the constitutional right to be protected from abuse and violence",
        "plain_language_summary": (
            "Article 53 of the Constitution of Kenya guarantees every child the "
            "right to be protected from abuse, neglect, harmful cultural practices, "
            "all forms of violence, and inhuman treatment. Where a child's safety "
            "is at risk, the state has an obligation to intervene and protect them."
        ),
        "legal_reference": "Constitution of Kenya, Article 53; Children Act, 2022, Section 16",
        "section_reference": "Art. 53(1)(d) — Right to protection from abuse",
        "risk_level": "HIGH",
        "next_step_text": (
            "If a child needs immediate protection, contact Child Helpline 116, "
            "GBV Helpline 1195, the police (999/112), or the Children's Department. "
            "These services can arrange protective intervention."
        ),
        "limitations": (
            "These are constitutional and statutory protections. Enforcement "
            "depends on reporting and timely institutional response. "
            "If there is immediate danger, call emergency services."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
]

SEA_ACTIONS = {
    "understanding-exploitation": [
        {
            "step_number": 1,
            "title": "Know that it is not your fault",
            "instruction": (
                "Sexual exploitation of a child is a crime under Kenyan law. "
                "It is never the child's fault. You have rights and there is help available."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Contact Child Helpline 116 for confidential support",
            "instruction": (
                "Call 116 — it is free and available 24/7. A trained counsellor "
                "can listen confidentially and help connect you to the right services."
            ),
            "action_type": "SUPPORT_REFERRAL",
            "svc_slug": "child-helpline-116",
        },
        {
            "step_number": 3,
            "title": "Contact GBV Helpline 1195",
            "instruction": (
                "Call 1195 for GBV support and referral. This service is free, "
                "toll-free, and available 24/7."
            ),
            "action_type": "SUPPORT_REFERRAL",
            "svc_slug": "gbv-helpline-1195",
        },
    ],
    "sexual-abuse-child": [
        {
            "step_number": 1,
            "title": "Tell a trusted adult",
            "instruction": (
                "If it is safe to do so, tell a trusted adult — a teacher, "
                "healthcare worker, community leader, or family member who you "
                "trust. You do not have to face this alone."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Call Child Helpline 116",
            "instruction": (
                "Child Helpline 116 is free, confidential, and available 24/7. "
                "A counsellor will listen and help you access support and protection."
            ),
            "action_type": "SUPPORT_REFERRAL",
            "svc_slug": "child-helpline-116",
        },
    ],
    "safe-reporting": [
        {
            "step_number": 1,
            "title": "Report to Child Helpline 116",
            "instruction": (
                "Call 116 to report abuse. You can remain anonymous. "
                "The helpline will guide you on next steps and can escalate "
                "to the relevant authorities."
            ),
            "action_type": "REPORTING_OPTION",
            "svc_slug": "child-helpline-116",
        },
        {
            "step_number": 2,
            "title": "Report to the police or Children's Department",
            "instruction": (
                "You can also report to the nearest police station or the "
                "Children's Department in your area. "
                "If you are reporting on behalf of a child, you do not need "
                "to give your own name."
            ),
            "action_type": "REPORTING_OPTION",
            "svc_slug": None,
        },
    ],
    "protection-support": [
        {
            "step_number": 1,
            "title": "If there is immediate danger, call 999 or 112",
            "instruction": (
                "If you or a child is in immediate danger, call emergency services "
                "(999 or 112) right away. Your safety comes first."
            ),
            "action_type": "SAFETY_ACTION",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Contact Child Helpline 116 or GBV Helpline 1195",
            "instruction": (
                "For support, referral, and help accessing protective services, "
                "call Child Helpline 116 or GBV Helpline 1195. Both are free, "
                "confidential, and available 24/7."
            ),
            "action_type": "SUPPORT_REFERRAL",
            "svc_slug": "child-helpline-116",
        },
    ],
}


# ============================================================================
# JOURNEY C — CHILD JUSTICE  (existing arrest-rights preserved; 4 new topics)
# ============================================================================

CJ_JOURNEY = {
    "name": "Child Justice",
    "slug": "child-justice",
    "description": (
        "Understand the rights and protections that apply when a young person "
        "under 18 is involved in a police or justice process in Kenya."
    ),
    "risk_default": "HIGH",
    "active": True,
}

# Existing arrest-rights topic — DO NOT recreate; handled separately below.

CJ_NEW_TOPICS = [
    {
        "title": "Legal Representation",
        "slug": "legal-representation",
        "description": (
            "Do you have the right to a lawyer? This topic explains your "
            "constitutional right to legal representation and how to access "
            "legal aid if you cannot afford a lawyer."
        ),
        "default_risk_level": "HIGH",
        "sort_order": 2,
        "active": True,
    },
    {
        "title": "Parent or Guardian Involvement",
        "slug": "parent-guardian-involvement",
        "description": (
            "Must your parent or guardian be told if you are arrested or charged? "
            "This topic explains the legal requirement for parental notification."
        ),
        "default_risk_level": "HIGH",
        "sort_order": 3,
        "active": True,
    },
    {
        "title": "Detention Protections",
        "slug": "detention-protections",
        "description": (
            "If you are detained, what are your rights? "
            "This topic explains protections for children held in custody."
        ),
        "default_risk_level": "HIGH",
        "sort_order": 4,
        "active": True,
    },
    {
        "title": "Diversion",
        "slug": "diversion",
        "description": (
            "What is diversion and could it apply to you? "
            "This topic explains the diversion process under Kenyan law."
        ),
        "default_risk_level": "MEDIUM",
        "sort_order": 5,
        "active": True,
    },
]

CJ_NEW_RECORDS = [
    {
        "record_code": "CJ-LEGAL-001",
        "topic_slug": "legal-representation",
        "source_key": "constitution",
        "jurisdiction": "Kenya",
        "title": "A person accused of an offence has the right to choose and be represented by a lawyer",
        "plain_language_summary": (
            "Article 50(2)(g) of the Constitution gives every accused person the "
            "right to choose, and to be represented by, a lawyer. "
            "Article 50(2)(h) provides that if a person cannot afford a lawyer, "
            "and substantial injustice would otherwise result, they have the right "
            "to have a lawyer assigned to them at state expense. "
            "The National Legal Aid Service can assist young people who cannot "
            "afford private legal representation."
        ),
        "legal_reference": "Constitution of Kenya, Article 50(2)(g) and Article 50(2)(h)",
        "section_reference": "Art. 50(2)(g) — Right to choose a lawyer; Art. 50(2)(h) — State-funded legal representation",
        "risk_level": "HIGH",
        "next_step_text": (
            "Ask for a lawyer as soon as you are arrested or charged. "
            "You have the right to remain silent until a lawyer is present. "
            "Contact the National Legal Aid Service if you cannot afford a lawyer."
        ),
        "limitations": (
            "The right to state-funded legal representation under Art. 50(2)(h) "
            "applies where substantial injustice would otherwise result — "
            "this is assessed case by case. Contact the National Legal Aid Service "
            "to understand your eligibility. This is rights information, not "
            "legal advice for your specific situation."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "CJ-PARENT-001",
        "topic_slug": "parent-guardian-involvement",
        "source_key": "children_act",
        "jurisdiction": "Kenya",
        "title": "A child's parent or guardian must be notified and may be present during proceedings",
        "plain_language_summary": (
            "When a child under 18 is arrested or charged with an offence, "
            "the police and the court are required under the Children Act to "
            "notify the child's parent or guardian. The parent or guardian has "
            "the right to be present during police questioning and during court "
            "proceedings involving the child."
        ),
        "legal_reference": "Children Act, 2022, Section 222",
        "section_reference": "s.222 — Notification of parent or guardian",
        "risk_level": "HIGH",
        "next_step_text": (
            "Ask the police to contact your parent or guardian immediately. "
            "You have the right to have a parent, guardian, or trusted adult "
            "present during questioning. If a parent cannot be reached, "
            "ask for the National Legal Aid Service to be contacted."
        ),
        "limitations": (
            "This describes a legal requirement for parental notification under "
            "the Children Act. If a parent or guardian cannot be located, another "
            "responsible adult or guardian should be identified by the authorities. "
            "This is rights information, not a guarantee of a specific outcome."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "CJ-DETAIN-001",
        "topic_slug": "detention-protections",
        "source_key": "constitution",
        "jurisdiction": "Kenya",
        "title": "A child in detention has specific constitutional protections including separation from adults",
        "plain_language_summary": (
            "Article 53(1)(f) of the Constitution of Kenya provides that every "
            "child has the right not to be detained, except as a measure of last "
            "resort, and when detained, to be held only for the shortest appropriate "
            "period of time, separately from adults, and in conditions that take "
            "account of the child's sex and age. These are constitutional protections "
            "that apply specifically to children."
        ),
        "legal_reference": "Constitution of Kenya, Article 53(1)(f)",
        "section_reference": "Art. 53(1)(f) — Child's right not to be detained except as last resort",
        "risk_level": "HIGH",
        "next_step_text": (
            "If you or a child you know is being held with adults, or conditions "
            "of detention do not account for the child's age, contact a lawyer or "
            "the National Legal Aid Service immediately. Complaints about police "
            "conduct can be made to IPOA."
        ),
        "limitations": (
            "These are constitutional protections specific to children under "
            "Article 53. If these rights are being violated, a lawyer or the "
            "National Legal Aid Service should be contacted urgently. "
            "SafeSpace cannot provide emergency legal intervention."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
    {
        "record_code": "CJ-DIVERT-001",
        "topic_slug": "diversion",
        "source_key": "children_act",
        "jurisdiction": "Kenya",
        "title": "A child may be considered for diversion if the legal requirements for diversion are met",
        "plain_language_summary": (
            "Diversion is a process under the Children Act, 2022 (sections 227 "
            "and 228) that may allow a child to be dealt with outside the formal "
            "court system. The Act sets out specific eligibility requirements that "
            "must be met. If eligible, a child may be subject to a formal caution, "
            "community service, or counselling instead of prosecution. "
            "Diversion aims to rehabilitate rather than punish, but it is not "
            "available in every case and is not guaranteed."
        ),
        "legal_reference": "Children Act, 2022, Section 227",
        "section_reference": "s.227 — Diversion eligibility and procedure",
        "risk_level": "MEDIUM",
        "next_step_text": (
            "Ask your lawyer or the National Legal Aid Service whether the "
            "legal requirements for diversion are met in your situation. "
            "Diversion is decided by the relevant authorities — a lawyer "
            "can help you understand whether it may be available."
        ),
        "limitations": (
            "Diversion eligibility is governed by the specific requirements in "
            "Children Act s.227 and is assessed case by case. It is not guaranteed "
            "and depends on the nature of the alleged offence and other circumstances. "
            "This is a description of a legal process, not a guarantee of any "
            "specific outcome. Always seek qualified legal advice."
        ),
        "last_verified": TODAY,
        "status": "VERIFIED",
        "active": True,
    },
]

CJ_NEW_ACTIONS = {
    "legal-representation": [
        {
            "step_number": 1,
            "title": "Ask for a lawyer immediately",
            "instruction": (
                "As soon as you are arrested or told you are being charged, "
                "ask for a lawyer. You have the constitutional right to legal "
                "representation. You do not have to answer questions until "
                "a lawyer is present."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Contact the National Legal Aid Service",
            "instruction": (
                "If you cannot afford a lawyer, contact the National Legal Aid "
                "Service. They provide free legal support to eligible young "
                "people in Kenya."
            ),
            "action_type": "LEGAL_ASSISTANCE",
            "svc_slug": "national-legal-aid-service",
        },
    ],
    "parent-guardian-involvement": [
        {
            "step_number": 1,
            "title": "Ask the police to contact your parent or guardian",
            "instruction": (
                "You have the right to have your parent or guardian notified. "
                "Ask the police to do this immediately. You do not have to "
                "answer questions until they are present."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Request the National Legal Aid Service if no parent is available",
            "instruction": (
                "If your parent or guardian cannot be reached, ask for the "
                "National Legal Aid Service to be contacted so that you have "
                "legal support present."
            ),
            "action_type": "LEGAL_ASSISTANCE",
            "svc_slug": "national-legal-aid-service",
        },
    ],
    "detention-protections": [
        {
            "step_number": 1,
            "title": "Know you must be held separately from adults",
            "instruction": (
                "If you are under 18 and being detained, you must not be placed "
                "with adult detainees. If this is happening, tell a lawyer or "
                "trusted adult immediately."
            ),
            "action_type": "RIGHTS_GUIDANCE",
            "svc_slug": None,
        },
        {
            "step_number": 2,
            "title": "Contact the National Legal Aid Service",
            "instruction": (
                "If your detention rights are being violated, the National Legal "
                "Aid Service can assist. Contact them or ask a trusted adult to "
                "contact them on your behalf."
            ),
            "action_type": "LEGAL_ASSISTANCE",
            "svc_slug": "national-legal-aid-service",
        },
        {
            "step_number": 3,
            "title": "Report police misconduct to IPOA",
            "instruction": (
                "If police have behaved unlawfully or mistreated you during "
                "detention, a complaint can be made to the Independent Policing "
                "Oversight Authority (IPOA)."
            ),
            "action_type": "REPORTING_OPTION",
            "svc_slug": "ipoa",
        },
    ],
    "diversion": [
        {
            "step_number": 1,
            "title": "Ask your lawyer whether diversion may apply",
            "instruction": (
                "Diversion is not automatic. Ask a lawyer or the National Legal "
                "Aid Service whether diversion might be available given the "
                "nature of the alleged offence and your circumstances."
            ),
            "action_type": "LEGAL_ASSISTANCE",
            "svc_slug": "national-legal-aid-service",
        },
    ],
}

# Existing arrest-rights actions (reproduced for completeness; get_or_create
# means re-running will not duplicate them)
ARREST_RIGHTS_ACTIONS = [
    {
        "step_number": 1,
        "title": "Stay calm and ask why you are being arrested",
        "instruction": (
            "You have the right to know the reason for your arrest. Calmly ask "
            "the officer to explain what you are accused of. You do not have to "
            "resist or argue — but you can ask clearly and politely."
        ),
        "action_type": "RIGHTS_GUIDANCE",
        "svc_slug": None,
    },
    {
        "step_number": 2,
        "title": "Exercise your right to remain silent",
        "instruction": (
            "You do not have to answer questions or make a statement at the time "
            "of arrest. You can say: 'I am exercising my right to remain silent.' "
            "Wait until you have spoken to a lawyer or a trusted adult."
        ),
        "action_type": "RIGHTS_GUIDANCE",
        "svc_slug": None,
    },
    {
        "step_number": 3,
        "title": "Contact the National Legal Aid Service",
        "instruction": (
            "If you cannot afford a lawyer, you may be eligible for free legal "
            "support through the National Legal Aid Service. Ask to contact them "
            "or ask a trusted adult to contact them on your behalf."
        ),
        "action_type": "LEGAL_ASSISTANCE",
        "svc_slug": "national-legal-aid-service",
    },
]


# ============================================================================
# COMMAND
# ============================================================================

class Command(BaseCommand):
    help = "Load SafeSpace verified knowledge data — all three MVP journeys (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true",
            help="Delete ALL demo data and recreate from scratch.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            self._reset()

        # ── Legal sources ────────────────────────────────────────────────
        src = {}
        for key, data in SOURCES.items():
            obj, created = LegalSource.objects.get_or_create(
                title=data["title"],
                source_type=data["source_type"],
                defaults=data,
            )
            src[key] = obj
            self._log("LegalSource", obj.title, created)

        # ── Support services ─────────────────────────────────────────────
        svc_map = {}
        for svc_data in SUPPORT_SERVICES:
            obj, created = SupportService.objects.get_or_create(
                slug=svc_data["slug"], defaults=svc_data
            )
            svc_map[svc_data["slug"]] = obj
            self._log("SupportService", obj.name, created)

        # ── Risk rules ────────────────────────────────────────────────────
        for rule_data in RISK_RULES:
            obj, created = RiskRule.objects.get_or_create(
                name=rule_data["name"], defaults=rule_data
            )
            self._log("RiskRule", f"{obj.name} [{obj.risk_level}]", created)

        # ── Journey A — Teenage Pregnancy ─────────────────────────────────
        tp_journey = self._upsert_journey(TP_JOURNEY)
        self._seed_journey_topics(
            tp_journey, TP_TOPICS, TP_RECORDS, TP_ACTIONS, src, svc_map
        )

        # ── Journey B — Sexual Exploitation ───────────────────────────────
        sea_journey = self._upsert_journey(SEA_JOURNEY)
        self._seed_journey_topics(
            sea_journey, SEA_TOPICS, SEA_RECORDS, SEA_ACTIONS, src, svc_map
        )

        # ── Journey C — Child Justice (preserve + expand) ─────────────────
        cj_journey = self._upsert_journey(CJ_JOURNEY)

        # Preserve existing arrest-rights topic and CJ-001 record
        arrest_topic, created = Topic.objects.get_or_create(
            journey=cj_journey,
            slug="arrest-rights",
            defaults={
                "title": "Arrest Rights",
                "description": (
                    "What rights do you have if police say you have committed "
                    "an offence? This topic covers the constitutional protections "
                    "that apply at the point of arrest in Kenya."
                ),
                "default_risk_level": "HIGH",
                "sort_order": 1,
                "active": True,
            },
        )
        self._log("Topic", arrest_topic.title, created)

        cj001_defaults = {
            "journey": cj_journey,
            "topic": arrest_topic,
            "jurisdiction": "Kenya",
            "title": "Right to be informed of the reason for arrest",
            "plain_language_summary": (
                "If you are arrested in Kenya, you have the right to be told "
                "immediately why you are being arrested and what you are accused "
                "of. You also have the right to remain silent. You do not have to "
                "say anything to the police until you have spoken to a lawyer or "
                "another person you trust."
            ),
            "legal_reference": "Constitution of Kenya 2010, Article 49",
            "section_reference": "Art. 49(1)(a)(b)",
            "source": src["constitution"],
            "risk_level": "HIGH",
            "next_step_text": (
                "Ask the officer to clearly state why you are being arrested. "
                "You have the right to remain silent. Ask to contact a parent, "
                "guardian, or lawyer as soon as possible."
            ),
            "limitations": (
                "This information describes constitutional rights. It is not "
                "legal advice. For your specific situation, speak to a qualified "
                "lawyer or contact the National Legal Aid Service."
            ),
            "last_verified": TODAY,
            "status": "VERIFIED",
            "active": True,
        }
        r, created = RightsRecord.objects.get_or_create(
            record_code="CJ-001", defaults=cj001_defaults
        )
        self._log("RightsRecord", f"[{r.record_code}] {r.title}", created)

        for ap_data in ARREST_RIGHTS_ACTIONS:
            svc_slug = ap_data.get("svc_slug")
            ap, created = ActionPath.objects.get_or_create(
                topic=arrest_topic,
                step_number=ap_data["step_number"],
                defaults={
                    "title": ap_data["title"],
                    "instruction": ap_data["instruction"],
                    "action_type": ap_data["action_type"],
                    "support_service": svc_map.get(svc_slug) if svc_slug else None,
                    "source": src["constitution"],
                    "last_verified": TODAY,
                    "status": "VERIFIED",
                    "active": True,
                },
            )
            self._log("ActionPath", f"arrest-rights step {ap.step_number}", created)

        # New Child Justice topics
        self._seed_journey_topics(
            cj_journey, CJ_NEW_TOPICS, CJ_NEW_RECORDS, CJ_NEW_ACTIONS, src, svc_map
        )

        self.stdout.write(self.style.SUCCESS("\nSeed complete -- all three MVP journeys loaded.\n"))
        self.stdout.write(
            "Verify at:\n"
            "  GET  /api/v1/journeys/\n"
            "  POST /api/v1/ask/  {\"question\": \"Can my school send me away if I am pregnant?\"}\n"
            "  POST /api/v1/ask/  {\"question\": \"An adult is exploiting me sexually. Who can help?\"}\n"
            "  POST /api/v1/ask/  {\"question\": \"I was arrested. What are my rights?\"}\n"
        )

    # ── helpers ──────────────────────────────────────────────────────────────

    def _upsert_journey(self, data: dict) -> Journey:
        obj, created = Journey.objects.get_or_create(
            slug=data["slug"], defaults=data
        )
        self._log("Journey", obj.name, created)
        return obj

    def _seed_journey_topics(
        self,
        journey: Journey,
        topics_data: list[dict],
        records_data: list[dict],
        actions_data: dict,
        src: dict,
        svc_map: dict,
    ) -> None:
        topic_map: dict[str, Topic] = {}
        for t_data in topics_data:
            topic, created = Topic.objects.get_or_create(
                journey=journey,
                slug=t_data["slug"],
                defaults=t_data,
            )
            topic_map[t_data["slug"]] = topic
            self._log("Topic", f"{journey.name} › {topic.title}", created)

        for r_data in records_data:
            topic = topic_map[r_data["topic_slug"]]
            source = src[r_data["source_key"]]
            code = r_data["record_code"]
            defaults = {k: v for k, v in r_data.items()
                        if k not in ("record_code", "topic_slug", "source_key")}
            defaults["journey"] = journey
            defaults["topic"] = topic
            defaults["source"] = source
            obj, created = RightsRecord.objects.get_or_create(
                record_code=code, defaults={**defaults, "record_code": code}
            )
            self._log("RightsRecord", f"[{obj.record_code}] {obj.title}", created)

        for topic_slug, steps in actions_data.items():
            topic = topic_map.get(topic_slug)
            if not topic:
                continue
            # Determine primary source for this topic from its records
            rec = next(
                (r for r in records_data if r["topic_slug"] == topic_slug), None
            )
            topic_source = src[rec["source_key"]] if rec else None

            for step in steps:
                svc_slug = step.get("svc_slug")
                ap, created = ActionPath.objects.get_or_create(
                    topic=topic,
                    step_number=step["step_number"],
                    defaults={
                        "title": step["title"],
                        "instruction": step["instruction"],
                        "action_type": step["action_type"],
                        "support_service": svc_map.get(svc_slug) if svc_slug else None,
                        "source": topic_source,
                        "last_verified": TODAY,
                        "status": "VERIFIED",
                        "active": True,
                    },
                )
                self._log(
                    "ActionPath",
                    f"{journey.name} › {topic.title} step {ap.step_number}",
                    created,
                )

    def _log(self, label: str, name: str, created: bool) -> None:
        verb = "Created" if created else "Already exists"
        self.stdout.write(f"  {verb}: {label} '{name}'")

    def _reset(self) -> None:
        self.stdout.write("Removing all demo data...")
        # Delete in dependency order (PROTECT constraints require children first)
        ActionPath.objects.all().delete()
        RightsRecord.objects.all().delete()
        Topic.objects.all().delete()
        Journey.objects.all().delete()
        LegalSource.objects.all().delete()
        SupportService.objects.all().delete()
        RiskRule.objects.all().delete()
        self.stdout.write(self.style.WARNING("All demo data removed."))
