# Tech Machinist Bros

Android-first Expo prototype for a 100-question, 10-level machining adventure starring selectable animated versions of Elon and Sam.

## Game loop

1. Pick a machinist.
2. Answer ten shop questions to move across a production-line board.
3. Complete a touch-based machine or inspection challenge.
4. Unlock the next station.
5. Finish all ten stations to release the master assembly.

The included question bank covers safety, measurement, drilling, lathe work, milling, CNC, threads, welding/fabrication, quality, and production. Questions are stored separately in `questions.js`, so future generated packs can be added without changing the game UI.

## Run on Android

Install Expo Go on the phone. On a computer with Node installed, unzip this project, run `npm install`, then `npm run start`, and scan the Expo QR code. For a standalone APK, use Expo Application Services after adding an Expo project ID and Android package name.

## Art direction

The prototype uses original geometric character tokens and machine diagrams. Final production art should use a legally cleared, original 1990s theatrical-animation look rather than copying protected studio character designs.

## Infinite expansion plan

Each generated question should store: skill, machine, material, variables, formula, answer, distractors, explanation, difficulty, and a validation checksum. Formula templates can safely vary diameter, tolerance, surface speed, flute count, chip load, coordinates, bend allowance, and inspection data. Generated questions must be recomputed by a deterministic validator before entering play.
