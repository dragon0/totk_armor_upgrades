from typing import Optional
from dataclasses import dataclass, field


@dataclass
class UpgradeItem:
    item: str
    quantity: int


UpgradeTierRequirement = list[UpgradeItem]


@dataclass
class ArmorPiece:
    name: str
    level: int


@dataclass
class ArmorPieceUpgrade:
    piece: ArmorPiece
    required_for_upgrade: Optional[UpgradeTierRequirement]


@dataclass
class ArmorSet:
    name: str
    pieces: list[ArmorPiece]
    upgrade_tiers: list[UpgradeTierRequirement]

    def upgrade_requirements(self) -> list[ArmorPieceUpgrade]:
        requirements = []
        for piece in self.pieces:
            upgrade_requirement = (self.upgrade_tiers[piece.level]
                                   if piece.level < len(self.upgrade_tiers)
                                   else None)
            upgrade = ArmorPieceUpgrade(
                piece=piece,
                required_for_upgrade=upgrade_requirement)
            requirements.append(upgrade)
        return requirements


@dataclass
class UpgradeMaterial:
    name: str
    quantity: int
    armor_pieces: list[ArmorPiece] = field(default_factory=list)
    armor_sets: set[ArmorPiece] = field(default_factory=set)
