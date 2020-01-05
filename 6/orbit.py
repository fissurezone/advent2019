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
        other_filler = '\n│   '
        other_lead = '├───'
        last_lead = '└───'
        last_filler = '\n    '

        if self.children:
            subtrees = []
            for idx, child in enumerate(self.children):
                lead = first_lead if idx == 0 else (last_lead if idx == len(self.children) - 1 else other_lead)
                filler = last_filler if idx == len(self.children) - 1 else other_filler
                subtrees.append(lead + child.__str__().replace('\n', filler))
            return '\n'.join(subtrees)
        return self.name


if __name__ == '__main__':
    com = Tree('COM')
    with open('input.txt') as f:
        tail = [orbit.strip().split(')') for orbit in f.readlines()]
    while tail:
        centre, body = tail.pop(0)
        if centre in com:
            com[centre].push(body)
        else:
            tail.append((centre, body))

    print(com)
