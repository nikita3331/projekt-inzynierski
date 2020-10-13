# Instrukcja uruchomienia

Uruchamiamy program w pliku testEverything.py

**Zawartość plików**
1. Testeverything.py zawiera tworzenie randomowych punktów oraz uruchamia triangulację. Pozwala również na wyświetlenie obiektu.
2. MyDelaunay ,to klasa zawierająca naszą triangulację. Znajdują się w niej funkcje do triangulacji. Oprócz tego są tam funkcje poboczne, na przykład do konwersji tablicy punktów do tablicy indeksów tych punktów. Jest to wymagane przez programy generujące modele .ply . Jest też funkcja do wyliczania wektorów normalnych do powierzchni ściany czworościanu w celu lepszego ich wyświetlania. 
3. Tetra.py jest to klasa będąca czworościanem. Znajdują się tam funkcje do badania czy punkt jest wewnątrz sfery opisanej na bryle jak również sprawdzanie czy czworościan jest poprawnie zbudowany czyli czy z 4 pkt utworzyliśmy czworościan a nie trójkąt. 
4. Point3D jest klasa przechowująca punkty będące wierzchołkami czworościanu. Mamy tam konwersję na array i tupel by można było na nich wykonywać operacje.
