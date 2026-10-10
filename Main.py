from antlr4 import *
from LenguajeLexer import LenguajeLexer
from LenguajeParser import LenguajeParser
from EvalVisitor import EvalVisitor

entrada = FileStream("Ejercicio5.txt", encoding="utf-8")
parser = LenguajeParser(CommonTokenStream(LenguajeLexer(entrada)))
EvalVisitor().visit(parser.root())