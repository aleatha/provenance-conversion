// This file is part of PyANTLR. See LICENSE.txt for license
// details..........Copyright (C) Wolfgang Haefelinger, 2004.
//
// $Id$

/*
 * Make sure to run antlr.Tool on the lexer.g file first!
 */
 
header {
import prov_stats

pnodestore = prov_stats.PNodeStore()
}

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

	for pnode in pnodestore.pnodes.keys():
      print pnode
      for edge in pnodestore.pnodes[pnode].outedges:
      	print "  "+edge
      	
  analyzer = prov_stats.PGraphAnalyzer(pnodestore)
  
  analyzer.calcDegree()
  analyzer.calcHeights()
  analyzer.TaPiR()

}

options {
	mangleLiteralPrefix = "TK_";
  language=Python;
}


class graphviz_p extends Parser;
options {
	importVocab=graphViz;
	buildAST = true;
	k = 2;
}


diagram
  : TK_digraph! optionname! LCURLY (statement SEMICOLON)* RCURLY EOF
  ;
  
statement
    : 
      {fro = self.LT(1).getText()} 
      STRING_LITERAL EDGE 
      {
      to = self.LT(1).getText()
      pnodestore.insertEdge(fro,to)
      } 
      STRING_LITERAL (optionclause!)?
    | STRING_LITERAL! EQUALS! optionval!
    | {"ID" in self.LT(1).getText()}? STRING_LITERAL optionclause!
    |  STRING_LITERAL! optionclause!
    ;

//  setedge
//	: EDGE STRING_LITERAL (optionclause)?
//	;
	
optionclause
  : LSQUARE optionlist RSQUARE
  ;
  
optionlist
  : STRING_LITERAL setvariable (COMMA STRING_LITERAL setvariable)*
  ;

setvariable
  : EQUALS optionval
  | optionclause!
  ;
  
optionname
 	: STRING_LITERAL
 	;
 	
optionval
	: STRING_LITERAL
	| NUM_LITERAL
	;