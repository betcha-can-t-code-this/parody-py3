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
Bytecode generator objects, methods, and related-operations.
"""

import parody.ast_kind as a
import parody.exceptions as ex
import parody.node_kind as n
import parody.opcodes.general as gen
import parody.opcodes.jump as jgen

class Codegen(object):
	def __init__(self, jump_label):
		self.jump_label = jump_label
		self.patch_jump = []
		self.patch_loop = []
		self.generated  = []

	"""
	"""
	def generate(self, ast):
		if ast.get_type() != a.AST_ROOT:
			raise ex.AstError("Current ast type is not root.")

		exception = False

		for vnode in ast.get_childs():
			if vnode.get_type() != a.AST_INSTRUCTION_LINE and \
			   vnode.get_type() != a.AST_LABEL:
				exception = True
				break

			if vnode.get_type() == a.AST_LABEL:
				self.jump_label.add(vnode.get_value().get_value(), len(self.generated) - 1)
				continue

			self._process_instruction_line(vnode)

		if exception == True:
			raise a.AstError("Current ast node is not instruction or label.")

		# patching jump instruction, if any.
		for el in self.patch_jump:
			off = self.jump_label.fetch(el[2])

			if off == -1:
				continue

			l = self._deserialize_vanilla_number(off)
			p = el[0]

			self.generated[p + 0] = gen.JUMP_REX_PREFIX
			self.generated[p + 1] = el[1]
			self.generated[p + 2] = l[0]
			self.generated[p + 3] = l[1]
			self.generated[p + 4] = l[2]
			self.generated[p + 5] = l[3]

		return ''.join(map(lambda x: chr(x), self.generated))

	"""
	"""
	def get_jump_label(self):
		return self.jump_label

	"""
	"""
	def _process_instruction_line(self, ast):
		if len(ast.get_childs()) == 2 and \
		   ast.get_childs()[0].get_value().get_value() == "jmp":
			self._process_unary_jump_instruction(ast)

		if len(ast.get_childs()) == 2 and \
		   ast.get_childs()[0].get_value().get_value() == "prib":
			self._process_unary_prib_instruction(ast)

		if len(ast.get_childs()) == 3 and \
		   ast.get_childs()[0].get_value().get_value() == "movb":
			self._process_binary_movb_instruction(ast)

		if len(ast.get_childs()) == 3 and \
		   ast.get_childs()[0].get_value().get_value() == "addb":
			self._process_binary_addb_instruction(ast)

		if len(ast.get_childs()) == 3 and \
		   ast.get_childs()[0].get_value().get_value() == "subb":
			self._process_binary_subb_instruction(ast)

		if len(ast.get_childs()) == 3 and \
		   ast.get_childs()[0].get_value().get_value() == "mulb":
			self._process_binary_mulb_instruction(ast)

		if len(ast.get_childs()) == 3 and \
		   ast.get_childs()[0].get_value().get_value() == "divb":
			self._process_binary_divb_instruction(ast)

	"""
	"""
	def _process_unary_jump_instruction(ast):
		if ast.get_childs()[1].get_value().get_type() != n.LABEL:
			raise ex.AstError(
				"Jump-related instruction must be followed by label name."
			)

		name            = ast.get_childs()[1].get_value().get_value()
		repl            = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
		jump            = [len(self.generated), jgen.JUMP_PLAIN, name]
		self.generated += repl

		self.patch_jump.append(jump)

	"""
	"""
	def _process_unary_prib_instruction(ast):
		if ast.get_childs()[1].get_value().get_type() == n.NUMBER:
			num = ast.get_childs()[1]
				.get_value()
				.get_value()
			ser = self._deserialize_number(num)

		defined = True

		try:
			ser
		except NameError as e:
			defined = False

		if defined == True:
			self.generated += [gen.PRIB_IMM8] + ser
			return

		name = ast.get_childs()[1]
			.get_value()
			.get_value()

		if name == 'r0':
			self.generated.append(gen.PRIB_R0)
		elif name == 'r1':
			self.generated.append(gen.PRIB_R1)
		elif name == 'r2':
			self.generated.append(gen.PRIB_R2)
		elif name == 'r3':
			self.generated.append(gen.PRIB_R3)

	"""
	"""
	def _process_binary_movb_instruction(ast):
		if ast.get_childs()[1].get_value().get_type() == n.NUMBER:
			num = ast.get_childs()[1]
				.get_value()
				.get_value()
			ser = self._deserialize_number(num)

		defined = True

		try:
			ser
		except NameError as e:
			defined = False

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated += [gen.MOVB_IMM8_TO_R0] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated += [gen.MOVB_IMM8_TO_R1] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated += [gen.MOVB_IMM8_TO_R2] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated += [gen.MOVB_IMM8_TO_R3] + ser
			return

		if ast.get_childs()[1].get_value().get_type() == n.REGISTER and \
		   ast.get_childs()[2].get_value().get_type() == n.REGISTER:
			self._process_binary_movb_regs_to_regs_instruction(ast)
			return

	"""
	"""
	def _process_binary_movb_regs_to_regs_instruction(ast):
		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MOVB_R0_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MOVB_R1_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MOVB_R2_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MOVB_R3_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MOVB_R0_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MOVB_R1_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MOVB_R2_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MOVB_R3_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MOVB_R0_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MOVB_R1_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MOVB_R2_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MOVB_R3_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MOVB_R0_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MOVB_R1_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MOVB_R2_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MOVB_R3_TO_R3)
			return

	"""
	"""
	def _process_binary_addb_instruction(ast):
		if ast.get_childs()[1].get_value().get_type() == n.NUMBER:
			num = ast.get_childs()[1]
				.get_value()
				.get_value()
			ser = self._deserialize_number(num)

		defined = True

		try:
			ser
		except NameError as e:
			defined = False

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated += [gen.ADDB_IMM8_TO_R0] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated += [gen.ADDB_IMM8_TO_R1] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated += [gen.ADDB_IMM8_TO_R2] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated += [gen.ADDB_IMM8_TO_R3] + ser
			return

		if ast.get_childs()[1].get_value().get_type() == n.REGISTER and \
		   ast.get_childs()[2].get_value().get_type() == n.REGISTER:
			self._process_binary_addb_regs_to_regs_instruction(ast)
			return

	"""
	"""
	def _process_binary_addb_regs_to_regs_instruction(ast):
		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.ADDB_R0_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.ADDB_R1_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.ADDB_R2_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.ADDB_R3_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.ADDB_R0_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.ADDB_R1_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.ADDB_R2_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.ADDB_R3_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.ADDB_R0_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.ADDB_R1_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.ADDB_R2_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.ADDB_R3_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.ADDB_R0_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.ADDB_R1_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.ADDB_R2_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.ADDB_R3_TO_R3)
			return

	"""
	"""
	def _process_binary_subb_instruction(ast):
		if ast.get_childs()[1].get_value().get_type() == n.NUMBER:
			num = ast.get_childs()[1]
				.get_value()
				.get_value()
			ser = self._deserialize_number(num)

		defined = True

		try:
			ser
		except NameError as e:
			defined = False

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated += [gen.SUBB_IMM8_TO_R0] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated += [gen.SUBB_IMM8_TO_R1] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated += [gen.SUBB_IMM8_TO_R2] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated += [gen.SUBB_IMM8_TO_R3] + ser
			return

		if ast.get_childs()[1].get_value().get_type() == n.REGISTER and \
		   ast.get_childs()[2].get_value().get_type() == n.REGISTER:
			self._process_binary_subb_regs_to_regs_instruction(ast)

	"""
	"""
	def _process_binary_subb_regs_to_regs_instruction(ast):
		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.SUBB_R0_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.SUBB_R1_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.SUBB_R2_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.SUBB_R3_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.SUBB_R0_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.SUBB_R1_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.SUBB_R2_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.SUBB_R3_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.SUBB_R0_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.SUBB_R1_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.SUBB_R2_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.SUBB_R3_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.SUBB_R0_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.SUBB_R1_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.SUBB_R2_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.SUBB_R3_TO_R3)
			return

	"""
	"""
	def _process_binary_mulb_instruction(ast):
		if ast.get_childs()[1].get_value().get_type() == n.NUMBER:
			num = ast.get_childs()[1]
				.get_value()
				.get_value()
			ser = self._deserialize_number(num)

		defined = True

		try:
			ser
		except NameError as e:
			defined = False

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated += [gen.MULB_IMM8_TO_R0] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated += [gen.MULB_IMM8_TO_R1] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated += [gen.MULB_IMM8_TO_R2] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated += [gen.MULB_IMM8_TO_R3] + ser
			return

		if ast.get_childs()[1].get_value().get_type() == n.REGISTER and \
		   ast.get_childs()[2].get_value().get_type() == n.REGISTER:
			self._process_binary_mulb_regs_to_regs_instruction(ast)

	"""
	"""
	def _process_binary_mulb_regs_to_regs_instruction(ast):
		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MULB_R0_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MULB_R1_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MULB_R2_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.MULB_R3_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MULB_R0_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MULB_R1_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MULB_R2_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.MULB_R3_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MULB_R0_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MULB_R1_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MULB_R2_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.MULB_R3_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MULB_R0_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MULB_R1_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MULB_R2_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.MULB_R3_TO_R3)
			return

	"""
	"""
	def _process_binary_divb_instruction(ast):
		if ast.get_childs()[1].get_value().get_type() == n.NUMBER:
			num = ast.get_childs()[1]
				.get_value()
				.get_value()
			ser = self._deserialize_number(num)

		defined = True

		try:
			ser
		except NameError as e:
			defined = False

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated += [gen.DIVB_IMM8_TO_R0] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated += [gen.DIVB_IMM8_TO_R1] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated += [gen.DIVB_IMM8_TO_R2] + ser
			return

		if defined == True and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated += [gen.DIVB_IMM8_TO_R3] + ser
			return

		if ast.get_childs()[1].get_value().get_type() == n.REGISTER and \
		   ast.get_childs()[2].get_value().get_type() == n.REGISTER:
			self._process_binary_divb_regs_to_regs_instruction(ast)
			return

	"""
	"""
	def _process_binary_divb_regs_to_regs_instruction(ast):
		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.DIVB_R0_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.DIVB_R1_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.DIVB_R2_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r0':
			self.generated.append(gen.DIVB_R3_TO_R0)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.DIVB_R0_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.DIVB_R1_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.DIVB_R2_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r1':
			self.generated.append(gen.DIVB_R3_TO_R1)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.DIVB_R0_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.DIVB_R1_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.DIVB_R2_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r2':
			self.generated.append(gen.DIVB_R3_TO_R2)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r0' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.DIVB_R0_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r1' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.DIVB_R1_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r2' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.DIVB_R2_TO_R3)
			return

		if ast.get_childs()[1].get_value().get_value() == 'r3' and \
		   ast.get_childs()[2].get_value().get_value() == 'r3':
			self.generated.append(gen.DIVB_R3_TO_R3)
			return

	"""
	"""
	def _deserialize_vanilla_number(self, num):
		return [
			((num & 0xff000000) >> 24),
			((num & 0x00ff0000) >> 16),
			((num & 0x0000ff00) >>  8),
			((num & 0x000000ff) >>  0)
		]

	"""
	"""
	def _deserialize_number(self, num):
		norm = abs(num)

		return [
			0xff if num < 0 else 0xfe,
			((norm & 0xff000000) >> 24),
			((norm & 0x00ff0000) >> 16),
			((norm & 0x0000ff00) >>  8),
			((norm & 0x000000ff) >>  0)
		]
