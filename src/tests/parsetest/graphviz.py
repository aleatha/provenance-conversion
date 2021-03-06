import sys
import antlr
      

class Visitor(antlr.ASTVisitor):
   def __init__(self,*args):
      super(Visitor,self).__init__(*args)
      self.level = 0
      if not args:
         self.cout = sys.stdout
         return
      if isinstance(args[0],file):
         self.cout = args[0]
         return
      assert 0

   def tabs(self):
      print " " * self.level

   def printf(self,fmt,*args):
      if not args:
          sys.stdout.write(fmt)
          return
      argv = tuple(args)
      self.cout.write(fmt % argv)

   def flush(self):
      self.cout.flush()

   def visit1(self,node,level):
      if not node:
         self.printf(" nil ")
         return

      c = node.getType()
      t = node.getText()
      k = node.getFirstChild()
      s = node.getNextSibling()
      tabs = " " * level
      print "tabs:"+str(level)
      self.printf("\n"+tabs+" <%s> ",c)
      if t:
         self.printf(" %s ",t)
      self.printf("(")
      self.visit1(k,level+1);
      self.printf(")\n")
      self.visit1(s,level);


   def visit(self,node):
      self.visit1(node,0);
      self.printf("\n")



class GraphVizAST(antlr.CommonAST):
   def __init__(self,*args):
      antlr.CommonAST.__init__(self,*args)


      


def main():
   import graphviz_l
   import graphviz_p
   
   L = graphviz_l.Lexer() 
   P = graphviz_p.Parser(L)
   P.setFilename(L.getFilename())

   ### Parse the input expression
   try:
      P.diagram()
   except antlr.ANTLRException, ex:
      print "*** error(s) while parsing."
      print ">>> exit(1)"
      import sys
      sys.exit(1)

   
   ast = P.getAST()
   
   if not ast:
      print "stop - no AST generated."
      import sys
      sys.exit(1)
      
   ###show tree
   #print "Tree: " + ast.toStringTree()
   #print "List: " + ast.toStringList()
   #print "Node: " + ast.toString()
   #print "visit>>"
   #visitor = Visitor()
   #visitor.visit(ast);
   #print "visit<<"

if __name__ == "__main__":
   main()
