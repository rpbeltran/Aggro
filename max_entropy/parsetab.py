
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftEQUALSCMP_LTCMP_GTleftANDORleftPLUSMINUSleftTIMESDIVIDErightPOWERnonassocNOTAND BOOLEAN_CONSTANT BY CMP_GT CMP_LT DIVIDE ELSE EQUALS EVENLY IF MINUS MOD NOT NUMERIC_CONSTANT OR OTHERWISE PLUS POWER THAN THEN TIMES TO UNWORDproposition : numeric_expression EQUALS EQUALS numeric_expression\n                   | numeric_expression EQUALS numeric_expression\n                   | numeric_expression inequality numeric_expression\n                   | numeric_expression EVENLY\n                   | BOOLEAN_CONSTANT\n    inequality : inequality OR EQUALS\n                  | inequality OR EQUALS TOinequality : EQUALS inequality\n    inequality : CMP_LT\n                  | CMP_GT\n                  | THAN\n                  | CMP_LT THAN\n                  | CMP_GT THANnumeric_expression : numeric_expression PLUS   numeric_expression \n                          | numeric_expression MINUS  numeric_expression\n                          | numeric_expression TIMES  numeric_expression\n                          | numeric_expression DIVIDE numeric_expression\n                          | numeric_expression POWER  numeric_expression\n                          | numeric_expression MOD    numeric_expression\n                          | identifier\n                          | numeric_const\n    numeric_const : NUMERIC_CONSTANTidentifier : identifier_content\n    identifier_content : UNWORD\n                          | UNWORD identifier_content\n    '
    
_lr_action_items = {'CMP_GT':([1,2,3,4,6,7,12,21,23,24,25,28,31,33,34,35,],[-20,-23,-22,-21,9,-24,9,-25,-17,-18,9,-16,-14,-19,-15,9,]),'OR':([9,14,16,18,22,26,32,37,38,],[-10,30,-9,-11,-13,30,-12,-6,-7,]),'DIVIDE':([1,2,3,4,6,7,21,23,24,27,28,29,31,33,34,36,],[-20,-23,-22,-21,10,-24,-25,-17,-18,10,-16,10,10,10,10,10,]),'POWER':([1,2,3,4,6,7,21,23,24,27,28,29,31,33,34,36,],[-20,-23,-22,-21,11,-24,-25,11,11,11,11,11,11,11,11,11,]),'MOD':([1,2,3,4,6,7,21,23,24,27,28,29,31,33,34,36,],[-20,-23,-22,-21,17,-24,-25,-17,-18,17,-16,17,-14,17,-15,17,]),'EVENLY':([1,2,3,4,6,7,21,23,24,28,31,33,34,],[-20,-23,-22,-21,20,-24,-25,-17,-18,-16,-14,-19,-15,]),'EQUALS':([1,2,3,4,6,7,12,21,23,24,25,28,30,31,33,34,35,],[-20,-23,-22,-21,12,-24,25,-25,-17,-18,35,-16,37,-14,-19,-15,35,]),'TIMES':([1,2,3,4,6,7,21,23,24,27,28,29,31,33,34,36,],[-20,-23,-22,-21,13,-24,-25,-17,-18,13,-16,13,13,13,13,13,]),'TO':([37,],[38,]),'UNWORD':([0,7,9,10,11,12,13,14,15,16,17,18,19,22,25,26,32,37,38,],[7,7,-10,7,7,7,7,7,7,-9,7,-11,7,-13,7,-8,-12,-6,-7,]),'PLUS':([1,2,3,4,6,7,21,23,24,27,28,29,31,33,34,36,],[-20,-23,-22,-21,15,-24,-25,-17,-18,15,-16,15,-14,15,-15,15,]),'CMP_LT':([1,2,3,4,6,7,12,21,23,24,25,28,31,33,34,35,],[-20,-23,-22,-21,16,-24,16,-25,-17,-18,16,-16,-14,-19,-15,16,]),'NUMERIC_CONSTANT':([0,9,10,11,12,13,14,15,16,17,18,19,22,25,26,32,37,38,],[3,-10,3,3,3,3,3,3,-9,3,-11,3,-13,3,-8,-12,-6,-7,]),'BOOLEAN_CONSTANT':([0,],[8,]),'MINUS':([1,2,3,4,6,7,21,23,24,27,28,29,31,33,34,36,],[-20,-23,-22,-21,19,-24,-25,-17,-18,19,-16,19,-14,19,-15,19,]),'THAN':([1,2,3,4,6,7,9,12,16,21,23,24,25,28,31,33,34,35,],[-20,-23,-22,-21,18,-24,22,18,32,-25,-17,-18,18,-16,-14,-19,-15,18,]),'$end':([1,2,3,4,5,7,8,20,21,23,24,27,28,29,31,33,34,36,],[-20,-23,-22,-21,0,-24,-5,-4,-25,-17,-18,-2,-16,-3,-14,-19,-15,-1,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'proposition':([0,],[5,]),'identifier_content':([0,7,10,11,12,13,14,15,17,19,25,],[2,21,2,2,2,2,2,2,2,2,2,]),'numeric_expression':([0,10,11,12,13,14,15,17,19,25,],[6,23,24,27,28,29,31,33,34,36,]),'inequality':([6,12,25,35,],[14,26,26,26,]),'numeric_const':([0,10,11,12,13,14,15,17,19,25,],[4,4,4,4,4,4,4,4,4,4,]),'identifier':([0,10,11,12,13,14,15,17,19,25,],[1,1,1,1,1,1,1,1,1,1,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> proposition","S'",1,None,None,None),
  ('proposition -> numeric_expression EQUALS EQUALS numeric_expression','proposition',4,'p_proposition','parser.py',71),
  ('proposition -> numeric_expression EQUALS numeric_expression','proposition',3,'p_proposition','parser.py',72),
  ('proposition -> numeric_expression inequality numeric_expression','proposition',3,'p_proposition','parser.py',73),
  ('proposition -> numeric_expression EVENLY','proposition',2,'p_proposition','parser.py',74),
  ('proposition -> BOOLEAN_CONSTANT','proposition',1,'p_proposition','parser.py',75),
  ('inequality -> inequality OR EQUALS','inequality',3,'p_proper_inequality','parser.py',98),
  ('inequality -> inequality OR EQUALS TO','inequality',4,'p_proper_inequality','parser.py',99),
  ('inequality -> EQUALS inequality','inequality',2,'p_inequality_cut_is','parser.py',104),
  ('inequality -> CMP_LT','inequality',1,'p_inequality','parser.py',111),
  ('inequality -> CMP_GT','inequality',1,'p_inequality','parser.py',112),
  ('inequality -> THAN','inequality',1,'p_inequality','parser.py',113),
  ('inequality -> CMP_LT THAN','inequality',2,'p_inequality','parser.py',114),
  ('inequality -> CMP_GT THAN','inequality',2,'p_inequality','parser.py',115),
  ('numeric_expression -> numeric_expression PLUS numeric_expression','numeric_expression',3,'p_numeric_expression','parser.py',120),
  ('numeric_expression -> numeric_expression MINUS numeric_expression','numeric_expression',3,'p_numeric_expression','parser.py',121),
  ('numeric_expression -> numeric_expression TIMES numeric_expression','numeric_expression',3,'p_numeric_expression','parser.py',122),
  ('numeric_expression -> numeric_expression DIVIDE numeric_expression','numeric_expression',3,'p_numeric_expression','parser.py',123),
  ('numeric_expression -> numeric_expression POWER numeric_expression','numeric_expression',3,'p_numeric_expression','parser.py',124),
  ('numeric_expression -> numeric_expression MOD numeric_expression','numeric_expression',3,'p_numeric_expression','parser.py',125),
  ('numeric_expression -> identifier','numeric_expression',1,'p_numeric_expression','parser.py',126),
  ('numeric_expression -> numeric_const','numeric_expression',1,'p_numeric_expression','parser.py',127),
  ('numeric_const -> NUMERIC_CONSTANT','numeric_const',1,'p_numeric_const','parser.py',136),
  ('identifier -> identifier_content','identifier',1,'p_identifier','parser.py',141),
  ('identifier_content -> UNWORD','identifier_content',1,'p_identifier_content','parser.py',148),
  ('identifier_content -> UNWORD identifier_content','identifier_content',2,'p_identifier_content','parser.py',149),
]