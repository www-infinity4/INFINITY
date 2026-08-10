# Android Chrome Security Lab

## Purpose

This section documents a reproducible, evidence-first method for investigating abnormal Android battery drain that appears to correlate with Chrome or web activity.

The original observation behind this module was simple: abnormal battery behavior appeared, Chrome storage was cleared, and the battery behavior returned to normal. That is a useful diagnostic clue, but it is **not proof of hacking** by itself. The goal here is to separate measurable symptoms from assumptions and build a repeatable incident-response workflow.

## Core model

```text
Normal device
   |
   v
Chrome / website activity
   |
   +--> tabs, JavaScript, media, notifications
   +--> cached site data, service workers, storage
   +--> downloads, permissions, background sync
   |
   v
CPU + network + radio + memory activity
   |
   v
battery drain / heat / lag
```

A second path must also be considered when there is evidence of compromise:

```text
malicious page or download
   |
   v
permission abuse / harmful app / exploited vulnerability
   |
   v
persistent background activity
   |
   v
measurable indicators
```

## What clearing Chrome storage can tell us

If a problem stops immediately after Chrome storage or site data is cleared, reasonable hypotheses include:

- a runaway tab or script
- a broken or overly active service worker
- repeated background network requests
- notification or site-permission abuse
- corrupted browser state or cache
- storage pressure causing repeated reads/writes or process churn

It does **not** establish who caused the behavior or whether the device was intentionally attacked.

## Evidence before conclusions

Treat every incident as a small experiment. Record:

1. battery percentage and time
2. phone temperature or whether it feels unusually hot
3. Chrome battery usage compared with other apps
4. Chrome storage size
5. active tabs and recently visited sites
6. notification permissions granted to websites
7. recent downloads, especially APK files
8. Android apps installed recently
9. Accessibility, Device Admin, VPN and unknown-app-install permissions
10. whether the behavior continues in Airplane Mode or Safe Mode

## Chrome security checks

On current Android Chrome builds, use Chrome **Settings > Safety check** and review Safe Browsing, updates, compromised passwords, notification permissions and unused site permissions.

Keep Safe Browsing enabled. Chrome can warn about known malware, phishing, abusive sites, intrusive ads and dangerous downloads.

## Android security checks

Use Google Play Protect to scan installed apps. Also inspect:

- Settings > Apps
- Settings > Accessibility
- Settings > Security / Device admin apps
- Settings > Network / VPN
- Settings > Install unknown apps
- Settings > Battery > Battery usage

Any unfamiliar app with Accessibility, Device Admin or broad background privileges deserves closer review.

## Battery-specific safety

Security investigation is separate from physical battery safety. If the phone is swelling, deforming, producing a chemical smell, becoming dangerously hot or refusing to charge normally, stop treating it as a browser problem and have the battery/device inspected.

## Infinity integration

This module is designed to become part of the broader Infinity documentation system. Future security modules can use the same pattern:

```text
OBSERVATION -> MEASUREMENT -> HYPOTHESIS -> TEST -> RESULT -> CONFIDENCE
```

That format allows the system to preserve ideas and incidents without converting an unverified theory into a fact.

## Files in this module

- `INCIDENT-LOG.md` — structured event recording
- `THREAT-MODEL.md` — realistic browser and Android attack surfaces
- `CHROME-FORENSICS.md` — browser-specific diagnostic workflow
- `ANDROID-CHECKLIST.md` — fast device-security checklist

## Reference points

Primary reference material should favor official Android, Chrome and device-vendor documentation. Useful Google topics include Chrome Safety Check, Chrome Safe Browsing, removal of unwanted software, Play Protect and Android app-permission controls.

---

**Status:** defensive research and incident documentation. This repository does not claim that a specific battery-drain event was an intrusion unless supporting evidence is collected.