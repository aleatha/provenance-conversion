// This file is part of PyANTLR. See LICENSE.txt for license
// details..........Copyright (C) Wolfgang Haefelinger, 2004.
//
// $Id$

/*
 * Make sure to run antlr.Tool on the lexer.g file first!
 */
options {
	mangleLiteralPrefix = "TK_";
    language=Python;
}

class graphviz_l extends Lexer;
options {
	k=2;
	exportVocab=graphViz;
	charVocabulary = '\3'..'\377';
}

WS	:	(' '
	|	'\t'
	|	'\n'	{ $newline;}
	|	'\r')
		{ _ttype = SKIP; }
	;


LCURLY:	'{'
	;

RCURLY:	'}'
	;
	
LSQUARE: '['
  ;
  
RSQUARE: ']'
  ;
  
EDGE: "->"
  ;
  
COMMA: ','
  ;  
  
EQUALS: '='
  ;  
  
SEMICOLON: ';'
  ;  


GRAPHTYPE: "digraph"
  ;


CHAR_LITERAL
	:	'\'' (ESC|~'\'') '\''
	;

STRING_LITERAL
	:	'"' (ESC|~'"')* '"'
	;


protected
ESC	:	'\\'
		(	'n'
		|	'r'
		|	't'
		|	'b'
		|	'f'
		|	'"'
		|	'\''
		|	'\\'
		|	'0'..'3'
			(
				options {
					warnWhenFollowAmbig = false;
				}
			:	'0'..'9'
				(
					options {
						warnWhenFollowAmbig = false;
					}
				:	'0'..'9'
				)?
			)?
		|	'4'..'7'
			(
				options {
					warnWhenFollowAmbig = false;
				}
			:	'0'..'9'
			)?
		)
	;

NODENAME: "PID"('0'..'9')+'_'('0'..'9')+'.'('0'..'9')+
  ;

BARESTRING : ('a'..'z'|'A'..'Z'|'_'|'0'..'9') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')*
  ;