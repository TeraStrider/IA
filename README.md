# IA
Inteligenta Artificiala - UPB 2020-2021



## Laboratoare
### Laborator 1 - A*
Se foloseste _A*_ pentru a se gasi drumul de lungime minima intre 2 puncte
dintr-un sistem de coordonate carteziene. Nu exista costuri la trecerea dintr-o
celula in alta, iar euristicile folosite sunt distanta euclidiana si cea
Manhattan.

#### Nota
Daca se elimina `sqrt()` din distanta euclidiana, **pare** ca algoritmul se
comporta mai bine, dar asta e o pura intamplare, din moment ce fara `sqrt()`
euristica nu mai e admisibila. De fapt, explorand mai putine stari, algoritmul
ar putea ajunge la un rezultat gresit daca ar fi rulat pentru o problema mai
complexa


### Laborator 2 - Arbore SI/SAU
Se foloseste un *arbore SI/SAU* pentru a se modela comportamentul unui aspirator
**nedeterminist** intr-un spatiu 1D, unde celulele pot fi fie curate, fie
murdare. Nedeterminismul consta in faptul ca atunci cand aspiratorul curata o
celula, exista 2 posibilitati:
- Celula era curata $\Rightarrow$ aceasta se poate ramane curata sau se poate
murdari
- Celula era murdara $\Rightarrow$ aceasta va fi curatat, dar se poate ca si
celula din dreapta sa fie curatata

#### Nod SAU
Reprezinta o decizie. In fiecare stare, sunt maxumum 3 actiuni posibile: `Left`,
`Right`, `Clean`. Fiii unui nod **SAU** reprezinta efectele acestor decizii,
daca ar deveni actiuni. Deci daca oricare dintre ele duce la o stare de succes
(in care toate celulele sunt cu siguranta curate), atunci si nodul poate duce
la o stare de succes.

#### Nod SI
Reprezinta o actiune in sine. Pentru actiunile de miscare (`Left`, `Right`), are
un singur fiu, noua pozitie in care ajunge aspiratorul. Pentru actiunea `Clean`,
nedeterminismul aspiratorului inseamna ca pentru a fi siguri ca acest nod duce
la o stare de succes, e nevoie ca ambele situatii care se pot obtine in urma
acestei actiuni (descrise mai sus) sa duca la succes, pentru ca nu stim care
scenariu se va intampla in cazul unei functionari a aspiratorului.

#### Plan
La final se creeaza un *plan* de actiune, un fel de algoritm care descrie
deciziile aspiratorului in functie de mediu (curatenia celulelor).


### Laborator 3 - PCSP
Se implementeaza un algoritm generic de rezolvare a unei probleme de satisfacere
a constrangerilor care admite un numar dat de abateri de la constrangerile date.
Algoritmul folosit este un *BKT* clasic care nu mai viziteaza nodurile de pe o
ramura atunci cand numarul de abateri de la constragneri de pe aceasta depaseste
numarul minim global gasit pana in acel moment, deoarece ce pe acea ramura nu
mai se poate gasi o asignare de variabile cu un cost mai mic decat minimul
curent.


### Laborator 4 - MCTS
Se implementeaza algoritmul *Monte Carlo Tree Search* pe un joc de
[connect 4](https://en.wikipedia.org/wiki/Connect_Four)


### Laborator 5 - Unificare in logica cu predicate de ordinul I
Se foloseste
[algoritmul Robinson](https://en.wikipedia.org/wiki/Unification_(computer_science)#A_unification_algorithm)
pentru a se realiza unificarea a doua formule, pe baza unui dictionar de
substitutii (care se completeaza pe parcursul algoritmului).

Bine ca de data asta putem sa alegem singuri cum reprezentam datele...


### Laborator 6 - Rezolutie in logica cu predicate de ordinul I
Se utilizeaza rezolutia pentru a demonstra propozitii.


### Laborator 7 - Forward Chaining
Se demonstreaza o serie de teoreme (implicatii) folosind forward chaining.
Teoremele sunt formulate in _FNC_ si se folosesc functiile implementate in
laboratoarele anterioare (`unify()` si `substitute()`) pentru a aplica un set
de fapte unor premise, astfel incat sa se obtina noi fapte.


### Laborator 8 - Graphplan
In lab e implementat algoritmul *Graphplan* care creeaza o planificare de
actiuni cu scopul de a ajunge la o anumita stare. Starile sunt definite ca o
lista de predicate. Algoritmul se bazeaza pe 2 notiuni:

#### Predicate mutex
Sunt predicate care se contrazic (de ex.: `A` si `~A`). Aceste predicate nu pot
face parte din aceeasi stare.

#### Actiuni mutex
Sunt actiuni care au cel putin unul dintre preconditii sau efecte in mutex.
Aceste actiuni nu se pot executa simultan.

Pe baza mutecsilor descrisi mai sus, se creeaza o lista de actiuni posibile, una
de actiuni aflate in mutex (au oricare dintre premise sau efecte in relatie de
mutex), alta de efecte ale actiunilor antementionate si inca una cu efectele
aflate in mutex.


### Laborator 9 - Seminar retele bayesiene
Niste tractoare scarboase de rezolvat pe hartie. Calcule chioare de
probabilitati si nimic mai mult. Nu merita sa ajunga pe Git...


### Laborator 10 - Eliminarea variabilelor din retele bayesiene
Se implementeaza reguli care reduc dimensiunea _factorilor_ (tabelelor de
probabilitati) din nodurile unei retele bayesiene.

#### Multiplicare
Un join intre 2 factori prin care se inmultesc probabilitatile liniilor care fac
match.

#### Insumare
Se elimina o variabila dintr-un factor adunand valorile intrarilor unde
variabila respectiva are valori opuse (se poate ignora pentru ca se considera
si cazul in care e adevarata si cel in care nu).

#### Reducere conform cu observatiile
Daca observam ca o variabila are o anumita valoare, putem elimina intrarile cu
valoarea opusa din toti factorii in care apare variabila.



## Teme
### Tema 1 - Cautari informate in spatiul starilor
Se implementeaza si se compara performantele algoritmilor `DFID`, `IDA*`,
`LRTA*` si [Branch and Bound](https://artint.info/html/ArtInt_63.html). Se
afieseaza caile gasite de agent de la starea initiala pana la cea finala,
costurile gasite de acesta pentru fiecare stare explorata, precum si timpii si
memoria utilizata in cadrul fiecarui algoritm.

### Tema 2 - Game about Squares
Se implementeaza un algoritm de rezolvare a nivelurilor din jocul "Game about
Squares". Se foloseste algoritmul Best First ce foloseste euristica euclidiana,
impreuna cu doua strategii de eliminare a starilor ce nu pot duce la o stare
castigatoare.

### Tema 3 - Clasificarea si rezumarea articolelor de stiri
Se foloseste algoritmul Naive Bayes pentru a clasifica articole de stiri dupa
domeniul acestora. Acelasi algoritm este folosit si pentru rezumarea acestor
articole. Rezumatele sunt create de catre model selectand unele propozitii din
articolul initial. Se antreneaza si se compara rezultatele obtinute atat cu
monograme cat si cu bigrame.
