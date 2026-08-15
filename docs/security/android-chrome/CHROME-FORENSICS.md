# Chrome Forensics on Android

## Goal

Determine whether an abnormal event is primarily browser state, website behavior, a downloaded application, an Android-level problem, or hardware/battery degradation.

## Fast isolation sequence

### A. Capture the state before clearing anything

When practical, record battery percentage and time, Chrome position in Android Battery Usage, device heat, active tabs, Chrome storage size, recent downloads, websites with notification permissions, and whether redirects or pop-ups are occurring.

### B. Run Chrome Safety Check

Open Chrome > Settings > Safety check. Review warnings for Safe Browsing, compromised passwords, updates, unwanted notifications and unused site permissions.

### C. Inspect site permissions

Review Chrome > Settings > Site settings, especially Notifications, Camera, Microphone, Location, Pop-ups and redirects, and download permissions. Revoke anything unfamiliar or unnecessary.

### D. Inspect downloads

Look for files you did not intentionally download. APK files deserve special attention because they can cross the boundary from browser content into installed software if installation from that source is enabled.

### E. Test browser-state hypotheses

Use the least destructive test first:

1. close suspicious tabs
2. stop/restart Chrome
3. remove permissions for a suspicious site
4. clear that site's data when possible
5. clear Chrome cache
6. clear broader Chrome storage/data only if needed

Record which action changes the symptom.

## Interpreting a successful reset

If clearing Chrome storage immediately resolves battery drain, record: **Browser-state reset correlated with resolution.** Do not automatically record: **Attack confirmed.** The reset may have removed malicious site state, but it can also remove legitimate yet broken cached data, runaway scripts, background web state or corrupted application data.

## Safe Mode comparison

If symptoms continue after Chrome is reset, Android Safe Mode can help distinguish third-party apps from core system/hardware behavior. If the problem disappears in Safe Mode, recently installed or privileged third-party apps become stronger candidates.

## Network comparison

Compare battery behavior during normal connectivity with Airplane Mode. A major difference can indicate radio/network traffic, weak signal or network-active software. It does not identify the responsible party by itself.

## Evidence hierarchy

Strong evidence includes a specific harmful app identified by Play Protect or security tooling, an unknown app with dangerous privileges, a suspicious APK matching the timeline, unauthorized account sessions, a known vulnerability with matching indicators, or reproducible process/network behavior identifying the responsible component.

Weak evidence includes battery drain alone, warmth alone, nearly full storage, a problem disappearing after reboot, or a problem disappearing after cache clearing. Weak evidence can start an investigation; it should not finish one.