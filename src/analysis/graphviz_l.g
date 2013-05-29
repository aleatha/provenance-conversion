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
	k=3;
	exportVocab=graphViz;
	charVocabulary = '\3'..'\377';
}

tokens {
	"digraph";
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


NUM_LITERAL:
  ('0'..'9')+('.'('0'..'9'))?;

STRING_LITERAL 
	: ('a'..'z'|'A'..'Z')('a'..'z'|'A'..'Z'|'_'|'0'..'9')*
	|	'"'(ESC|~'"')*'"'
  ;