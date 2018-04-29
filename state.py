import typing as T
from pysistence import make_dict

class ImmState():

    def __init__(self, settings, game) -> None:
        if type(settings) is dict:
            settings = make_dict(settings)

        if type(game) is dict:
            game = make_dict(game)

        self.settings = settings
        self.game = game

    def using(self, key: str, value: T.Any, player: str = None) -> 'ImmState':
        if player == 'game' or player is None:
            return ImmState(self.settings, self.game.using(**{key: value}))

        if key not in self.game:
            key_dict = make_dict({})
        else:
            key_dict = self.game[key]

        return ImmState(self.settings, self.game.using(**{
            key: key_dict.using(**{player: value})
        }))

    def __str__(self):
        return str(self.dict())

    def __iter__(self):
        return self.dict().__iter__()

    def dict(self):
        return {
            'settings': dict(self.settings.items()),
            'game': dict(self.game.items())
        }

    def __call__(self, key, value):
        return ImmState(self.settings, self.game.using(**{key: value}))


class State():

    def __init__(self) -> None:
        self.settings : T.Dict[str, T.Any] = {}
        self.game : T.Dict[str, T.Any] = {}

    def update(self, player: str, key: str, value: T.Any) -> None:
        if player == 'game':
            self.game[key] = value
            return

        if key not in self.game:
            self.game[key] = {}

        self.game[key][player] = value

    def setting(self, key: str, value: T.Any) -> None:
        self.settings[key] = value

    def handle_cmd(self, cmd: str, payload: T.Sequence[T.Any]) -> None:
        if cmd == 'update':
            self.update(*payload)
        elif cmd == 'setting':
            self.setting(*payload)

    def immutable(self) -> ImmState:
        return ImmState(self.settings, self.game)
