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

    def print_info(self):
        """
        Muestra el estado del fuego
        """
        print(f"Burned Nodes: {self.burned_nodes}")
        print(f"Burning Nodes: {self.burning_nodes}")
        print(f"Protected Nodes: {self.protected_nodes}")
