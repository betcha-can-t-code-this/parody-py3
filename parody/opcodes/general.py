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
General opcode for Parody VM.
"""

MOVB_R0_TO_R0 = 0x10
MOVB_R1_TO_R0 = 0x11
MOVB_R2_TO_R0 = 0x12
MOVB_R3_TO_R0 = 0x13

MOVB_R0_TO_R1 = 0x14
MOVB_R1_TO_R1 = 0x15
MOVB_R2_TO_R1 = 0x16
MOVB_R3_TO_R1 = 0x17

MOVB_R0_TO_R2 = 0x18
MOVB_R1_TO_R2 = 0x19
MOVB_R2_TO_R2 = 0x1a
MOVB_R3_TO_R2 = 0x1b

MOVB_R0_TO_R3 = 0x1c
MOVB_R1_TO_R3 = 0x1d
MOVB_R2_TO_R3 = 0x1e
MOVB_R3_TO_R3 = 0x1f

ADDB_R0_TO_R0 = 0x20
ADDB_R1_TO_R0 = 0x21
ADDB_R2_TO_R0 = 0x22
ADDB_R3_TO_R0 = 0x23

ADDB_R0_TO_R1 = 0x24
ADDB_R1_TO_R1 = 0x25
ADDB_R2_TO_R1 = 0x26
ADDB_R3_TO_R1 = 0x27

ADDB_R0_TO_R2 = 0x28
ADDB_R1_TO_R2 = 0x29
ADDB_R2_TO_R2 = 0x2a
ADDB_R3_TO_R2 = 0x2b

ADDB_R0_TO_R3 = 0x2c
ADDB_R1_TO_R3 = 0x2d
ADDB_R2_TO_R3 = 0x2e
ADDB_R3_TO_R3 = 0x2f

SUBB_R0_TO_R0 = 0x30
SUBB_R1_TO_R0 = 0x31
SUBB_R2_TO_R0 = 0x32
SUBB_R3_TO_R0 = 0x33

SUBB_R0_TO_R1 = 0x34
SUBB_R1_TO_R1 = 0x35
SUBB_R2_TO_R1 = 0x36
SUBB_R3_TO_R1 = 0x37

SUBB_R0_TO_R2 = 0x38
SUBB_R1_TO_R2 = 0x39
SUBB_R2_TO_R2 = 0x3a
SUBB_R3_TO_R2 = 0x3b

SUBB_R0_TO_R3 = 0x3c
SUBB_R1_TO_R3 = 0x3d
SUBB_R2_TO_R3 = 0x3e
SUBB_R3_TO_R3 = 0x3f

MULB_R0_TO_R0 = 0x40
MULB_R1_TO_R0 = 0x41
MULB_R2_TO_R0 = 0x42
MULB_R3_TO_R0 = 0x43

MULB_R0_TO_R1 = 0x44
MULB_R1_TO_R1 = 0x45
MULB_R2_TO_R1 = 0x46
MULB_R3_TO_R1 = 0x47

MULB_R0_TO_R2 = 0x48
MULB_R1_TO_R2 = 0x49
MULB_R2_TO_R2 = 0x4a
MULB_R3_TO_R2 = 0x4b

MULB_R0_TO_R3 = 0x4c
MULB_R1_TO_R3 = 0x4d
MULB_R2_TO_R3 = 0x4e
MULB_R3_TO_R3 = 0x4f

DIVB_R0_TO_R0 = 0x50
DIVB_R1_TO_R0 = 0x51
DIVB_R2_TO_R0 = 0x52
DIVB_R3_TO_R0 = 0x53

DIVB_R0_TO_R1 = 0x54
DIVB_R1_TO_R1 = 0x55
DIVB_R2_TO_R1 = 0x56
DIVB_R3_TO_R1 = 0x57

DIVB_R0_TO_R2 = 0x58
DIVB_R1_TO_R2 = 0x59
DIVB_R2_TO_R2 = 0x5a
DIVB_R3_TO_R2 = 0x5b
