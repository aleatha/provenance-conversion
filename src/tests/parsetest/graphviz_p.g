// This file is part of PyANTLR. See LICENSE.txt for license
// details..........Copyright (C) Wolfgang Haefelinger, 2004.
//
// $Id$

/*
 * Make sure to run antlr.Tool on the lexer.g file first!
 */

header "graphviz_p.__main__" {
   import graphviz_l
   import graphviz_p
   
   L = graphviz_l.Lexer() 
   P = graphviz_p.Parser(L)
   P.setFilename(L.getFilename())

   ### Parse the input expression
   try:
      P.diagram()
   except antlr.ANTLRException, ex:
      print ex
      print "*** error(s) while parsing."
      print ">>> exit(1)"
      import sys
      sys.exit(1)
   
   ast = P.getAST()
   
   if not ast:
      print "stop - no AST generated."
      sys.exit(0)  
      
   ###show tree
   print "Tree: " + ast.toStringTree()
   print "List: " + ast.toStringList()
   print "Node: " + ast.toString()
   print "visit>>"
   visitor = Visitor()
   visitor.visit(ast);
   print "visit<<"
}

options {
	mangleLiteralPrefix = "TK_";
    language=Python;
}


class graphviz_p extends Parser;
options {
	importVocab=graphViz;
	buildAST = true;
}


diagram
  : GRAPHTYPE optionstring LCURLY (statement)* RCURLY EOF
  ;
  
statement
  : setvariable SEMICOLON
  | defnode SEMICOLON
  | setdefaults SEMICOLON
  | defedge SEMICOLON
  ;
  
setvariable
  : optionstring EQUALS optionstring
  ;
  
optionclause
  : LSQUARE optionlist RSQUARE
  ;
  
optionlist
  : setvariable COMMA optionlist
  | setvariable
  ;

defnode
  : NODENAME (optionclause)?
  ;
  
setdefaults
  : optionstring (optionclause)?
  ;


defedge
  : NODENAME EDGE NODENAME (optionclause)?
  ;
  
 optionstring
 	: STRING_LITERAL
 	| BARESTRING
 	;