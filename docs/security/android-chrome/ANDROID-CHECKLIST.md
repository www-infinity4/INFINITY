# Android Security Checklist

Use this checklist when battery drain, heat, redirects, unknown notifications or other suspicious behavior appears.

## Immediate capture

- [ ] Note time and battery percentage
- [ ] Screenshot Battery Usage
- [ ] Note whether the phone is unusually hot
- [ ] Record Wi-Fi/cellular state
- [ ] Screenshot suspicious notifications or redirects

## Chrome

- [ ] Run Chrome Safety Check
- [ ] Review Site settings > Notifications
- [ ] Review Camera, Microphone and Location permissions
- [ ] Check Pop-ups and redirects
- [ ] Review Downloads for unknown files or APKs
- [ ] Close suspicious tabs
- [ ] Clear only the suspicious site's data first when possible
- [ ] Clear broader Chrome storage only after recording evidence

## Android

- [ ] Run Google Play Protect
- [ ] Review recently installed apps
- [ ] Review Accessibility services
- [ ] Review Device Admin apps
- [ ] Review VPN configuration
- [ ] Review Install unknown apps permissions
- [ ] Review apps allowed to display over other apps
- [ ] Review notification access when available
- [ ] Install Android, Google Play system, Chrome and WebView updates

## Isolation tests

- [ ] Restart the device
- [ ] Compare behavior in Airplane Mode
- [ ] Compare behavior in Android Safe Mode
- [ ] Re-check Battery Usage after each test

## Account checks when warranted

- [ ] Review Google account security activity
- [ ] Review signed-in devices/sessions
- [ ] Change passwords if unauthorized access is found
- [ ] Enable or verify multi-factor authentication

## Hardware safety

If the battery is swelling, deforming the case, emitting odor, or becoming dangerously hot, stop charging/using it and seek hardware service. Do not continue treating those symptoms as a browser-only incident.

## Classification

End each investigation with one of these labels:

- **Observed anomaly**
- **Likely browser-state problem**
- **Likely application problem**
- **Likely hardware/network problem**
- **Security concern requiring more evidence**
- **Confirmed compromise**

Only use the last label when specific evidence supports it.