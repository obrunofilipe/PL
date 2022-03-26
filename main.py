import makeJson as mj
import ops
import lexer

lexer.readTokens()
ops.apply_op(lexer.get_dics(), lexer.get_cabecalho())
mj.dicToJson(lexer.get_dics(), lexer.get_cabecalho())