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
Lexing class, objects, and properties.
"""

import parody.token_kind as t
import parody.node_kind as n
import parody.node as node

from parody.exceptions import SyntaxError as ParodySyntaxError
from parody.exceptions import LexedEntityError


class Lexer(object):
    def __init__(self):
        self.input = ""
        self.token = ""
        self.position = 0
        self.is_negative = False
        self.token_objects = []

    """
	"""

    def lex(buffer):
        self.input = buffer

        while True:
            if self._is_eof():
                self._process_when_eof()
                break

            if self.token == t.SPACE or self.token == t.TAB:
                self.token = ""
                continue

            if self.token == t.NEWLINE:
                self._process_newline()
                self.token = ""
                continue

            if self.token == t.START_COMMENT_LINE:
                self._process_comment_line()
                self.token = ""
                continue

            if self.token == t.COMMA:
                self._process_comma()
                self.token = ""
                continue

            if self.token == t.PREFIX_NUM:
                self._process_integer()
                self.token = ""
                continue

            if self.token == t.START_LABEL:
                self._process_label()
                self.token = ""
                continue

            if self._is_valid_instruction(self.token):
                self._process_mnemonic()
                self.token = ""
                continue

            if self._is_valid_register(self.token):
                self._process_register()
                self.token = ""
                continue

            self.token += self._current()
            self._next()

    """
	"""

    def get_token_objects(self):
        return self.token_objects

    """
	"""

    def add_node(self, node):
        self.token_objects.append(node)

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

    def _current(self):
        return self.input[self.position]

    """
	"""

    def _peek(self):
        return self.input[self.position + 1]

    """
	"""

    def _is_eof(self):
        return self.position >= len(self.input)

    """
	"""

    def _process_comma(self):
        self.add_node(node.Comma(self.token))

    """
	"""

    def _process_integer(self):
        try:
            self.input[self.position]
        except IndexError as e:
            raise ParodySyntaxError(
                "Syntax error, '#' must be followed by number "
                + "(either positive/negative) or +/- sign then followed by number."
            )

        self.token = ""
        self.is_negative = True if self._current() == "-" else False

        if self.is_negative == True:
            self._next()

        exists = True

        try:
            self.input[self.position]
        except IndexError as e:
            exists = False

        if self.is_negative == True and exists == False:
            raise ParodySyntaxError(
                "Syntax error, '-' must be followed by decimal digit."
            )

        while True:
            try:
                self.input[self.position]
            except IndexError as e:
                break

            if self._current().isnumeric() == False or self._current() == t.COMMA:
                break

            self.token += self._current()
            self._next()

        self.add_node(
            node.Number(
                int(self.token) * -1 if self.is_negative == True else int(self.token)
            )
        )

    """
	"""

    def _process_label(self):
        exception = False

        while True:
            if self._is_eof() or self._current() == t.NEWLINE:
                break

            if self._current() == t.SPACE:
                exception = True
                break

            self.token += self._current()
            self._next()

        if exception == True:
            raise LexedEntityError("Label name cannot contain whitespace characters.")

        if self.token[-1] != ":" and (
            len(self.token_objects) == 0
            and self.token_objects[-1].get_type() != n.MNEMONIC
        ):
            raise LexedEntityError("Label name must ended by colon.")

        self.token = self.token[: (-1 if self.token[-1] == ":" else len(self.token))]
        self.add_node(node.Label(self.token))

    """
	"""

    def _process_mnemonic(self):
        self.add_node(node.Mnemonic(self.token))

    """
	"""

    def _process_newline(self):
        self.add_node(node.Newline(self.token))

    """
	"""

    def _process_comment_line(self):
        while True:
            if self._is_eof():
                break

            if self._current() == t.NEWLINE:
                self.token = self._current()
                break

            # ignore the current token except newline
            # because this is in the scope of comment
            # section.
            self._next()

        if self.token == t.NEWLINE:
            self._process_newline()

    """
	"""

    def _process_register(self):
        self.add_node(node.Register(self.token))

    """
	"""

    def _process_when_eof(self):
        if self._is_valid_insn(self.token):
            self._process_mnemonic()

        if self._is_valid_reg(self.token):
            self._process_register()

    """
	"""

    def _get_valid_insns(self):
        return ["movb", "addb", "subb", "mulb", "divb", "prib", "jmp"]

    """
	"""

    def _is_valid_insn(self, insn):
        return insn in self._get_valid_insns()

    """
	"""

    def _get_valid_regs(self):
        return ["r0", "r1", "r2", "r3"]

    """
	"""

    def _is_valid_reg(self, reg):
        return reg in self._get_valid_regs()
