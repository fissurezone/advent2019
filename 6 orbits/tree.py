
class Tree(object):
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def push(self, name: str):
        self.children.append(Tree(name, self))

    def __contains__(self, name: str):
        if name == self.name:
            return True
        return any(child.__contains__(name) for child in self.children)

    def nodes(self):
        yield self
        for child in self.children:
            yield from child.nodes()

    def __getitem__(self, name):
        for node in self.nodes():
            if node.name == name:
                return node
        raise IndexError('node {} is out of bounds of tree {}'.format(name, self.name))

    def __str__(self):
        first_lead = self.name + '─'
        other_filler = '\n│' + ' ' * len(self.name)
        other_lead = '├' + '─' * len(self.name)
        last_lead = '└' + '─' * len(self.name)
        last_filler = '\n ' + ' ' * len(self.name)

        if self.children:
            subtrees = []
            for idx, child in enumerate(self.children):
                lead = first_lead if idx == 0 else (last_lead if idx == len(self.children) - 1 else other_lead)
                filler = last_filler if idx == len(self.children) - 1 else other_filler
                subtrees.append(lead + child.__str__().replace('\n', filler))
            return '\n'.join(subtrees)
        return self.name

    def count_orbiters_orbits(self, depth=0):
        if not self.children:
            return depth
        return depth + sum(child.count_orbiters_orbits(depth + 1) for child in self.children)

    def orbits(self):
        if not self.parent:
            return []
        return self.parent.orbits() + [self.parent.name]

if __name__ == '__main__':
    with open('input.txt') as f:
        tail = [orbit.strip().split(')') for orbit in f.readlines()]

    orbits_map = Tree('COM')
    while tail:
        centre, body = tail.pop(0)
        if centre in orbits_map:
            orbits_map[centre].push(body)
        else:
            tail.append((centre, body))
    print('part 1: {}'.format(orbits_map.count_orbiters_orbits()))

    your_orbits = orbits_map['YOU'].orbits()
    santas_orbits = orbits_map['SAN'].orbits()
    idx = 0
    while your_orbits[idx] == santas_orbits[idx]:
        idx += 1
    orbit_maneuvers = len(your_orbits[idx:]) + len(santas_orbits[idx:])
    print('part 2: {}'.format(orbit_maneuvers))
