grammar SignalTemporalLogic;


evl	:	statementList;


statementList
	:	NEWLINE* statement+
	;

statement
	:	declaration NEWLINE+
	|	boolExpr NEWLINE+
	;

declaration
	:	CONST DOUBLE ID ('=' (INTEGER | FLOAT))? SEMICOLON
	|	CONST INT ID ('=' INTEGER)? SEMICOLON
	|	CONST BOOL ID ('=' (TRUE | FALSE))? SEMICOLON
	;



// $<Boolean Expressions
boolExpr
    :   stlTerm (OR stlTerm)*
    |   stlTerm (AND stlTerm)*
    |   stlTerm (IMPLIES stlTerm)*
    ;


stlTerm	:	booelanAtomic (U timeBound booelanAtomic)?
		|	F timeBound booelanAtomic
		|	G timeBound booelanAtomic
		;
// $>



// $<Temporal Operators
timeBound
	:	'<=' atomic
	|	LBRAT atomic COMMA atomic RBRAT
	|	atomic
	;
// $>




booelanAtomic
	:	NOT?
		(	relationalExpr
		|	LPAR boolExpr RPAR
		|	TRUE
		|	FALSE
		)
	;



relationalExpr
	:	atomic (EQ | NEQ | GT | LT | GE | LE) atomic
	;


atomic
	:	(INTEGER | FLOAT)
	|	ID;

// $>


CONST   :       'const';
INT  	:       'int';
DOUBLE  :       'double';
BOOL  	:       'bool';
COMMA   :       ',';
SEMICOLON  :    ';';
LPAR    :       '(';
RPAR    :       ')';

LBRAT   :       '[';
RBRAT   :       ']';
U       :	'U';
F       :	'F';
G       :	'G';

TRUE	:	'true';
FALSE	:	'false';

AND	:	'&';
OR	:	'|';
IMPLIES: '->';
NOT	:	'!';

EQ	:	'=';
NEQ	:	'!=';
GT	:	'>';
GE	:	'>=';
LT	:	'<';
LE	:	'<=';



// $<Terminal

INTEGER	:	'-'? '0'..'9'+
	;

FLOAT
	:   ('0'..'9')+ '.' ('0'..'9')* EXPONENT?
	|   '.' ('0'..'9')+ EXPONENT?
	|   ('0'..'9')+ EXPONENT
	;

fragment
EXPONENT : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;



ID	:	('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
	;

NEWLINE	:	( '\r'| '\n' )
	;

// $>




// $<White space

COMMENT
    :   '//' ~('\n'|'\r')* -> channel(HIDDEN)
    ;

/* Ignore white space characters, except from newline */
WS
    :   (' ' | '\t' | NEWLINE ) -> channel(HIDDEN)
    ;
// $>