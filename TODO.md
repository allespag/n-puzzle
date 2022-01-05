# n-puzzle

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

* Je suis un idiot: le `goal` n'est pas un array organisé genre : `[0, 1, 2, 3, 4, 5, 6, 7, 8]` (pour `n = 3`) mais un *escargot* (i.e `[1, 2, 3, 8, 0, 4, 7, 6, 5`). Du coup, `Npuzzle.goal` doit generer un array type *escargot*.

* Creer une methode pour verifier si une `Npuzzle` est solvable ou non

**UPDATE**: Je n'ai pas compris comme ça fonctionne

## solver.py

* Je ne suis pas sûr que l'implémentation des différents `Solver` doit être dans `solver.py`. Le *potentiel* problème c'est les `import` qui n'ont aucun sens pour tel ou tel `Solver`.

**UPDATE**: si jamais je le fait ça va casser des trucs dans `__main__.py`. Une solution peut être de quand même le faire, et de jetter un oeil au `plugin pattern`.

* `self.close` ne peut pas être une `list`. Il faut, *si j'ai bien compris* un objet qui implemente `__contain__` en **O(1)**. Genre un `set` ou un `dict` (ou peut être autre chose qui sait ?). Sachant que, *je pense* que l'objet stocké doit être hashable.

<!-- * Je pense qu'il y a un soucis lorsque j'utilise `in self.open.queue` ou `in self.close`. Je pense que les pointeurs ne sont pas les mêmes ou quelque chose du genre. Du coup, même si le `Node` est présent dans l'une des listes, puisque *potentiellement* ce n'est pas le pointeur, il n'est pas considéré dedans ?

**UPDATE**: non -->

<!-- * Lorsque je log les `current_node.state.tiles` je vois qu'il y en a plusieurs identique...

**UPDATE**: fixed -->

<!-- * Je ne comprends pas A*

**UPDATE**: En fait si, je manquais quelque chose dans le sujet -->

<!-- * Je ne sais pas si c'est une bonne idée de generer les `successors` à l'intérieur de `Node`

**UPDATE**: je ne sais toujours pas mais ce n'était pas la cause du problème -->

## distance.py

* Même chose que pour `solver.py`. Est-ce que l'implémentation des différentes `Distance` doit être dans `distance.py` ? Sachant que, *je pense* que leurs implémentation vont être plus simple.

**UPDATE**: Même chose que pour `solver.py`. Si jamais je le fait ça va casser des trucs dans `__main__.py`. Une solution peut être de quand même le faire, et de jetter un oeil au `plugin pattern`.
