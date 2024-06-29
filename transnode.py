from objs import MainFile, MainNode
from typedef import LuaNode, FilePointer
from datac import Slice
from ast import parse as python_parse
from transform.python import transform_lua_node
from antlr4.Token import CommonToken
from antlr4.CommonTokenStream import CommonTokenStream


class TransNode:

    def __init__(self, 
                 node:LuaNode="", 
                 index:int=0, 
                 source: FilePointer|str=MainFile) -> None:
        
        """
        Transpiler Node, represents the lua node, lua source, python node, and python source can be used with a buffer or a string
        Arguments:
            node (luaparser.astnodes.Node): any luaparser node
            index (int)                   : the node index in the list of nodes
            source (TextIOWrapper|str)    : if TextIOWrapper: 
                                                memory [optimized] - attributes are created as needed
                                            elif str:
                                                memory [ineffective] -attributes are initialized when they can be
        Properties       | Access    |  Attributes                    | Type                           |
            index         (public)  ->  self                            [int]
            lua_node      (public)  ->  self                            [luaparser.astnodes.Node <ANY>]
            source        (public)  ->  self.__source        (private)  [str or TextIOWrapper]
            python_string (public)  ->  self.__python_string (private)  [str]
            python_node   (public)  ->  self.__python_node   (private)  [ast.AST]
            lua_slice     (public)  ->  self.__lua_slice     (private)  [Slice]
            lua_string    (public)  ->  self.__lua_string    (private)  [str]

        """

        # initialized attributes
        self.lua_node = node
        self.index = index
        self.lua_tokens:list[list[CommonToken]] = []
        self.__source = source
        
        # as needed attributes
        self.__python_node = None
        self.__python_string = None
        self.indentation = 0
        

        # input dependent attributes
        if isinstance(self.__source, FilePointer):
            self.__lua_slice: Slice = None
            self.__lua_string = None
        else:
            try:
                self.__lua_slice = Slice(self.lua_node.first_token.start, self.lua_node.last_token.stop)
            except:
                try:
                    self.__lua_slice = Slice(self.lua_node.first_token.start, -1)
                except:
                    self.__lua_slice = Slice(0, -1)

            self.__lua_string = self.__source[self.__lua_slice.start:self.__lua_slice.end]
            
    @property
    def lua_slice(self) -> Slice:
        if self.__lua_slice == None:
            self.__lua_slice = Slice(self.lua_node.first_token.start, self.lua_node.last_token.stop)
        return self.__lua_slice

    @property
    def python_string(self) -> str:
        if self.__python_string == None:
            self.__python_string = transform_lua_node(self.lua_node)
        return self.__python_string
    
    @property
    def lua_string(self) -> str:
        if self.lua_string == None:
            self.__source.seek(self.lua_node.first_token.start)
            self.__lua_string = self.__source.read(self.lua_node.first_token.start-self.lua_node.last_token.stop)
            self.__source.seek(0)
        return self.__lua_string
   
    @property
    def python_node(self):
        if self.__python_node == None:
            if self.__python_string == None:
                self.__python_string = transform_lua_node(self.lua_node)
            self.__python_node = python_parse(source=self.__python_string, mode="eval")
        return self.__python_node
    
    def collect_tokens(self, token_stream: CommonTokenStream):
        self.lua_tokens.append(token_stream.getTokens(self.__lua_slice.start, self.__lua_slice.end))

        try:
            self.indentation = token_stream.getHiddenTokensToLeft(self.lua_node.first_token.start)
        except:
            self.indentation = None

        self.indentation = 0 if self.indentation == None else len(self.indentation)
            
        # fixes the indents here
        retv = []
        ind = " "*self.indentation
        for line in self.python_string.split("\n"):
            retv.append(ind + line)
        self.__python_string = "\n".join(retv)

    #def fix_indentation(self):
    #    retv = []
    #    ind = " "*len(self.indentation)
    #    for line in self.python_string.split("\n"):
    #        retv.append(ind + line)
    #    self.__python_string = "\n".join(retv)