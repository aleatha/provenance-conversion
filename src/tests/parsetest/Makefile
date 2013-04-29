# navigation 
antlr_home        = /Users/aleatha/Firefox_Downloads/antlr-2.7.7


g_FILES  = \
 graphviz_l.g \
 graphviz_p.g \
 $(eol)

g_py_FILES = \
 graphviz_l.py graphviz_p.py \
 $(eol)



compile :
	/bin/rm -r -f graphviz_l.py graphviz_p.py 
	/bin/sh $(antlr_home)/scripts/antlr.sh $(g_FILES)


test : compile
	python graphviz_p.py < example.gv ;

### cleanup example.gv
clean ::
	@/bin/echo cleaning example.gv ...
	@ -/bin/rm -r -f $(g_py_FILES)
	@ -/bin/rm -r -f *.pyc *.tmp *TokenTypes.txt *TokenTypes
