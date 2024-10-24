Rule Engine with Abstract Syntax Tree (AST)
Objective
The aim of this project is to develop a 3-tier rule engine that determines user eligibility based on attributes like age, department, income, and experience. This engine will utilize Abstract Syntax Trees (AST) to dynamically represent, create, combine, and evaluate rules.
This document outlines the following:
1.	AST Data Structure: A flexible structure that represents logical and conditional expressions.
2.	API Design: Functions that build, combine, and evaluate rules in AST form.
3.	Database Design: Schema for storing rules and associated metadata.
Overview of the System
The system is designed to:
1.	Parse rule strings into an AST.
2.	Allow dynamic modification and combination of rules.
3.	Evaluate rules based on user input data.
4.	Store and retrieve rules in a structured database.
The sample rules used in this project are:
•	rule1: "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
•	rule2: "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
These rules will be represented as ASTs and evaluated against user data.
________________________________________
1. AST Data Structure
The Abstract Syntax Tree (AST) is a tree-based representation of logical and conditional expressions. Each node in the AST represents either:
•	An operator node (e.g., AND, OR) that connects other nodes.
•	An operand node (e.g., age > 30, salary > 50000) that represents the conditions.
Node Class
The following class structure defines the nodes in our AST:
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
Each node is defined by:
•	node_type: Identifies the type of node (either "operator" or "operand").
•	value: Holds the value of an operand (e.g., age > 30) or operator (e.g., AND/OR).
•	left and right: Reference to child nodes.
This tree-like structure makes it easier to traverse and evaluate the rules logically.
________________________________________
2. Parsing Rules into AST
To dynamically create rules, we need a function that can parse rule strings (e.g., age > 30 AND department = 'Sales') and convert them into an AST. The following function uses regular expressions to tokenize the rule and then constructs the AST accordingly.
Rule Parsing Function
import re
def parse_rule(rule_string):
    Parse a rule string and build the corresponding AST.
    :param rule_string: The rule string to be parsed (e.g., "(age > 30 AND department = 'Sales')").
    :return: ASTNode representing the root of the AST for the rule.
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
Explanation
1.	Logical Operators: The function replaces AND and OR with simplified tokens && and || to make parsing easier.
2.	Tokenization: The string is split into tokens representing operands (e.g., age > 30) and operators (AND, OR).
3.	AST Construction: Based on the operators, the function recursively builds an AST where each node contains either an operator or an operand.
________________________________________
3. Combining Multiple Rules
The rule engine allows the combination of multiple rules into a single, efficient AST. This can be useful when evaluating a series of conditions across different rules.
Combining Rules Function
def combine_rules(rules):
    Combine multiple rule ASTs into a single AST using OR/AND operations.
    :param rules: List of rule strings.
    :return: Combined AST.
    ast_nodes = [parse_rule(rule) for rule in rules]
    if len(ast_nodes) == 1:
        return ast_nodes[0]  # No need to combine if there's only one rule
    # Combine the rules with 'AND' for simplicity
    root = ast_nodes[0]
    for node in ast_nodes[1:]:
        root = ASTNode("operator", "AND", root, node)

    return root
Explanation
•	parse_rule: Each rule string is parsed into an AST using the parse_rule function.
•	Combination: The rules are combined using the AND operator, but this can be extended to support more complex combination strategies (such as using a most-frequent operator heuristic).
________________________________________
4. Evaluating Rules
The rule engine evaluates the rules (represented by the AST) against user data. The evaluation traverses the AST and checks whether the conditions in the nodes are satisfied by the data.
Rule Evaluation Function
def evaluate_rule(ast_node, user_data):
    Evaluate an AST against user data.
    :param ast_node: The root of the AST representing the rule.
    :param user_data: Dictionary of user attributes (e.g., {"age": 35, "department": "Sales"}).
    :return: True if the rule is satisfied, False otherwise.
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
Explanation
1.	Operand Nodes: For operand nodes, the field (e.g., age, department) is extracted, and its value in user_data is compared against the rule condition.
2.	Operator Nodes: For operator nodes, the function recursively evaluates the left and right child nodes based on the operator (AND/OR).
________________________________________
5. Test Cases
The following tests ensure the rule engine behaves as expected:
# Create rules
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"
# Parse the rules into ASTs
ast1 = parse_rule(rule1)
ast2 = parse_rule(rule2)
# Combine rules
combined_ast = combine_rules([rule1, rule2])
# Test evaluation
user_data1 = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
user_data2 = {"age": 22, "department": "Marketing", "salary": 45000, "experience": 4}

print(f"Evaluation for user_data1: {evaluate_rule(combined_ast, user_data1)}")  # Should be True
print(f"Evaluation for user_data2: {evaluate_rule(combined_ast, user_data2)}")  # Should be False
________________________________________
6. Database Design for Rule Storage
For rule persistence, we can store the rule strings and their corresponding ASTs in a SQL or NoSQL database. Below is a sample SQL schema for this purpose:
CREATE TABLE rules (
    id INT PRIMARY KEY,
    rule_string TEXT NOT NULL,
    ast_json TEXT NOT NULL,  -- JSON representation of the AST
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Explanation
•	rule_string: Stores the original rule in string format.
•	ast_json: The AST can be serialized to JSON format and stored in this column.
•	created_at: A timestamp indicating when the rule was created.
namic rules.
