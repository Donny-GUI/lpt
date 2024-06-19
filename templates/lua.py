from luaparser import astnodes


all_nodes = [astnodes.Node, astnodes.Comment, astnodes.Expression, astnodes.Statement, astnodes.Block, astnodes.Chunk, astnodes.Lhs, astnodes.Name, astnodes.IndexNotation, astnodes.Index, astnodes.Assign, astnodes.LocalAssign, astnodes.While, astnodes.Do, astnodes.Repeat, astnodes.ElseIf, astnodes.If, astnodes.Label, astnodes.Goto, astnodes.SemiColon, astnodes.Break, astnodes.Return, astnodes.Fornum, astnodes.Forin, astnodes.Call, astnodes.Invoke, astnodes.Function, astnodes.LocalFunction, astnodes.Method, astnodes.Nil, astnodes.TrueExpr, astnodes.FalseExpr, astnodes.Number, astnodes.Varargs, astnodes.StringDelimiter, astnodes.String, astnodes.Field, astnodes.Table, astnodes.Dots, astnodes.AnonymousFunction, astnodes.Op, astnodes.BinaryOp, astnodes.AriOp, astnodes.AddOp, astnodes.SubOp, astnodes.MultOp, astnodes.FloatDivOp, astnodes.FloorDivOp, astnodes.ModOp, astnodes.ExpoOp, astnodes.BitOp, astnodes.BAndOp, astnodes.BOrOp, astnodes.BXorOp, astnodes.BShiftROp, astnodes.BShiftLOp, astnodes.RelOp, astnodes.LessThanOp, astnodes.GreaterThanOp, astnodes.LessOrEqThanOp, astnodes.GreaterOrEqThanOp, astnodes.EqToOp, astnodes.NotEqToOp, astnodes.LoOp, astnodes.AndLoOp, astnodes.OrLoOp, astnodes.Concat, astnodes.UnaryOp, astnodes.UMinusOp, astnodes.UBNotOp, astnodes.ULNotOp, ULengthOP]