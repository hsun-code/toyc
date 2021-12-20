from tok import TokenType


class Var(object):
    def __init__(self, var_name, data_type, scope, is_ptr, is_ary, is_inited, size, offset):
        assert isinstance(data_type, TokenType), "data_type must be TokenType!"
        assert isinstance(scope, list), "scope must be list!"
        self.var_name = var_name    # string: variable name
        self.data_type = data_type  # TokenType: only INT supported
        self.scope = scope          # int list. element: scope info
        self.is_ptr = is_ptr        # 1 for pointer type
        self.is_ary = is_ary        # 1 for array
        self.is_inited = is_inited  # 1 if has initialization expr
        self.size = size            # int: number of bytes this variable can occupy
        self.offset = offset        # int: offset to frame pointer


class Fun(object):
    def __init__(self, func_name, data_type, para_list, max_depth, cur_depth, scope_info, ir_list):
        assert isinstance(data_type, TokenType), "data_type must be TokenType!"
        assert isinstance(para_list, list), "para_list must be list!"
        assert isinstance(scope_info, list), "scope_info must be list!"
        assert isinstance(ir_list, list), "ir_list must be list!"
        self.func_name = func_name    # string: function name
        self.data_type = data_type    # TokenType: only INT supported
        self.para_list = para_list    # int list. element: parameter index
        self.max_depth = max_depth    # int: max allocated size
        self.cur_depth = cur_depth    # int: current depth
        self.scope_info = scope_info  # int list. element: scope info
        self.ir_list = ir_list        # IR list: element: ir instruction
