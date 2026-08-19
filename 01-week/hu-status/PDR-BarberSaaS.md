# Product Requirements Document (PRD)
## BarberSaaS — Multi-Tenant Barbershop Management Platform

---

| Field | Details |
|---|---|
| **Document version** | 1.0 |
| **Status** | In Development |
| **Product owner** | Carlos Leal,Daniel Cerquera,Juan Pablo Borrero, Carolay Arraut |
| **Last updated** | August 2026 |
| **Confidentiality** | Internal — Proprietary |

---

## Table of Contents

1. Executive Summary
2. Problem Statement
3. Goals & Success Metrics
4. Target Users & Personas
5. Market Context
6. Product Scope
7. Functional Requirements
8. Non-Functional Requirements
9. System Architecture Overview
10. Data Model & Database
11. API Design Principles
12. Security & Compliance
13. Monetization Model
14. Release Roadmap
15. Risks & Mitigations
16. Open Questions
17. Appendix

---

## 1. Executive Summary

BarberSaaS is a cloud-based, multi-tenant SaaS platform designed to digitize and streamline the operations of barbershops across Colombia. It provides a complete suite of tools for barbershop owners, barbers, and clients, covering appointment scheduling, staff management, loyalty programs, inventory tracking, and financial reporting — all accessible from a single mobile application.

The platform targets the underserved barbershop market in Colombia, where the vast majority of businesses still rely on WhatsApp groups, paper notebooks, and verbal agreements to manage their day-to-day operations. BarberSaaS brings the operational capabilities previously available only to large salon chains within reach of any independent barbershop, at a fraction of the cost.

The business model is a monthly SaaS subscription with a 60-day free trial, giving shop owners enough time to experience the full value of the product before committing to a paid plan.

---

## 2. Problem Statement

### The Current Reality

Barbershops in Colombia — particularly in mid-sized cities like Neiva, Ibagué, Pasto, and Cúcuta — face a set of recurring operational problems that directly impact their revenue and client retention:

**For barbershop owners:**
- No reliable way to track individual barber performance (clients served, revenue generated).
- Manual income/expense tracking on paper or basic spreadsheets, with no consolidated financial view.
- No loyalty program to incentivize repeat clients, leaving client retention entirely to personal relationships.
- Inability to manage appointment scheduling — clients call, text, or simply show up, causing queues and frustration.
- No formal way to track inventory (hair products, tools) or generate restock alerts.

**For barbers:**
- No visibility into their own daily schedule or upcoming appointments.
- No clear metric of how many clients they've served or how much revenue they've contributed.
- Manual coordination with the shop owner for every schedule change.

**For clients:**
- No way to book an appointment in advance without calling or messaging.
- No loyalty tracking — they accumulate visits mentally with no formal reward system.
- No confirmation or reminders for upcoming appointments.

### The Gap

Existing solutions (Booksy, Fresha, Treatwell) are designed for and priced for Western markets. They lack Spanish-language support tailored to Colombian colloquialisms, don't support the specific operational patterns of Colombian barbershops (e.g., walk-in clients tracked without registration, offline-first scenarios), and carry pricing that puts them out of reach for small independent shops.

---

## 3. Goals & Success Metrics

### Business Goals

| Goal | Metric | Target (12 months post-launch) |
|---|---|---|
| Acquire paying barbershops | Number of active paid subscriptions | 50 barbershops |
| Validate retention | Monthly churn rate | < 5% |
| Generate recurring revenue | Monthly Recurring Revenue (MRR) | COP $5,000,000 |
| Expand geographically | Cities with active barbershops | 5+ cities |

### Product Goals

| Goal | Metric | Target |
|---|---|---|
| Appointment digitization | % of appointments booked through the app | > 70% within 30 days of onboarding |
| Notification delivery | Push notification delivery rate | > 95% |
| Platform reliability | API uptime | > 99.5% |
| Client experience | Time to complete booking (from search to confirmation) | < 90 seconds |

### Leading Indicators (Early Validation)

- At least 3 barbershops complete their first full week of operations on the platform within 30 days of launch.
- At least 80% of onboarded barbershops configure their service catalog and at least one barber schedule within the first 48 hours.
- At least one loyalty redemption per barbershop within the first 30 days.

---

## 4. Target Users & Personas

### Persona 1 — The Barbershop Owner (ADMIN_BARBERSHOP)
**Name:** Carlos, 34 years old, Neiva  
**Context:** Owns a barbershop with 2–4 barbers. Has a smartphone, uses WhatsApp daily, has basic comfort with apps but no technical background. His biggest pain is not knowing at the end of the month whether he made or lost money, and not being able to hold barbers accountable for their performance.  
**Goal:** Understand his business numbers, control his team's schedule, and keep clients coming back.  
**Frustration:** "I don't know how much each barber brings in. I just trust them."

### Persona 2 — The Barber (BARBER)
**Name:** Andrés, 24 years old  
**Context:** Works at a barbershop as an employee. Very comfortable with smartphones and social media. Wants to build his own client base and knows his reputation depends on reliability.  
**Goal:** See his daily agenda, know when clients are coming, and track how many services he has completed.  
**Frustration:** "Clients show up whenever, and I never know if it's going to be a busy day or empty."

### Persona 3 — The Client (CLIENT)
**Name:** María, 28 years old  
**Context:** Regular client at a barbershop. Always books via WhatsApp, sometimes forgets her appointment. Loves the idea of earning a free haircut after visiting enough times.  
**Goal:** Book easily, get reminded of her appointment, and feel valued as a loyal customer.  
**Frustration:** "I have to send a message and wait for a reply to know if there's availability."

### Persona 4 — The Platform Administrator (SUPER_ADMIN)
**Name:** Internal team member  
**Context:** Manages the entire BarberSaaS platform. Creates barbershop accounts, manages subscription plans, monitors platform health, and handles escalations.  
**Goal:** Maintain visibility over all active barbershops, manage billing cycles, and suspend or reactivate accounts as needed.

---

## 5. Market Context

### Competitive Landscape

| Competitor | Strengths | Weaknesses vs. BarberSaaS |
|---|---|---|
| **Booksy** | Strong brand, global presence | English-first UX, pricing in USD, not adapted to Colombian workflows |
| **Fresha** | Commission-free model, good UI | Lacks Spanish localization for Colombia, requires stable internet |
| **WhatsApp + notebooks** | Zero cost, familiar | No scheduling logic, no financial tracking, no loyalty, human error-prone |
| **Custom Excel sheets** | Flexible | No real-time, no mobile, no automation |

### Market Opportunity

- Colombia has approximately 80,000+ registered barbershops and hair salons (DANE, 2023).
- The mid-sized city segment (Neiva, Ibagué, Pasto, Manizales, Montería) is largely unserved by digital tools.
- Average monthly spend on operational tools by barbershops in this segment: < COP $50,000.
- Target addressable market (barbershops in cities with 100k–500k population): ~15,000 businesses.

---

## 6. Product Scope

### In Scope — MVP

- Multi-tenant architecture with tenant isolation by `barbershop_id`
- Four user roles: SUPER_ADMIN, ADMIN_BARBERSHOP, BARBER, CLIENT
- Appointment booking with real-time availability and anti-double-booking
- Service catalog management per barbershop
- Employee (barber) management and schedule configuration
- Loyalty card system (stickers + automatic reward coupon)
- Financial records (income/expense tracking per barbershop)
- Inventory management with stock alerts
- Push notifications (FCM) for appointment events
- Email notifications for password recovery
- Super-admin platform dashboard (all barbershops, plans, revenue)
- Self-registration for barbershop owners with 60-day free trial
- Subscription plan management

### Out of Scope — MVP (Future Phases)

- In-app payment processing (Stripe, PSE, Nequi integration)
- Client-facing web app for QR-based booking (no app installation required)
- Advanced analytics and reporting exports (PDF, Excel)
- Multi-location barbershop chains under a single account
- Marketplace / discovery platform for clients to find new barbershops
- Integration with Google Calendar or Apple Calendar
- Automated billing and dunning management

---

## 7. Functional Requirements

### 7.1 Authentication & Identity

| ID | Requirement | Priority |
|---|---|---|
| AUTH-01 | Users register with email, password, full name, and phone number | Must Have |
| AUTH-02 | All authenticated sessions use JWT with claims: userId, role, barbershopId | Must Have |
| AUTH-03 | Tokens expire after 24 hours; refresh tokens valid for 7 days | Must Have |
| AUTH-04 | Password recovery via 6-digit code sent to registered email (expires in 15 min) | Must Have |
| AUTH-05 | Barbershop owners self-register in a 3-step wizard (account → barbershop → plan) | Must Have |
| AUTH-06 | Barbers are registered by the barbershop admin; they do not self-register | Must Have |

### 7.2 Appointment System

| ID | Requirement | Priority |
|---|---|---|
| APPT-01 | Clients can search barbershops by city/location and view availability | Must Have |
| APPT-02 | Clients can book an appointment by selecting service, barber, date, and time slot | Must Have |
| APPT-03 | System prevents double-booking using pessimistic locking at the database level | Must Have |
| APPT-04 | Appointments follow a state machine: PENDING → CONFIRMED → IN_PROGRESS → COMPLETED | Must Have |
| APPT-05 | Clients can cancel appointments subject to the barbershop's cancellation policy (configurable hours) | Must Have |
| APPT-06 | Clients can reschedule appointments, triggering re-confirmation | Must Have |
| APPT-07 | Admins and barbers can mark appointments as NO_SHOW | Must Have |
| APPT-08 | Walk-in clients can be added by the admin directly to a barber's agenda without client registration | Must Have |
| APPT-09 | Appointment reminders are sent via push notification 1 hour before the scheduled time | Should Have |

### 7.3 Loyalty & Rewards

| ID | Requirement | Priority |
|---|---|---|
| LOYAL-01 | Each barbershop configures a loyalty program: number of stickers required and reward description | Must Have |
| LOYAL-02 | Admins and barbers can grant stickers to clients from the completed appointment view or by searching the client | Must Have |
| LOYAL-03 | When a client accumulates enough stickers, the admin/barber can redeem the reward | Must Have |
| LOYAL-04 | Redemption automatically generates an active coupon for the client | Must Have |
| LOYAL-05 | The coupon is automatically applied as a 100% discount on the client's next booking at that barbershop | Must Have |
| LOYAL-06 | Clients can view their loyalty card (sticker count, progress, reward description, active coupon) | Must Have |

### 7.4 Staff & Schedule Management

| ID | Requirement | Priority |
|---|---|---|
| STAFF-01 | Admins can add, edit, and deactivate employees (barbers) | Must Have |
| STAFF-02 | Each barber has a configurable weekly schedule with time slots | Must Have |
| STAFF-03 | Schedule exceptions (days off, modified hours) can be added per barber | Must Have |
| STAFF-04 | The availability algorithm considers the barber's schedule and existing appointments | Must Have |

### 7.5 Financial Tracking

| ID | Requirement | Priority |
|---|---|---|
| FIN-01 | Admins can register income and expense records manually | Must Have |
| FIN-02 | Dashboard shows total revenue, total expenses, and net profit for a given period | Must Have |
| FIN-03 | Revenue from completed appointments is automatically recorded | Should Have |

### 7.6 Notifications

| ID | Requirement | Priority |
|---|---|---|
| NOTIF-01 | Push notifications are sent for: appointment booked, confirmed, cancelled, completed | Must Have |
| NOTIF-02 | All notifications are persisted in the database regardless of FCM delivery status | Must Have |
| NOTIF-03 | Users can view their in-app notification history | Should Have |
| NOTIF-04 | Email is used exclusively for password recovery in MVP | Must Have |

### 7.7 Super Admin

| ID | Requirement | Priority |
|---|---|---|
| SA-01 | Super admin can view all barbershops, their status, and subscription plan | Must Have |
| SA-02 | Super admin can create, update, and deactivate subscription plans | Must Have |
| SA-03 | Super admin can manually create a barbershop and assign its first admin | Must Have |
| SA-04 | Super admin can activate, suspend, or cancel a barbershop's account | Must Have |
| SA-05 | Platform dashboard shows: total barbershops, active/trial/suspended, total clients, total revenue | Must Have |

---

## 8. Non-Functional Requirements

### 8.1 Performance

| Requirement | Target |
|---|---|
| API response time (p95) | < 300ms for read operations |
| API response time (p95) | < 500ms for write operations (appointment creation) |
| Concurrent users supported (MVP) | 500 simultaneous users |
| Appointment creation under load | No double-booking under concurrent requests |

### 8.2 Availability & Reliability

| Requirement | Target |
|---|---|
| API uptime | > 99.5% monthly |
| Graceful degradation | FCM unavailability must not block appointment creation |
| Database backups | Daily automated backups, 30-day retention |

### 8.3 Scalability

The system is designed as a modular monolith capable of horizontal scaling behind a load balancer. The stateless JWT authentication enables this without session affinity. Extraction of high-load bounded contexts (e.g., Notifications) into independent services is explicitly planned as a future ADR trigger (see ADR-001).

### 8.4 Security

| Requirement | Implementation |
|---|---|
| Authentication | JWT (HS512), 24h expiry |
| Tenant isolation | `barbershop_id` validated in every service operation via `TenantContext` |
| Password storage | BCrypt (strength 10) |
| Transport security | HTTPS enforced in production (TLS 1.2+) |
| Sensitive config | All secrets via environment variables, never hardcoded |
| Firebase credentials | Service account JSON excluded from version control |

### 8.5 Internationalization

- Language: Spanish (Colombia) — all UI strings, error messages, and emails.
- Currency: Colombian Peso (COP), formatted with `.toLocaleString('es-CO')`.
- Timezone: `America/Bogota` (UTC-5) as default for all barbershops.
- Date/time formatting: DD/MM/YYYY, 12-hour clock.

---

## 9. System Architecture Overview

### Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Mobile frontend** | React Native + Expo SDK 54 + Expo Router | Single codebase for Android/iOS; file-based routing; fast iteration |
| **State management** | Zustand (auth) + TanStack Query (server state) | Lightweight, no boilerplate; automatic cache invalidation |
| **Backend** | Spring Boot 3.3.4 + Java 21 | Production-grade, strong typing, excellent JPA/Security ecosystem |
| **Authentication** | JWT (jjwt 0.12.6) + Spring Security | Stateless, scalable, no server-side session needed |
| **Database** | PostgreSQL | ACID compliance, superior JSON support, better performance at scale vs MySQL |
| **Cache / Pub-Sub** | Redis | Session invalidation, future rate limiting |
| **Push notifications** | Firebase Admin SDK (FCM) | Native push for Android and iOS via a single integration |
| **Email** | Gmail SMTP (Spring Mail) | Zero-cost for MVP volume; migrate to Resend/SES at scale |
| **Build & Deploy (mobile)** | EAS Build (Expo Application Services) | Cloud-based native builds without local Android/iOS toolchain |
| **Hosting (backend)** | Railway (planned) | Zero-config deployment for Spring Boot + PostgreSQL; automatic TLS |

### Architecture Pattern

**Modular Monolith** — one deployable unit, internally structured by bounded context. See ADR-001 for the full rationale and future extraction triggers.

```
┌─────────────────────────────────────────────────────┐
│                  Spring Boot Application            │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐│
│  │   auth   │ │ barber-  │ │    appointment       ││
│  │          │ │  shop    │ │                      ││
│  └──────────┘ └──────────┘ └──────────────────────┘│
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐│
│  │ loyalty  │ │ finance  │ │   notification       ││
│  │          │ │          │ │                      ││
│  └──────────┘ └──────────┘ └──────────────────────┘│
│              shared: domain entities, security      │
└──────────────────────┬──────────────────────────────┘
                       │ JDBC
               ┌───────▼────────┐
               │   PostgreSQL   │
               │  (barbersaas)  │
               └────────────────┘
```

---

## 10. Data Model & Database

### Database: PostgreSQL

PostgreSQL was selected over MySQL for the following reasons:

| Factor | PostgreSQL | MySQL |
|---|---|---|
| JSON/JSONB support | Native JSONB with indexing | JSON stored as text, limited indexing |
| Concurrent write performance | MVCC — no read/write lock contention | Can exhibit table-level locks in some engines |
| Full-text search | Built-in `tsvector` / `tsquery` | Requires MyISAM or external tooling |
| Array and custom types | Native | Not supported |
| Standards compliance | Closest to SQL standard | Some deviations |
| Future analytics | Compatible with read replicas, Timescale, Citus | Limited ecosystem for analytical workloads |
| Cloud hosting | First-class support on Railway, Render, Supabase, AWS RDS | Also supported but PostgreSQL preferred |

> **Note:** The current development environment uses MySQL. Migration to PostgreSQL is planned before the first production deployment. The JPA/Hibernate abstraction layer minimizes the required code changes — primarily dialect configuration and a schema re-generation.

### Core Tables (abbreviated)

```
users                  — all roles, barbershop_id FK nullable for CLIENT/SUPER_ADMIN
barbershops            — name, city, status (TRIAL/ACTIVE/SUSPENDED/CANCELLED), trial_ends_at
subscription_plans     — name, price, max_barbers, features_json, is_active
barber_profiles        — user_id FK, bio, photo_url
barber_services        — barbershop_id FK, name, price, duration_minutes
barber_schedules       — barber_profile_id FK, day_of_week, start_time, end_time
schedule_exceptions    — barber_profile_id FK, exception_date, is_day_off
appointments           — client_id, barber_id, service_id, date, start/end_time, status, price_at_booking
loyalty_cards          — client_id FK, barbershop_id FK, stickers_count, total_rewards_redeemed
loyalty_rewards_config — barbershop_id FK, stickers_required, reward_description, is_active
loyalty_transactions   — loyalty_card_id FK, type (GRANT/REDEEM), granted_by_id
reward_coupons         — client_id FK, barbershop_id FK, status (ACTIVE/USED), appointment_id FK nullable
finance_records        — barbershop_id FK, type (INCOME/EXPENSE), amount, description, date
inventory_products     — barbershop_id FK, name, stock, min_stock_alert
notifications          — user_id FK, title, body, type, is_read
device_tokens          — user_id FK, token, platform (android/ios)
password_reset_tokens  — user_id FK, token (6-digit), expires_at, used
```

### Multi-Tenancy Enforcement

Every table that stores barbershop-scoped data includes `barbershop_id`. Tenant context is resolved from the JWT on every request and stored in a `ThreadLocal` (`TenantContext`). All service-layer methods validate that the resource being accessed belongs to the authenticated tenant before returning data.

---

## 11. API Design Principles

- **RESTful** — resources as nouns, HTTP verbs for actions.
- **Versioning** — currently unversioned (MVP); `v1` prefix to be added before public API release.
- **Route naming convention:**
  - `/api/public/**` — unauthenticated (search, registration, public plans)
  - `/api/auth/**` — authentication endpoints
  - `/api/client/**` — CLIENT role only
  - `/api/barber/**` — BARBER role (and ADMIN_BARBERSHOP where shared)
  - `/api/admin/**` — ADMIN_BARBERSHOP role
  - `/api/super-admin/**` — SUPER_ADMIN role only
- **Error format:**
  ```json
  {
    "error": "Human-readable message in Spanish",
    "fields": { "fieldName": "Validation error message" }
  }
  ```
- **Documentation** — Swagger UI available at `/swagger-ui.html` (dev profile only).

---

## 12. Security & Compliance

### Data Privacy

- Client personal data (name, email, phone) is stored only within the barbershop's tenant scope.
- No personal data is shared across tenants.
- Password reset codes expire in 15 minutes and are invalidated after use.
- Firebase service account credentials are never committed to version control.

### Recommendations Before Production

- [ ] Move `JWT_SECRET` to a secrets manager (AWS Secrets Manager, Railway secrets).
- [ ] Enable HTTPS-only (already handled by Railway's automatic TLS).
- [ ] Add rate limiting on `/api/auth/**` endpoints to prevent brute-force attacks.
- [ ] Implement token revocation list (Redis) for logout invalidation.
- [ ] Add audit logging for sensitive actions (plan changes, account suspensions).

---

## 13. Monetization Model

### Subscription Plans

| Plan | Price (COP/month) | Max Barbers | Target |
|---|---|---|---|
| Starter | $39,900 | 2 | Solo barber or very small shop |
| Profesional | $79,900 | 5 | Standard barbershop |
| Premium | $149,900 | Unlimited | Multi-barber shops, chains |

### Free Trial

- All new barbershops start on a **60-day free trial** (status: `TRIAL`).
- `trial_ends_at` is set to `created_at + 60 days` at registration.
- After the trial, the Super Admin manually transitions the account to `ACTIVE` upon payment confirmation (MVP: manual billing).
- Accounts that do not convert are transitioned to `SUSPENDED`.

### Future Monetization (Post-MVP)

- Automated billing via Stripe or PayU (PSE, Nequi, credit cards).
- Annual plan discount (2 months free for annual commitment).
- Add-on: advanced analytics dashboard.
- Add-on: multi-location management.

---

## 14. Release Roadmap

### Phase 1 — Private Beta (Current)
- ✅ Core backend (8 phases: auth, appointments, loyalty, notifications, finance, inventory)
- ✅ Mobile app — all 4 roles functional end-to-end
- ✅ Self-registration wizard for barbershop owners
- ✅ FCM push notifications (development build)
- ✅ Password recovery via email
- 🔄 Walk-in client tracking (in progress)
- 🔄 Trial expiration automation (in progress)

### Phase 2 — Controlled Launch (Q4 2026)
- Migration to PostgreSQL
- Backend deployment on Railway
- Production EAS Build (Play Store + App Store)
- Terms & Conditions and Privacy Policy
- Custom barbershop icon and splash screen
- Trial-to-paid conversion flow

### Phase 3 — Growth (Q1 2027)
- Client web app (QR-based booking, no app install required)
- Automated billing (PayU / Stripe)
- Advanced reporting and PDF exports
- Referral program for barbershop owners

---

## 15. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Low adoption due to unfamiliarity with digital tools | High | High | Onboarding flow in < 5 minutes; in-person setup support for first barbershops |
| FCM delivery failures on poor network | Medium | Medium | All notifications persisted in DB; in-app inbox always available |
| Gmail SMTP rate limit exceeded | Low | Medium | Monitor volume; migrate to Resend/SES before reaching 500 emails/day |
| Double-booking under high concurrency | Low | High | Pessimistic DB lock on appointment creation; tested under load |
| Trial abuse (re-registering to reset trial) | Medium | Medium | Email uniqueness constraint; Super Admin review for suspicious patterns |
| MySQL → PostgreSQL migration issues | Low | Medium | JPA abstraction minimizes changes; schema tested in PostgreSQL before migration |
| App Store rejection | Low | Medium | Privacy Policy, permissions justification, and test account ready for review |

---

## 16. Open Questions

| # | Question | Owner | Target resolution |
|---|---|---|---|
| 1 | What is the exact pricing strategy for the Colombian market? | Product | Before Phase 2 launch |
| 2 | Should barbers receive a revenue share report within the app? | Product | Phase 2 |
| 3 | Should the client web app support full booking or only registration + redirect to app? | Engineering | Phase 3 scoping |
| 4 | How will the Super Admin be notified when a trial is about to expire? | Engineering | Phase 2 |
| 5 | Is there a legal requirement to store client data within Colombia? | Legal | Before production |
| 6 | Will the platform support iOS at launch or Android only? | Product | Phase 2 |

---

## 17. Appendix

### A. Glossary

| Term | Definition |
|---|---|
| **Tenant** | A barbershop registered on the platform. All their data is scoped by `barbershop_id`. |
| **Walk-in client** | A client who arrives without a prior appointment. Tracked in the system without requiring account registration. |
| **Sticker** | A loyalty point granted by a barber or admin after a completed service. |
| **Coupon** | An automatically generated reward granting a 100% discount on the client's next booking. |
| **Trial** | The 60-day free period granted to newly registered barbershops. |
| **TenantContext** | A ThreadLocal-based Java class that stores the authenticated user's `userId`, `barbershopId`, and `role` for the duration of a single HTTP request. |
| **EAS Build** | Expo Application Services Build — cloud-based compilation of the React Native app into a native APK/IPA. |
| **PRD** | Product Requirements Document — this document. |
| **ADR** | Architecture Decision Record — a document capturing a specific architectural decision, its alternatives, and consequences. |

### B. Related Documents

- `docs/ADR-001-barbersaas.md` — Architecture Decision Record (modular monolith, JWT, PostgreSQL, FCM)
- `db/init.sql` — Database initialization script (development seed data)
- `src/main/resources/application.yml` — Backend configuration
- `app.json` — Expo/React Native build configuration

### C. Contacts

| Role | Contact |
|---|---|
| Product Owner / Lead Developer | Carlos Leal |
| Platform Email (transactional) | sasbarberias@gmail.com |
| Expo Project | carlosleal / barbersaas-mobile |
| Firebase Project | barbersaas (Spark plan) |
