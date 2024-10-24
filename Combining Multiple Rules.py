def combine_rules(rules):
    """
    Combine multiple rule ASTs into a single AST using OR/AND operations.
    :param rules: List of rule strings.
    :return: Combined AST.
    """
    ast_nodes = [parse_rule(rule) for rule in rules]
    if len(ast_nodes) == 1:
        return ast_nodes[0]  # No need to combine if there's only one rule

    # Combine the rules with 'AND' for simplicity
    root = ast_nodes[0]
    for node in ast_nodes[1:]:
        root = ASTNode("operator", "AND", root, node)

    return root
