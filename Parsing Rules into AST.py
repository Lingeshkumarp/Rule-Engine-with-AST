import re

def parse_rule(rule_string):
    """
    Parse a rule string and build the corresponding AST.
    :param rule_string: The rule string to be parsed (e.g., "(age > 30 AND department = 'Sales')").
    :return: ASTNode representing the root of the AST for the rule.
    """
    # Convert logical operators for easy handling
    rule_string = rule_string.replace("AND", "&&").replace("OR", "||")

    # Define patterns for operands and operators
    operand_pattern = re.compile(r'([a-zA-Z_]+) *([<>=]+) *([a-zA-Z0-9\'"]+)')
    operator_pattern = re.compile(r'&&|\|\|')

    tokens = operand_pattern.split(rule_string)
    operators = operator_pattern.findall(rule_string)

    # Build the AST from tokens and operators
    def build_ast(tokens, operators):
        if not tokens:
            return None
        left_operand = tokens.pop(0).strip()
        operator = operators.pop(0).strip() if operators else None
        right_operand = tokens.pop(0).strip() if tokens else None

        left_node = ASTNode("operand", left_operand)
        if right_operand:
            right_node = ASTNode("operand", right_operand)
            if operator == "&&":
                return ASTNode("operator", "AND", left_node, right_node)
            elif operator == "||":
                return ASTNode("operator", "OR", left_node, right_node)

        return left_node

    return build_ast(tokens, operators)
