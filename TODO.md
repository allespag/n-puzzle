# n-puzzle

## *.py

* Docstrings ffs !

## npuzzle.py

<!-- * Trouver une façon de vérifier l'égalité entre 2 Npuzzle. Une idée naive :

```python
class Npuzzle:
    def __init__(self, n: int, tiles: list[int]) -> None:
        # ...some checks...

        self.n = n
        self.tiles = tiles
    
    def __eq__(self, other: Npuzzle) -> bool:
        return self.tiles == other.tiles
```

Le problème sur cette implémentation c'est que `0` dans `self.titles` peut être n'importe ou. Il faut du coup, vérifier que tous les nombres dans `self.tiles` sont dans le bon ordre **sans compter les 0**.

**UPDATE**: pour le moment la solution est la suivante. Cependant elle n'a pas était encore testé.

**UPDATE2**: A cause de ma compréhension du sujet, la solution naive est *pour le moment* la bonne solution

```python
    def __eq__(self, other: Npuzzle) -> bool:
        a = self.tiles.copy()
        b = other.tiles.copy()
        a.remove(EMPTY_TILE)
        b.remove(EMPTY_TILE)

        return a == b
``` -->

<!-- * J'ai 4 fonctions type "utils" dans ce fichier :

```python
# npuzzle.py
def index_in_list(index: int, list: list[Any]) -> bool:
    return 0 <= index < len(list)


def coor_in_list(coor: tuple[int, int], shape: tuple[int, int]) -> bool:
    max_x, max_y = shape
    x, y = coor

    return 0 <= x < max_x and 0 <= y < max_y

def index_to_coor(index: int, shape: tuple[int, int]) -> tuple[int, int]:
    width, _ = shape

    return (index % width, index // width)


def coor_to_index(coor: tuple[int, int], shape: tuple[int, int]) -> int:
    x, y = coor
    width, _ = shape

    return y * width + x
```

Peut être qu'il faut les déplacer dans un fichier `utils.py` ?

**UPDATE**: C'est fait. -->

<!-- * J'ai écris 2 fonctions pour pouvoir convertir un index vers des coordonnées et inversement mais je ne les utilise pas dans les méthodes `__make_[UP|RIGHT|DOWN|LEFT]`.

```python
# npuzzle.py
def index_to_coor(index: int, shape: tuple[int, int]) -> tuple[int, int]:
    width, _ = shape

    return (index % width, index // width)


def coor_to_index(coor: tuple[int, int], shape: tuple[int, int]) -> int:
    x, y = coor
    width, _ = shape

    return y * width + x

class Npuzzle:
    def __make_up(self) -> bool:
        src = self.empty_tile
        dst = src - self.n

        if not index_in_list(dst, self.tiles):
            return False

        self.tiles[src] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE
        return True

    def __make_right(self) -> bool:
        src_x = self.empty_tile % self.n                        # ici
        dst_x = src_x + 1                                       # ici
        dst_y = self.empty_tile // self.n                       # ici

        if not coor_in_list((dst_x, dst_y), (self.n, self.n)):
            return False

        dst = dst_y * self.n + dst_x                            # ici

        self.tiles[self.empty_tile] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE

        return True

    def __make_down(self) -> bool:
        src = self.empty_tile
        dst = src + self.n

        if not index_in_list(dst, self.tiles):
            return False

        self.tiles[src] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE
        return True

    def __make_left(self) -> bool:
        src_x = self.empty_tile % self.n                        # ici
        dst_x = src_x - 1                                       # ici
        dst_y = self.empty_tile // self.n                       # ici

        if not coor_in_list((dst_x, dst_y), (self.n, self.n)):
            return False

        dst = dst_y * self.n + dst_x                            # ici

        self.tiles[self.empty_tile] = self.tiles[dst]
        self.tiles[dst] = EMPTY_TILE

        return True
```

**NOTE**: je ne suis pas sûr qu'elles sont utiles pour `__make_up` et `__make_down`.

**UPDATE**: C'est fait. -->

* Tester `Npuzzle.from_file`. Il y a quelques tests dans `resources/puzzles/tests` mais je manque peut être des choses.

<!-- * Je suis un idiot: le `goal` n'est pas un array organisé genre : `[0, 1, 2, 3, 4, 5, 6, 7, 8]` (pour `n = 3`) mais un *escargot* (i.e `[1, 2, 3, 8, 0, 4, 7, 6, 5`). Du coup, `Npuzzle.goal` doit generer un array type *escargot*.

**UPDATE**: Je pense que ce n'est pas nécessaire de créer un algo pour ça. En temps normal, oui, mais dans mon cas (i.e. manque de temps), je ne pense pas que ça soit très pertinent. L'idée que j'ai atm c'est créer N fichier(s) pour décrire les N puzzle solution. Exemple:

```
# goal_3.txt
# Goal for 3x3
3
1 2 3
8 0 4
7 6 5
```

**UPDATE2**: `goal_3.txt`, `goal_4.txt`, `goal_5.txt`, `goal_6.txt` fait.

**UPDATE3**: si le `path` vers mes goals est changé, j'ai un crash. Peut être verifier quelque part que le `path` fait sens.

**UPDATE4**: J'ai créer l'algo finalement. C'est fait. -->

* Creer une methode pour verifier si une `Npuzzle` est solvable ou non

**UPDATE**: Je n'ai pas compris comment ça fonctionne

**UPDATE2**: C'est fait, **MAIS** besoin d'être testé !

**UPDATE3**: Ne fonctionne pas dans certains cas. En gros, ça marche pas.

**UPDATE4**: C'est *re*fait mais, **MAIS** besoin d'être *encore* testé.

<!-- * Dans `Npuzzle.from_random`, j'ai ajouté un flag `solvable`. Si il est vrai, alors le puzzle que je retourne **doit** être solvable et inversement.

**UPDATE**: C'est fait. -->

## solver.py

<!-- * Je ne suis pas sûr que l'implémentation des différents `Solver` doit être dans `solver.py`. Le *potentiel* problème c'est les `import` qui n'ont aucun sens pour tel ou tel `Solver`.

**UPDATE**: si jamais je le fait ça va casser des trucs dans `__main__.py`. Une solution peut être de quand même le faire, et de jetter un oeil au `plugin pattern`.

**UPDATE2**: Je close ça. Alors qu'il y a *pas mal* d'algo dans `solver.py`, je ne sens pas le besoin de ce point. -->

<!-- * `Solver.__node_in_open` est très, très lent. Le `any` prend une éternité...

**UPDATE**: J'ai ajouté un `Solver.__open_hash` pour supprimé le `any`. Les perfs pour le 3x3 sont turbo cool. *Cependant*, le 4*4 est pas ouf. Je pense que `A*` n'est pas adapté. -->

* Ajouter des algos

**UPDATE**: `BFS`, `DFS` fait.

**UPDATE2**: `IDA*` ajouter. Cependant il a pas l'air fou fou. TODO: voir pourquoi

**UPDATE3**: `Greedy Search` fait. Il fonctionne bien pour `3x3`, `4x4`, `5x5`.

**UPDATE4**: `Dijkstra` fait.

**UPDATE5**: `IDA*` refait. Il marche davantage

* J'ai un soucis avec `A*`, je pense qu'il faut suivre l'algo de l'école.

<!-- * Ajouter un `uniform cost search`

**UPDATE**: J'ai ajouté `Dijkstra`. En gros, c'est la même chose que `A*` sans `h(x)`. C'est fait. -->

<!-- * Attention, certains algo n'ont pas besoin d'heuristique (i.e `DFS` et `BFS` pour le moment). Il faut donc trouvé un moyen d'ignorer `args.heuristic` pour ces cas la.

**UPDATE**: C'est chiant à faire, mais il faut trouver. Peut être avoir une fonction qui vérifie si le `Solver` a un attribut `distance` et déduire que le `Solver` est `Informed` dans ce cas.

**UPDATE2**: La solution est la suivante:

```python
import inspect

def is_informed(solver: Type[Solver]) -> bool:
    return "distance" in inspect.signature(solver).parameters

```
Ce n'est peut être pas la goat solution mais je close ce todo. C'est fait. -->

<!-- * Euuuh, `A*` ne trouve pas le chemin opti avec `Manhattan`

**UPDATE**: En fait c'est normal, `Manhattan` n'est pas ultra adapté. Voir un point dans `distance.py`. C'est fait. -->

<!-- * `self.close` ne peut pas être une `list`. Il faut, *si j'ai bien compris* un objet qui implemente `__contain__` en **O(1)**. Genre un `set` ou un `dict` (ou peut être autre chose qui sait ?). Sachant que, *je pense* que l'objet stocké doit être hashable.

**UPDATE**: `self.close` est un `set` maintenant -->

<!-- * Je pense qu'il y a un soucis lorsque j'utilise `in self.open.queue` ou `in self.close`. Je pense que les pointeurs ne sont pas les mêmes ou quelque chose du genre. Du coup, même si le `Node` est présent dans l'une des listes, puisque *potentiellement* ce n'est pas le pointeur, il n'est pas considéré dedans ?

**UPDATE**: non -->

<!-- * Lorsque je log les `current_node.state.tiles` je vois qu'il y en a plusieurs identique...

**UPDATE**: fixed -->

<!-- * Je ne comprends pas A*

**UPDATE**: En fait si, je manquais quelque chose dans le sujet -->

<!-- * Je ne sais pas si c'est une bonne idée de generer les `successors` à l'intérieur de `Node`

**UPDATE**: je ne sais toujours pas mais ce n'était pas la cause du problème -->

## distance.py

<!-- * Même chose que pour `solver.py`. Est-ce que l'implémentation des différentes `Distance` doit être dans `distance.py` ? Sachant que, *je pense* que leurs implémentation vont être plus simple.

**UPDATE**: Même chose que pour `solver.py`. Si jamais je le fait ça va casser des trucs dans `__main__.py`. Une solution peut être de quand même le faire, et de jetter un oeil au `plugin pattern`.

**UPDATE2**: Même chose que pour `solver.py`. Je ne pense pas que ça soit necessaire. -->

* Ajouter des façons de calculer une distance. **Attention**, tu dois choisir des fonctions heuristiques dites "**admissible**" !

* Regarde `linear conflict`

**UPDATE**: ça me saoul, mais ça avance

## main.py

<!-- * Faire un *"smart flag"* qui donne la solution la plus rapide avec différentes configurations. Exemple: solver1 avec distance1, distance2, ..., distanceN, ..., solverN avec distance1, distance2, ..., distanceN.

**UPDATE**: Je pense que c'est une mauvaise idée/une idée redondante avec le flag `--kompare`. Je close. -->

<!-- * Afficher les informations demandé par le sujet !

**UPDATE**: J'ai créer une class `Report`, je ne sais pas si c'est la meilleur idée, mais en gros, j'ai envie de créer un decorateur pour compter le nombre de fois qu'une methode a était appelé pour donner un rapport final. Il y a *sans doute* mieux.

**UPDATE2**: L'ajout de `ReportManager` permet l'idée que j'avais, cependant je ne sais pas si c'est une bonne idée. *Pour le moment* ça fonctionne, mais attention.

**UPDATE3**: C'est fait. -->

<!-- * Faire un flag `--kompare` pour *comparer* les différents algo, les différents heuristiques, et peut être faire un graphique avec 
`matplotlib`

**UPDATE**: C'est fait. -->

<!-- * Ajouter 2 flags comme le script de l'école pour determiner si le puzzle generé est solvable ou non

**UPDATE**: C'est fait. -->

* Pour le flag `--kompare`, peut être ajouter une cfg pour comparer les des `solvers` (ou des `distances`) en particulier

**UPDATE**: Du coup, j'ai créer un flag `--config`. Il devrait être xor avec `--all`

**UPDATE2**: `--all` n'existe plus, il a été remplacé par `--report`, pour simplement print les différents `Report`.

**UPDATE3**: C'est fait, **MAIS** la logique derrière `--config` est assez particulière, c'est pas impossible qu'il y ai des soucis part endroits.

<!-- * Peut être avoir un flag qui *log* le puzzle

**UPDATE**: C'est fait. -->

## README.md

* Faire un truc stylé parce que les .md c'est cool

## report.py

<!-- * Peut être renommer `size_complexity` en `current_size_complexity` et `max_size_complexity` en `size_complexity`

**UPDATE**: C'est fait. -->
