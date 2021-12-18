# BSD 3-Clause License
#
# Copyright (c) 2021, Paulus Gandung Prakosa <gandung@lists.infradead.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Parser objects, method, and related-operations.
"""

import parody.ast as ast
import parody.ast_kind as a
import parody.exceptions as ex
import parody.node_kind as n


class Parser(object):
    def __init__(self, lexer):
        self.token = None
        self.input = None
        self.position = 0
        self.line = 0
        self.lexer = lexer
        self.ast = ast.Ast(a.AST_ROOT, None)

    """
	"""

    def parse(self, buffer):
        try:
            self.lexer.lex(buffer)
        except ex.AbstractParodyError as e:
            raise e

        self.input = self.lexer.get_token_objects()

        while True:
            if self._is_eof():
                break

            if self._current().get_type() == n.LABEL:
                self._process_label()

            if self._current().get_type() == n.MNEMONIC:
                self._process_instruction_line()

            self._next()

    """
	"""

    def get_lexer(self):
        return self.lexer

    """
	"""

    def set_lexer(self, lexer):
        self.lexer = lexer

    """
	"""

    def get_input(self):
        return self.input

    """
	"""

    def set_input(self, input):
        self.input = input

    """
	"""

    def get_ast(self):
        return self.ast

    """
	"""

    def set_ast(self, ast):
        self.ast = ast

    """
	"""

    def _current(self):
        return self.input[self.position]

    """
	"""

    def _next(self):
        self.position += 1

    """
	"""

    def _prev(self):
        self.position -= 1

    """
	"""

    def _is_eof(self):
        return self.position >= len(self.input)

    """
	"""

    def _process_label(self):
        self.ast.add_child(ast.Ast(a.AST_LABEL, self._current()))

    """
	"""

    def _process_instruction_line(self):
        tmp = []

        while True:
            if self._is_eof():
                break

            if self._current().get_type() == n.NEWLINE:
                self.line += 1
                break

            tmp.append(self._current())
            self._next()

        if len(tmp) == 0:
            return

        if tmp[0].get_type() != n.MNEMONIC:
            raise SyntaxError("Instruction line must be prefixed by valid mnemonic.")

        self._run_instruction_line_validator(tmp)

        child = ast.Ast(a.AST_INSTRUCTION_LINE, None)

        for el in tmp:
            if el.get_type() == n.COMMA:
                continue

            child.add_child(ast.Ast(self._determine_node_type(el), el))

        self.ast.add_child(child)

    """
	"""

    def _validate_binary_movb_instruction(self, insn):
        if insn[0].get_value() == "movb" and insn[3].get_type() == n.NUMBER:
            raise SyntaxError(
                "Number cannot be placed in second operand when it's mnemonic "
                + " is 'movb' (line: %d)." % (self.line)
            )

        if insn[0].get_value() == "movb" and (
            (insn[1].get_type() != n.REGISTER or insn[1].get_type() != n.NUMBER)
            and insn[3].get_type() != n.REGISTER
        ):
            raise SyntaxError(
                "First operand must be register or numeric constant, and second operand "
                + "must be register (line: %d)." % (self.line)
            )

    """
	"""

    def _validate_binary_addb_instruction(self, insn):
        if insn[0].get_value() == "addb" and insn[3].get_type() == n.NUMBER:
            raise SyntaxError(
                "Number cannot be placed in second operand when it's mnemonic is "
                + "'addb' (line: %d)." % (self.line)
            )

        if insn[0].get_value() == "addb" and (
            (insn[1].get_type() != n.REGISTER or insn[1].get_type() != n.NUMBER)
            and insn[3].get_type() != n.REGISTER
        ):
            raise SyntaxError(
                "First operand must be register or numeric constant, and second operand "
                + "must be register (line: %d)." % (self.line)
            )

    """
	"""

    def _validate_binary_subb_instruction(self, insn):
        if insn[0].get_value() == "subb" and insn[3].get_type() == n.NUMBER:
            raise SyntaxError(
                "Number cannot be placed in second operand when it's mnemonic is "
                + "'subb' (line: %d)." % (self.line)
            )

        if insn[0].get_value() == "subb" and (
            (insn[1].get_type() != n.REGISTER or insn[1].get_type() != n.NUMBER)
            and insn[3].get_type() != n.REGISTER
        ):
            raise SyntaxError(
                "First operand must be register or numeric constant, and second operand "
                + "must be register (line: %d)." % (self.line)
            )

    """
	"""

    def _validate_binary_mulb_instruction(self, insn):
        if insn[0].get_value() == "mulb" and insn[3].get_type() == n.NUMBER:
            raise SyntaxError(
                "Number cannot be placed in second operand when it's mnemonic is "
                + "'mulb' (line: %d)." % (self.line)
            )

        if insn[0].get_value() == "mulb" and (
            (insn[1].get_type() != n.REGISTER or insn[1].get_type() != n.NUMBER)
            and insn[3].get_type() != n.REGISTER
        ):
            raise SyntaxError(
                "First operand must be register or numeric constant, and second operand "
                + "must be register (line: %d)." % (self.line)
            )

    """
	"""

    def _validate_binary_divb_instruction(self, insn):
        if insn[0].get_value() == "divb" and insn[3].get_type() == n.NUMBER:
            raise SyntaxError(
                "Number cannot be placed in second operand when it's mnemonic is "
                + "'mulb' (line: %d)." % (self.line)
            )

        if insn[0].get_value() == "divb" and (
            (insn[1].get_type() != n.REGISTER or insn[1].get_type() != n.NUMBER)
            and insn[3].get_type() != n.REGISTER
        ):
            raise SyntaxError(
                "First operand must be register or numeric constant, and second operand "
                + "must be register (line: %d)." % (self.line)
            )

    """
	"""

    def _validate_binary_prib_instruction(self, insn):
        if insn[0].get_value() == "prib" and (
            insn[1].get_type() != n.NUMBER and insn[1].get_type() != n.REGISTER
        ):
            raise SyntaxError(
                "'prib' instruction must be followed by register name or number."
            )

    """
	"""

    def _run_instruction_line_validator(self, insn):
        ilen = len(insn)

        if ilen == 2:
            self._validate_binary_prib_instruction(insn)
        elif ilen == 4:
            self._validate_binary_movb_instruction(insn)
            self._validate_binary_addb_instruction(insn)
            self._validate_binary_subb_instruction(insn)
            self._validate_binary_mulb_instruction(insn)
            self._validate_binary_divb_instruction(insn)
        else:
            raise SyntaxError("Unknown instruction.")

    """
	"""

    def _determine_node_type(self, val):
        if val.get_type() == n.MNEMONIC:
            return a.AST_MNEMONIC
        elif val.get_type() == n.REGISTER:
            return a.AST_REGISTER
        elif val.get_type() == n.NUMBER:
            return a.AST_INTEGER_VALUE
