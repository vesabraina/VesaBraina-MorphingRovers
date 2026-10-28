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
dhe ta bëjmë kërkimin më të shpejtë me GPU.

## Teknologjia dhe burimet
- Gjuha: Python (Jupyter notebooks në Kaggle, GPU T4)
- Përshkrimi i problemit: https://optimize.esa.int/challenge/spoc-2-morphing-rovers/About
- Funksioni i vlerësimit dhe të dhënat: repository zyrtar i ESA-s, https://github.com/esa/SpOC2
- Algoritmet e optimizimit dhe versioni GPU: puna ime

## Struktura
| Notebook / Dosja | Përmbajtja |
|---|---|
| 01_Setup.ipynb | Setup në Kaggle, testimi i roverit shembull të ESA-s |
| 02_Eksplorimi.ipynb | Hartat, koordinatat dhe rrugët e roverit |
| 03_RandomSearch.ipynb | Algoritmi i parë: Random Search |
| 04_KohaCPUvsGPU.ipynb | Matja e kohës: gjyqtari i ESA-s në CPU dhe prova CPU kundër GPU |
| 05_HillClimbing.ipynb | Algoritmi i dytë: Hill Climbing (përmirësim hap pas hapi) |
| checkpoints/ | Roverat më të mirë të ruajtur (.npy), që algoritmet e ardhshme të vazhdojnë prej tyre |
| images/ | Grafikët e rezultateve |

## Rezultatet deri tani
| Metoda | Nota më e mirë | Vlerësime | Koha |
|---|---|---|---|
| Roveri shembull i ESA-s | 7.98 | 1 | 24 s |
| Random Search | 7.488 | 10 | 312 s |
| Hill Climbing | 5.421 | 15 | 385 s |

## Grafikët
<img width="571" height="427" alt="random_search" src="https://github.com/user-attachments/assets/2201cf5a-3e6e-4d1f-8d25-c1c64ffac11f" />
<img width="846" height="646" alt="hill_climbing" src="https://github.com/user-attachments/assets/a42820f2-9b6f-4a95-9126-2e3435c6d77c" />


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
| CMA-ES | Mëson drejtimin e mirë të kërkimit | Standard për probleme me shumë numra realë | Më kompleks |

## Pse GPU
Një vlerësim zgjat ~24 s në CPU dhe algoritmeve u duhen qindra vlerësime.
GPU llogarit shumë rovera njëkohësisht (paralelizëm), prandaj e rishkruajmë
simulimin që të vlerësojë shumë rovera përnjëherë.

## Si ekzekutohet
1. Hape notebook-un në Kaggle, Accelerator = GPU T4, Internet = On.
2. Kutia e parë shkarkon kodin e ESA-s dhe rregullon dy gabime të vogla.
3. Run All. Notebook-et ekzekutohen me radhë sipas numrave.

## Hapat e ardhshëm
- Algoritmi gjenetik
- Strategjitë evolutive (CMA-ES)
- Simulimi i shumë roverave njëkohësisht në GPU
