class Key:
    def __init__(self, ab: int, g: int, p: int):
        self.ab = ab
        self.g = g
        self.p = p
        self.AB = round(g ** ab % p)

    @property
    def public_key(self) -> list:
        return [self.g, self.p, self.AB]

    @property
    def private_key(self) -> list:
        return [self.ab]
