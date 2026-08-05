# Zero Trust Architecture (ZTA): A Research Overview

## 1. Introduction

Traditional network security models operate on the principle of **"trust but verify"** — once a user or device is inside the network perimeter (e.g., connected via VPN or on the corporate LAN), it is implicitly trusted. This "castle-and-moat" approach has repeatedly failed against modern threats such as insider attacks, lateral movement after a single compromised credential, and cloud/remote-work environments where there is no clear "perimeter" anymore.

**Zero Trust Architecture (ZTA)** flips this model with the core principle:

> **"Never trust, always verify."**

No user, device, or application is trusted by default — regardless of whether it is inside or outside the network. Every access request is continuously authenticated, authorized, and encrypted based on all available context.

---

## 2. Motivation for the Research

- Rise of remote work, BYOD (Bring Your Own Device), and cloud-first infrastructure has dissolved the traditional network perimeter.
- High-profile breaches (e.g., SolarWinds, Colonial Pipeline) showed how a single compromised credential can lead to full network compromise under perimeter-based trust.
- Regulatory pressure (NIST SP 800-207, US Executive Order 14028) is pushing organizations toward Zero Trust adoption.
- Growing attack surface from IoT, microservices, and third-party APIs.

**Research Question Examples:**
- How effective is ZTA in reducing lateral movement compared to traditional VPN-based access?
- What are the performance/latency trade-offs of continuous authentication in ZTA?
- How can ZTA be implemented cost-effectively in small/medium enterprises (SMEs)?
- How does ZTA integrate with legacy systems that were not designed for it?

---

## 3. Core Principles of Zero Trust (NIST SP 800-207)

| Principle | Description |
|---|---|
| **Verify Explicitly** | Always authenticate and authorize based on all available data points — identity, location, device health, service, data classification, anomalies. |
| **Least Privilege Access** | Limit user/service access with Just-In-Time (JIT) and Just-Enough-Access (JEA) policies. |
| **Assume Breach** | Design the system assuming an attacker is already inside; minimize blast radius via segmentation. |
| **Micro-segmentation** | Divide the network into small zones to contain breaches. |
| **Continuous Monitoring** | Real-time logging, analytics, and behavioral analysis to detect anomalies. |

---

## 4. Key Components / Architecture

```
                     +---------------------------+
                     |   Policy Decision Point    |
                     |          (PDP)              |
                     +---------------------------+
                              |     ^
                       Policy |     | Trust
                       Engine |     | Algorithm
                              v     |
+--------+   Request   +---------------------------+   Grant/Deny   +-----------+
| Subject | ----------> |   Policy Enforcement Point | -------------> | Resource  |
| (User/  |             |          (PEP)              |                | (App/DB/  |
| Device) | <---------- +---------------------------+ <-------------  | Service)  |
+--------+   Response                                                 +-----------+
```

- **Policy Engine (PE):** Decides whether to grant access based on policy and trust score.
- **Policy Administrator (PA):** Establishes/terminates the communication path.
- **Policy Enforcement Point (PEP):** Enables, monitors, and terminates connections between subject and resource.
- **Trust Algorithm:** Continuously calculates a trust score using contextual signals (device posture, geolocation, behavior, threat intel).

---

## 5. Example Use Case: Corporate Employee Accessing an Internal App

**Scenario:** An employee wants to access an internal HR portal from home.

**Traditional model:** Employee connects to VPN → gets full network access → can reach almost anything on the internal network.

**Zero Trust model:**
1. Employee authenticates via **MFA** (identity verification).
2. Device posture is checked (Is antivirus updated? Is disk encrypted? Is OS patched?).
3. Policy Engine evaluates context: location, time of access, device trust score.
4. Access is granted **only to the HR portal**, not the entire network (micro-segmentation).
5. Session is continuously monitored; if anomalous behavior is detected (e.g., sudden data download at 3 AM from a new country), access is revoked mid-session.

---

## 6. Example Implementation Stack (for a research prototype)

| Layer | Example Tools/Technologies |
|---|---|
| Identity & Access Management | Keycloak, Okta, Azure AD |
| Multi-Factor Authentication | TOTP (Google Authenticator), FIDO2/WebAuthn |
| Device Posture Check | Microsoft Intune, Jamf, custom agent script |
| Micro-segmentation | Istio Service Mesh, Cilium, VMware NSX |
| Policy Engine | Open Policy Agent (OPA), Google BeyondCorp |
| Continuous Monitoring | SIEM (Splunk, ELK Stack), UEBA tools |
| Encryption | mTLS (mutual TLS) between all services |

**Mini Python-style pseudocode for a simple trust-score-based Policy Engine:**

```python
def evaluate_access(user, device, context):
    trust_score = 0

    if user.mfa_verified:
        trust_score += 30
    if device.is_patched and device.antivirus_active:
        trust_score += 25
    if context.location in user.usual_locations:
        trust_score += 20
    if context.time_of_day in user.usual_working_hours:
        trust_score += 15
    if not context.anomaly_detected:
        trust_score += 10

    if trust_score >= 70:
        return "ACCESS_GRANTED"
    elif trust_score >= 40:
        return "STEP_UP_AUTH_REQUIRED"  # e.g., ask for OTP again
    else:
        return "ACCESS_DENIED"
```

---

## 7. Comparison: Traditional Security vs Zero Trust

| Aspect | Traditional (Perimeter-based) | Zero Trust |
|---|---|---|
| Trust model | Trust inside, verify outside | Never trust, always verify |
| Network access | Broad, once inside VPN | Granular, per-resource |
| Lateral movement risk | High | Low (micro-segmentation) |
| Authentication | Once at login | Continuous |
| Suitability for cloud/remote work | Poor | Strong |
| Implementation complexity | Lower | Higher (initial setup) |

---

## 8. Challenges / Open Research Problems

- **Legacy system integration** — old systems may not support modern identity protocols (SAML/OAuth/mTLS).
- **Performance overhead** — continuous verification can add latency.
- **User experience** — too much re-authentication can frustrate users.
- **Cost** — full ZTA rollout can be expensive for SMEs.
- **Standardization** — lack of unified implementation guidelines across vendors.
- **AI/ML-driven anomaly detection** — improving accuracy of behavioral trust scoring without high false-positive rates.

---

## 9. Suggested Research Directions

1. **Lightweight Zero Trust for IoT networks** — resource-constrained devices can't run heavy agents.
2. **AI-based continuous trust scoring** — using ML models to dynamically adjust trust scores in real time.
3. **Zero Trust in Cloud-Native (Kubernetes) environments** — service-to-service mTLS + OPA policies.
4. **Cost-benefit analysis of ZTA adoption in SMEs vs enterprises.**
5. **Zero Trust for hybrid/multi-cloud environments.**

---

## 10. References (starting points for literature review)

- NIST Special Publication 800-207 — *Zero Trust Architecture*
- Google BeyondCorp whitepapers
- CISA Zero Trust Maturity Model
- Forrester's original Zero Trust Model (Kindervag, 2010)

---

*Prepared as a research topic overview — expand each section with citations, diagrams, and experimental data as per your paper/thesis format.*
