__all__ = ["Version"]

class Version:
    def __init__(self, major:int, minor:int=0, patch:int=0):
        if major < 0:
            raise ValueError(f"Invalid major version number: {major}")
        elif minor < 0:
            raise ValueError(f"Invalid minor version number: {minor}")
        elif patch < 0:
            raise ValueError(f"Invalid patch version number: {patch}")

        self.numbers = (major, minor, patch)

    @property
    def major(self) -> int:
        return self.numbers[0]

    @property
    def minor(self) -> int:
        return self.numbers[1]

    @property
    def patch(self) -> int:
        return self.numbers[2]

    def __eq__(self, other):
        try:
            return (self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch)
        except AttributeError:
            return NotImplemented

    def __lt__(self, other: "Version"):
        if self.major < other.major:
            return True
        elif other.major < self.major:
            return False
        elif self.minor < other.minor:
            return True
        elif other.minor < self.minor:
            return False
        elif self.patch < other.patch:
            return True
        elif other.patch < self.patch:
            return False
        else:
            return False

    def __ge__(self, other: "Version"):
        return not (self < other)

    def __le__(self, other: "Version"):
        return not (self > other)

    def __hash__(self):
        return hash(self.numbers)

    def __repr__(self):
        args = ", ".join(str(num) for num in self.numbers)
        return f"{self.__class__.__name__}({args})"

    def __str__(self):
        return ".".join((str(num) for num in self.numbers))

    @classmethod
    def parse(cls, version: str):
        strings = version.split(".")

        try:
            return cls(*(int(num) for num in strings))
        except (TypeError, ValueError) as err:
            errmsg = f"\"{version}\" is not a valid version identifier"
            raise ValueError(errmsg) from err
