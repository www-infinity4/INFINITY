# Android + Chrome Threat Model

## Scope

This document maps realistic ways a browser-related event can become a device-security event on Android. It is defensive documentation for diagnosis, prevention and evidence collection.

## Trust boundaries

```text
Internet
  |
  v
Website / ad / download
  |
  v
Chrome sandbox
  |
  +--> site data
  +--> notifications
  +--> camera/mic/location permissions
  +--> downloads
  +--> external app intents
  |
  v
Android application boundary
  |
  +--> installed apps
  +--> Accessibility
  +--> Device Admin
  +--> VPN
  +--> unknown-app installation
  |
  v
accounts / files / sensors / network / battery
```

## Threat classes

### 1. Resource-abusive web content

A page can consume substantial CPU, GPU, memory, network and radio resources through scripts, media, animation, repeated requests or badly behaved background components. The result can look dramatic: heat, lag and battery loss. This is a performance/security concern but is not automatically proof of device compromise.

### 2. Notification and permission abuse

A site that has been granted notification or other permissions can create persistent nuisance behavior. Review and revoke permissions that are unnecessary or unfamiliar.

### 3. Phishing and social engineering

A page may impersonate a trusted service, display false virus warnings or attempt to convince the user to reveal credentials, change settings or install software.

### 4. Dangerous downloads

Browser downloads become higher risk when they lead to installation of an APK or another executable payload. Android's unknown-app-install controls and Play Protect are important boundaries here.

### 5. Harmful installed applications

A malicious or unwanted app can outlive the browser session. High-impact permissions include Accessibility, Device Admin, VPN, notification access, overlay/display-over-other-apps and broad background activity.

### 6. Browser or OS vulnerability exploitation

Browsers and operating systems can contain security vulnerabilities. Keeping Chrome, Android System WebView, Google Play system components and the Android OS patched reduces exposure. A real exploit should be treated as a specific technical hypothesis requiring evidence, not assumed from battery drain alone.

### 7. Account compromise

Some events that appear to originate on a phone are actually account-level problems: stolen passwords, unauthorized sessions, malicious forwarding/rules or compromised recovery settings. Account security should be checked separately from device security.

### 8. Non-adversarial causes

Always keep these in the model:

- aging battery
- poor cellular signal
- defective charger/cable
- background synchronization
- OS update/indexing
- high screen brightness
- GPS/navigation
- camera/video processing
- corrupted application data
- storage pressure

## Severity model

| Level | Meaning | Example |
|---|---|---|
| 0 | normal | expected battery consumption |
| 1 | anomaly | Chrome unexpectedly dominates battery usage |
| 2 | browser abuse | persistent redirects, abusive notifications, suspicious site behavior |
| 3 | device concern | unknown app or privileged permission discovered |
| 4 | confirmed compromise | malware/security tooling or forensic evidence confirms unauthorized code/activity |
| 5 | account + device incident | confirmed compromise crosses accounts, device or financial identity |

## Response rule

Escalate based on evidence, not fear:

```text
symptom
 -> reproduce
 -> isolate browser vs device
 -> inspect permissions/apps
 -> preserve evidence
 -> remove confirmed cause
 -> rotate credentials only when warranted
 -> update and monitor
```

## Design principle for Infinity

Security modules should distinguish three states:

- **Observed** — directly seen or measured
- **Inferred** — best explanation from available evidence
- **Confirmed** — independently demonstrated or detected

This distinction keeps the larger Infinity knowledge system useful for both unconventional hypotheses and conventional engineering analysis without confusing one with the other.