class FireState:
    def __init__(self, tree):
        self.tree = tree
        self.burned_nodes = set()  
        self.burning_nodes = set()
        self.protected_nodes = set()
    
    def set_burned_nodes(self, burned_nodes):
        self.burned_nodes = burned_nodes

    def set_burning_nodes(self, burning_nodes):
        self.burning_nodes = burning_nodes
