from dataclasses import dataclass, field
from datetime import date
from typing import Self

from dataclasses_json import DataClassJsonMixin, config, dataclass_json

from utils import get_current_semester, get_mid


@dataclass
class Base(DataClassJsonMixin):
    @classmethod
    def load_from_file(cls, file: str) -> Self:
        return cls.from_path(file)

    @classmethod
    def from_path(cls, file: str) -> Self:
        from json import load

        with open(file, encoding="utf-8") as f:
            return cls.from_dict(load(f))

    def save(self, file: str):
        from json import dump

        with open(file, "w", encoding="utf-8") as f:
            dump(self.to_dict(), f, ensure_ascii=False, indent=2)


@dataclass_json
@dataclass
class Config(Base):
    semester: int = -1

    @classmethod
    def load(cls, file: str) -> Self:
        from pathlib import Path

        return cls.load_from_file(file) if Path(file).exists() else cls()

    def get_semester(self) -> int:
        return self.semester if self.semester in {1, 2} else get_current_semester()


@dataclass_json
@dataclass
class Grade(Base):
    grade: int
    date: "date" = field(
        default_factory=date.today,
        metadata=config(decoder=date.fromisoformat, encoder=date.isoformat),
    )
    semester: int = field(default_factory=get_current_semester)


@dataclass_json
@dataclass
class Subject(Base):
    name: str
    grades: list[Grade]

    def avg_by_semester(self, semester: int) -> float:
        return get_mid([g.grade for g in self.grades if g.semester == semester])

    def avg_year(self) -> float:
        return get_mid(
            [
                self.avg_by_semester(1),
                self.avg_by_semester(2),
            ]
        )


@dataclass_json
@dataclass
class Data(Base):
    subjects: list[Subject]
