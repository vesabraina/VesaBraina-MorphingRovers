# Morphing Rovers: Dizajni dhe Analiza e Algoritmeve

Projekt për lëndën "Dizajni dhe Analiza e Algoritmeve", mbi sfidën e ESA-s **SpOC-2 Morphing Rovers**.

Përshkrimi zyrtar i problemit: https://optimize.esa.int/challenge/spoc-2-morphing-rovers/About

## Problemi
Një rover në Mars duhet të arrijë te një mostër në 30 skenarë (6 harta), brenda 500 hapave.
Roveri ka 4 forma (për terrene të ndryshme) dhe një rrjet neural që vendos drejtimin dhe formën.
I gjithë roveri përshkruhet me një varg prej **19 133 numrash**:
- 484 numra: 4 format e roverit (4 × 11 × 11)
- 18 642 numra: peshat e rrjetit neural
- 7 numra të plotë: arkitektura e rrjetit

Funksioni i vlerësimit (nga ESA) e simulon roverin dhe kthen një notë. **Sa më e ulët nota, aq më mirë.**

## Qëllimi
Të gjejmë me algoritme optimizimi pa derivate roverin me notën më të ulët,
t'i krahasojmë algoritmet (nota, numri i vlerësimeve, koha),
dhe ta bëjmë kërkimin më të shpejtë.

## Teknologjia dhe burimet
- Gjuha: Python (Jupyter notebooks në Kaggle)
- Përshkrimi i problemit: https://optimize.esa.int/challenge/spoc-2-morphing-rovers/About
- Funksioni i vlerësimit dhe të dhënat: repository zyrtar i ESA-s, https://github.com/esa/SpOC2
- Algoritmet e optimizimit: puna ime

## Struktura
```
VesaBraina-MorphingRovers/
├── notebooks/                      # Eksplorimi hap pas hapi
│   ├── 01_Setup.ipynb              # Setup në Kaggle, roveri shembull i ESA-s
│   ├── 02_Eksplorimi.ipynb         # Hartat, koordinatat, rrugët e roverit
│   ├── 03_RandomSearch.ipynb       # Algoritmi 1: Random Search
│   ├── 04_KohaCPUvsGPU.ipynb       # Matja e kohës CPU kundër GPU
│   ├── 05_HillClimbing.ipynb       # Algoritmi 2: Hill Climbing
│   ├── 06_AlgoritmiGjenetik.ipynb  # Algoritmi 3: Algoritmi gjenetik
│   └── 07_CMAES.ipynb              # Algoritmi 4: CMA-ES (diagonal)
├── src/
│   └── algoritmet.py               # Kodi final: 4 algoritmet + vlerësim paralel
├── checkpoints/                    # Roverat më të mirë (.npy)
├── images/                         # Grafikët e rezultateve
├── requirements.txt                # Libraritë: numpy, torch, matplotlib, cma
└── README.md
```
Notebook-et 01-07 janë eksplorimi hap pas hapi; kodi final është në `src/algoritmet.py`.

## Rezultatet deri tani
| Metoda | Nota më e mirë | Vlerësime | Koha |
|---|---|---|---|
| Roveri shembull i ESA-s | 7.98 | 1 | 24 s |
| Random Search | 7.488 | 10 | 312 s |
| Hill Climbing | 5.421 | 15 | 385 s |
| Algoritmi gjenetik | 4.739 | 38 | 775 s |
| CMA-ES | **4.618** | 30 | 818 s |

**Rekordi në Leaderboard e ESA-s:** 1.856 (Team HRI)

**CPU vs GPU (1000 rovera, shtresa Conv2d):** CPU 4.41 s, GPU 0.118 s, rreth 37 herë më shpejt.

**Vërejtje për algoritmin gjenetik:** nota 4.739 u gjet në popullatën e parë (me mutacion të roverit të Hill Climbing). Gjatë 5 gjeneratave mesatarja e popullatës u përmirësua (nga 7.397 në 6.738), por roveri më i mirë jo. Checkpoint-i i ruajtur (ga_best.npy), kur u vlerësua sërish, dha notën 4.828, prandaj CMA-ES nisi nga 4.828.

## Grafikët
### 1. Random Search
Nota e secilit prej 10 roverave të rastësishëm. Notat janë të shpërndara dhe nuk përmirësohen me kohë, sepse algoritmi nuk mëson nga provat. Më i miri: 7.488.

<img width="471" height="327" alt="random_search" src="https://github.com/user-attachments/assets/2201cf5a-3e6e-4d1f-8d25-c1c64ffac11f" />

### 2. Hill Climbing
Nota më e mirë pas çdo hapi. Vija vetëm bie ose mbetet njësoj, sepse pranohen vetëm ndryshimet që e përmirësojnë roverin. Nga 7.98 në 5.421 me 15 vlerësime, pastaj ngeci (optimum lokal).

<img width="471" height="327" alt="hill_climbing" src="https://github.com/user-attachments/assets/a42820f2-9b6f-4a95-9126-2e3435c6d77c" />

### 3. Algoritmi gjenetik
Nota më e mirë dhe mesatarja e popullatës për çdo gjeneratë. Më e mira (4.739) u gjet që në popullatën e parë dhe u ruajt falë elitizmit, ndërsa mesatarja ra nga 7.397 në 6.738, që tregon se e gjithë popullata po përmirësohej.

<img width="471" height="327" alt="algoritmi_gjenetik png" src="https://github.com/user-attachments/assets/d2255078-6ac9-466c-b1a0-12bf868af777" />

### 4. CMA-ES
Provimi i parë me hap 0.3 nuk e përmirësoi roverin (4.828): fëmijët kishin mesatarisht notë 9.5, sepse ndryshimi i 19 mijë numrave njëkohësisht me hap të madh e prish roverin. Me hap 0.02, nota ra nga 4.828 në **4.618** për 5 gjenerata. Mësimi: me kaq shumë numra, hapat duhet të jenë të vegjël.

<img width="571" height="427" alt="cmaes png" src="https://github.com/user-attachments/assets/fca7e0dd-af1e-41e1-8798-3d6ae3f1f72a" />


## Algoritmet dhe pse këto
Funksioni i vlerësimit është "kuti e zezë": simulim pa formulë dhe pa derivat.
Prandaj nuk mund të përdoren gradient descent, programimi dinamik apo brute force
(hapësira e kërkimit ka 19 133 numra realë). Përdorim algoritme optimizimi pa derivate
(metaheuristika), nga më i thjeshti te më i avancuari:

| Algoritmi | Ideja | Përparësia | Dobësia |
|---|---|---|---|
| Random Search | Provo rovera krejt të rastësishëm, mbaje më të mirin | Shumë i thjeshtë, pikë krahasimi | Nuk mëson asgjë nga provat |
| Hill Climbing | Ndrysho pak roverin më të mirë, pranoje nëse përmirësohet | Përmirësim i shpejtë | Ngec në optimum lokal |
| Algoritmi gjenetik | Popullatë roverash, kryqëzim dhe mutacion | Shmang ngecjen | Kërkon më shumë vlerësime |
| CMA-ES | Mëson drejtimin dhe madhësinë e hapit të kërkimit | Standard për probleme me shumë numra realë | Më kompleks, varet nga hapi fillestar |

## Shpejtësia: CPU dhe GPU
Një vlerësim zgjat ~24 s dhe algoritmeve u duhen qindra vlerësime.
Simulimi i ESA-s lëviz një rover në një kohë, prandaj ekzekutohet në CPU.
Plani: (1) vlerësimi i disa roverave njëkohësisht në 4 procesorët CPU të Kaggle,
(2) si bonus, rishkrimi i simulimit që GPU të lëvizë shumë rovera përnjëherë.

## Si ekzekutohet
1. Hape notebook-un në Kaggle, Internet = On.
2. Kutia e parë shkarkon kodin e ESA-s dhe rregullon dy gabime të vogla.
3. Run All. Notebook-et ekzekutohen me radhë sipas numrave.

## Hapat e ardhshëm
- Kodi i algoritmeve në src/algoritmet.py dhe dataset-e në Kaggle
- Krahasimi head to head i 4 algoritmeve (e njëjta pikënisje, i njëjti numër vlerësimesh)
- Ekzekutimi i gjatë i algoritmit fitues, për notë sa më afër rekordit
