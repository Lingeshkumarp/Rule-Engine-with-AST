CREATE TABLE rules (
    id INT PRIMARY KEY,
    rule_string TEXT NOT NULL,
    ast_json TEXT NOT NULL,  -- JSON representation of the AST
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
