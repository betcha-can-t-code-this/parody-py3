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
AST objects, methods, and related-operations.
"""

import parody.ast_kind as a

class Ast(object):
    def __init__(self, ast_type, value):
        self.value = value
        self.type = ast_type
        self.childs = []

    """
	"""

    def get_value(self):
        return self.value

    """
	"""

    def set_value(self, value):
        self.value = value

    """
	"""

    def get_type(self):
        return self.type

    """
	"""

    def set_type(self, ast_type):
        self.type = ast_type

    """
	"""

    def get_child_at(self, index):
        try:
            return self.childs[index]
        except IndexError as e:
            return None

    """
	"""

    def get_childs(self):
        return self.childs

    """
	"""

    def set_childs(self, childs):
        self.childs = childs

    """
	"""

    def add_child(self, child):
        self.childs.append(child)

    """
    """
    def _type_to_string_resolver(self, ast_type):
        if ast_type == a.AST_ROOT:
            return '<root>'
        elif ast_type == a.AST_MNEMONIC:
            return '<mnemonic>'
        elif ast_type == a.AST_REGISTER:
            return '<register>'
        elif ast_type == a.AST_INTEGER_VALUE:
            return '<integer>'
        elif ast_type == a.AST_INSTRUCTION_LINE:
            return '<instruction-line>'
        elif ast_type == a.AST_LABEL:
            return '<label>'

    """
    """
    def __repr__(self):
        return '%s (%s)' % (
            self._type_to_string_resolver(self.get_type()),
            '<nil>' if self.get_value() == None else self.get_value()
        )
