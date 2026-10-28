# Morphing Rovers: Dizajni dhe Analiza e Algoritmeve

Projekt për lëndën "Dizajni dhe Analiza e Algoritmeve", mbi sfidën e ESA-s **SpOC-2 Morphing Rovers**.

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

## Teknologjia
- Gjuha: Python (Jupyter notebooks në Kaggle, GPU T4)
- Funksioni i vlerësimit dhe të dhënat: repository zyrtar i ESA-s, github.com/esa/SpOC2
- Algoritmet e optimizimit dhe versioni GPU: puna ime

## Struktura
| Notebook | Përmbajtja |
|---|---|
| 01_Setup.ipynb | Setup në Kaggle, testimi i roverit shembull të ESA-s |
| 02_Eksplorimi.ipynb | Hartat, koordinatat dhe rrugët e roverit |
| 03_RandomSearch.ipynb | Algoritmi i parë: Random Search |
| 04_KohaCPUvsGPU.ipynb | Matja e kohës: gjyqtari i ESA-s në CPU dhe prova CPU kundër GPU |

## Rezultatet deri tani
| Metoda | Nota më e mirë | Vlerësime | Koha |
|---|---|---|---|
| Roveri shembull i ESA-s | 7.98 | 1 | 24 s |
| Random Search | 7.488 | 10 | 312 s |

## Hapat e ardhshëm
- Hill Climbing
- Algoritmi gjenetik
- Strategjitë evolutive (CMA-ES)
- Simulimi i shumë roverave njëkohësisht në GPU
