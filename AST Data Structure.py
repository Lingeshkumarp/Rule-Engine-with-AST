class ASTNode:
    def __init__(self, node_type, value=None, left=None, right=None):
        """
        Initialize an AST Node.
        :param node_type: Type of node - 'operator' (AND/OR) or 'operand' (condition).
        :param value: Value for operand nodes (e.g., "age > 30").
        :param left: Left child node for operator nodes.
        :param right: Right child node for operator nodes.
        """
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"ASTNode(type={self.node_type}, value={self.value})"
