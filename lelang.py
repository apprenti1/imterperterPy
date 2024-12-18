# -*- coding: utf-8 -*-
 
import ply.lex as lex
import ply.yacc as yacc
from genereTreeGraphviz2 import printTreeGraph
 
 
#https://pastebin.com/LCHRmVKm
 
reserved={
        'print':'PRINT'
 
        }zzzzzsss
 
tokens = [ 'NUMBER','MINUS', 'PLUS','TIMES','DIVIDE', 'LPAREN',
          'RPAREN', 'OR', 'AND', 'SEMI', 'EGAL', 'NAME', 'INF', 'SUP',
          'EGALEGAL','INFEG','INCREMENT']+ list(reserved.values())
 
t_PLUS = r'\+' 
t_MINUS = r'-' 
t_TIMES = r'\*' 
t_DIVIDE = r'/'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\+\+'
t_LPAREN = r'\(' 
t_RPAREN = r'\)' 
t_OR = r'\|'
t_AND = r'\&'
t_SEMI = r';'
t_EGAL = r'\='
#t_NAME = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_INF = r'\<'
t_SUP = r'>'
t_INFEG = r'\<\='
t_EGALEGAL = r'\=\='
 
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t
 
 
def t_NUMBER(t): 
    r'\d+' 
    t.value = int(t.value) 
    return t
 
t_ignore = " \t"
 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
lex.lex()
 
names={}
precedence = ( 
        ('left','OR' ), 
        ('left','AND'), 
        ('nonassoc', 'INF', 'INFEG', 'EGALEGAL', 'SUP'), 
        ('left','PLUS', 'MINUS' ), 
        ('left','TIMES', 'DIVIDE'), 
        )
def evalinst(t):
    print('evalInst', t)
    if t == 'empty' : return 
    if t[0] == 'assign' : names[t[1]]=evalExpr(t[2])
    if t[0] == 'increment':
        if t[1] in names:
            names[t[1]] += 1
        else:
            print(f"Error: variable '{t[1]}' is not defined.")
    if t[0] == 'print' : print('CALC>' , evalExpr(t[1]))
    if t[0] == 'bloc' :  
        evalinst(t[1])
        evalinst(t[2])
 
def evalExpr(t) : 
    print('evalExpr', t)
    if type(t) is int or type(t) is float : return t
    if type(t) is str : return names[t]
    if t[0]=='+' : return evalExpr(t[1])+evalExpr(t[2])
    if t[0]=='-' : return evalExpr(t[1])-evalExpr(t[2])
    if t[0]=='*' : return evalExpr(t[1])*evalExpr(t[2])
    if t[0]=='/' : return evalExpr(t[1])/evalExpr(t[2])
 
 
def p_start(p):
    'start : bloc'
    print(p[1])
    printTreeGraph(p[1])
    evalinst(p[1])
 
def p_bloc(p):
    '''bloc : bloc statement SEMI
    | statement SEMI'''
    if len(p) ==4 :
        p[0] = ('bloc', p[1], p[2])
    else :
        p[0] = ('bloc', p[1], 'empty')
 
 
def p_statement_expr(p): 
    'statement : PRINT LPAREN expression RPAREN' 
    #print(p[3]) 
    p[0] = ('print', p[3])
 
 
def p_statement_assign(p):
    'statement : NAME EGAL expression'
    #names[p[1]]=p[3] 
    p[0] = ('assign', p[1], p[3])
 
def p_statement_increment(p):
    '''statement : NAME INCREMENT'''
    p[0] = ('increment', p[1])

def p_expression_binop_inf(p): 
    '''expression : expression INF expression
    | expression INFEG expression
    | expression EGALEGAL expression
    | expression AND expression
    | expression OR expression
    | expression PLUS expression
    | expression TIMES expression
    | expression MINUS expression
    | expression DIVIDE expression
    | expression SUP expression''' 
    p[0] = (p[2],p[1],p[3])
 
 
def p_expression_group(p): 
    'expression : LPAREN expression RPAREN' 
    p[0] = p[2] 
 
def p_expression_number(p): 
    'expression : NUMBER' 
    p[0] = p[1] 
 
def p_expression_name(p): 
    'expression : NAME' 
    p[0] =  p[1]
 
def p_error(p):    print("Syntax error in input!")
 
yacc.yacc()
s = 'x=4; x++; print(x);'
yacc.parse(s)
 