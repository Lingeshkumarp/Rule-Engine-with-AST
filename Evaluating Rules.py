def evaluate_rule(ast_node, user_data):
    """
    Evaluate an AST against user data.
    :param ast_node: The root of the AST representing the rule.
    :param user_data: Dictionary of user attributes (e.g., {"age": 35, "department": "Sales"}).
    :return: True if the rule is satisfied, False otherwise.
    """
    if ast_node.node_type == "operand":
        field, op, value = re.split(r'([<>=]+)', ast_node.value.strip())
        field_value = user_data.get(field.strip())

        # Convert value to the appropriate type (int or string)
        if value.isdigit():
            value = int(value)
        else:
            value = value.strip("'\"")

        if op == ">":
            return field_value > value
        elif op == "<":
            return field_value < value
        elif op == "==":
            return field_value == value
        else:
            raise ValueError(f"Unknown operator: {op}")

    elif ast_node.node_type == "operator":
        if ast_node.value == "AND":
            return evaluate_rule(ast_node.left, user_data) and evaluate_rule(ast_node.right, user_data)
        elif ast_node.value == "OR":
            return evaluate_rule(ast_node.left, user_data) or evaluate_rule(ast_node.right, user_data)

    return False
