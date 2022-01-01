# n-puzzle

## npuzzle.py

* Trouver une façon de vérifier l'égalité entre 2 Npuzzle. Une idée naive :

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

## solver.py

* Je ne suis pas sûr que l'implémentation des différents `Solver` doit être dans `solver.py`. Le *potentiel* problème c'est les `import` qui n'ont aucun sens pour tel ou tel `Solver`.

## distance.py

* Même chose que pour `solver.py`. Est-ce que l'implémentation des différentes `Distance` doit être dans `distance.py` ? Sachant que, *je pense* que leurs implémentation vont être plus simple.
