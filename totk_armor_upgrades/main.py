from typing import Optional
import json
import csv

from .models import *


def main():
    from pprint import pprint
    armor_sets = load_armor_sets('armor-sets.json')
    # TODO Split armor-sets.json into sets.json and upgrades.json
    # sets.json will include user-specific info on the user's upgrade levels
    # upgrades.json will include the full upgrade requirements

    itemwise_material_list: dict[str, UpgradeMaterial] = {}
    for set in armor_sets:
        upgrades = set.upgrade_requirements()
        for upgrade in upgrades:
            if upgrade.required_for_upgrade:
                for item in upgrade.required_for_upgrade:
                    if item.item not in itemwise_material_list:
                        itemwise_material_list[item.item] = UpgradeMaterial(
                            name=item.item, quantity=0)
                    entry = itemwise_material_list[item.item]
                    entry.quantity += item.quantity
                    entry.armor_pieces.append(upgrade.piece)
                    entry.armor_sets.add(set.name)

    print("Materials Needed")
    for material in sorted(itemwise_material_list.values(), key=lambda mat: mat.name):
        # print(f'{material.quantity:>5} {material.name:<25} for {", ".join(map(lambda piece: piece.name, material.armor_pieces))}')
        print(
            f'{material.quantity:>5} {material.name:<25} for {", ".join(sorted(material.armor_sets))}')

    print()
    print("Materials per Armor Set")
    for set in armor_sets:
        upgrades = set.upgrade_requirements()
        setwise_material_list = condensed_requirements(upgrades)
        if setwise_material_list:
            lines = []
            for material in sorted(setwise_material_list.values(), key=lambda mat: mat.name):
                lines.append(f'{material.quantity} {material.name}')
            print(f'{set.name:<15}: {", ".join(lines)}')

    with open('materials.csv', 'w',  newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Quantity', 'Name', 'Armor Pieces'])
        for material in sorted(itemwise_material_list.values(), key=lambda mat: mat.name):
            writer.writerow([material.quantity, material.name, ", ".join(
                map(lambda piece: piece.name, material.armor_pieces))])


MaterialName = str


def condensed_requirements(upgrades: list[ArmorPieceUpgrade]) -> dict[MaterialName, UpgradeMaterial]:
    material_list: dict[MaterialName, UpgradeMaterial] = {}
    for upgrade in upgrades:
        if upgrade.required_for_upgrade:
            for item in upgrade.required_for_upgrade:
                if item.item not in material_list:
                    material_list[item.item] = UpgradeMaterial(
                        name=item.item, quantity=0)
                entry = material_list[item.item]
                entry.quantity += item.quantity
                entry.armor_pieces.append(upgrade.piece)
    return material_list


def load_armor_sets(filename: str) -> Optional[list[ArmorSet]]:
    with open(filename) as f:
        raw = json.load(f)
        if 'Armor Sets' in raw:
            armor_sets = []
            for k, v in raw['Armor Sets'].items():
                raw_upgrades = v.get('upgrades')
                upgrades = list(map(
                    lambda level: list(
                        map(lambda item: UpgradeItem(**item), level)),
                    raw_upgrades))

                raw_pieces = v.get('pieces')
                pieces = list(
                    map(lambda piece: ArmorPiece(**piece), raw_pieces))

                armor_sets.append(
                    ArmorSet(name=k, pieces=pieces, upgrade_tiers=upgrades))

            return armor_sets


if __name__ == '__main__':
    main()
