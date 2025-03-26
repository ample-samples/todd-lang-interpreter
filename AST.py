from abc import ABC, abstractmethod
from enum import Enum
from types import NotImplementedType

class NodeType(Enum):
    Program = "Program"

    ExpressionStatement = "ExpressionStatement"

    InfixExpression = "InfixExpression"

    IntegerLiteral = "IntegerLiteral"
    FloatLiteral = "FloatLiteral"


class Node(ABC):
    @abstractmethod
    def type(self) -> NodeType:
        pass

    @abstractmethod
    def json(self) -> dict:
        pass


class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    def __init__(self) -> None:
        self.statements: list[Statement] = []

    def type(self) -> NodeType:
        return NodeType.Program

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [{stmt.type().value: stmt.json()} for stmt in self.statements]
        }

class ExpressionStatement(Statement):
    def __init__(self, expr: Expression = None) -> None: # pyright: ignore[reportArgumentType]
        self.expr: Expression = expr

    def type(self) -> NodeType:
        return NodeType.ExpressionStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "expr": self.expr.json()
        }

class InfixEpression(Expression):
    def __init__(self, left_node: Expression, operator: str, right_node: Expression = None) -> None: # pyright: ignore[reportArgumentType]
        self.left_node: Expression = left_node
        self.operator: str = operator
        self.right_node: Expression = right_node

    def type(self) -> NodeType:
        return NodeType.InfixExpression
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "left_node": self.left_node.json(),
            "operator": self.operator,
            "right_node": self.right_node.json(),
        }

class IntegerLiteral(Expression):
    def __init__(self, value: int = None) -> None: # pyright: ignore[reportArgumentType]
        self.value: int = value

    def type(self) -> NodeType:
        return NodeType.IntegerLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }


class FloatLiteral(Expression):
    def __init__(self, value: float = None) -> None: # pyright: ignore[reportArgumentType]
        self.value: float = value

    def type(self) -> NodeType:
        return NodeType.FloatLiteral

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "value": self.value
        }

