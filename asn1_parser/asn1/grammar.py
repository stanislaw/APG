GRAMMAR = """
Asn1Module[noskipws]:
  (comment=Asn1Comment)?
  'Module-' module_name=NameLower ' DEFINITIONS AUTOMATIC TAGS ::= BEGIN'
  /\\s*/-
  (
    (comment_import = Asn1Comment)? 'IMPORTS' import_items+=ImportItem ';' '\n'
  )?
  (definitions += Definitions)
  'END'
;

ImportItem[noskipws]:
  /\\s*/-
  (comment=Asn1Comment)?
  /\\s*/-
  definitions+=NameCapital[', '] ' FROM Module-' module_name=NameLower
  /\\s*/-
;

Asn1Comment[noskipws]:
  /\\s*/-
  '--'
  (' ')*
  is_little_endian?='ENDIANNESS(LITTLE)'
  (' ')*
  ('[' unit=/[%A-Za-z\\d\\/\\^]+/ ']')?
  (' ')*
  (comment = ASN1CommentString)?
  '--' '\n'
  /\\s*/-
;

ASN1CommentString[noskipws]:
  (!'--' /./)+
;

NameLower[noskipws]:
  /[a-z][a-z\\d]*(-[a-z\\d]+)*/
;

NameCapital[noskipws]:
  /[A-Z][a-z\\d]*(-[a-z\\d]+)*/
;

Definitions:
  Choice | Enumerated | Sequence | SimpleDefinition
;

Enumerated[noskipws]:
  /\\s*/-
  (comment = Asn1Comment)?
  /\\s*/-
  type_name=NameCapital ' ::= ENUMERATED {' '\n'
    (enum = EnumeratedItemFirst)
    (enum *= EnumeratedItemXs)
  '}'
  /\\s*/-
;

EnumeratedItemFirst[noskipws]:
  /\\s*/-
  (comment = Asn1Comment)?
  /\\s*/-
  key=NameLower (' ' '('pos=INT')')?
  /\\s*/-
;

EnumeratedItemXs[noskipws]:
  ',' EnumeratedItemFirst
;

Asn1Type[noskipws]:
  type_name='REAL'('('begin=STRICTFLOAT ' .. ' end=STRICTFLOAT')')? |
  type_name='INTEGER'('('begin=INT'..'end=INT')')? |
  type_name='NULL' |
  type_name='BOOLEAN' |
  type_name=Asn1String |
  type_name=Array |
  type_name=NameCapital // TODO: correct to match exactly a defined typ
;

KeyTypePairFirst[noskipws]:
  /\\s*/-
  (comment=Asn1Comment)?
  /\\s*/-
  key=NameLower ' ' asn_type=Asn1Type
  /\\s*/-
  (with_components=WithComponents)?
  /\\s*/-
;

KeyTypePairXs[noskipws]:
  ',' KeyTypePairFirst
;

WithComponents[noskipws]:
  /\\s*/-
  (comment=Asn1Comment)?
  /\\s*/-
  '(WITH COMPONENTS {' '\n'
    (components = ComponentsItemFirst)
    (components *= ComponentsItemXs)
  '})'
  /\\s*/-
;

ComponentsItemFirst[noskipws]:
  /\\s*/-
  (comment=Asn1Comment)?
  /\\s*/-
  key=NameLower ' ' (
    '(' value=INT ')' |
    '(' value=STRICTFLOAT ')' |
    '(' value='TRUE' ')' |
    '(' value='FALSE' ')' |
    value=WithComponents
  )
  /\\s*/-
;

ComponentsItemXs[noskipws]:
  ','
  ComponentsItemFirst
;

Choice[noskipws]:
  /\\s*/-
  (comment = Asn1Comment)?
  /\\s*/-

  (type_name = NameCapital) ' ::= CHOICE {'
    (choice = KeyTypePairFirst)
    (choice *= KeyTypePairXs)
  '}'
  /\\s*/-
;

Sequence[noskipws]:
  /\\s*/-
  (comment=Asn1Comment)?
  /\\s*/-
  type_name=NameCapital ' ::= SEQUENCE {' '\n'
    (seq=KeyTypePairFirst)
    (seq *= KeyTypePairXs)
  '}'
  /\\s*/-
;

SimpleDefinition[noskipws]:
  /\\s*/-
  (comment=Asn1Comment)?
  /\\s*/-
  type_name=NameCapital ' ::= ' asn_type=Asn1Type
  /\\s*/-
;

Array[noskipws]:
  'SEQUENCE (SIZE ('length=INT')) OF ' asn_type=Asn1Type
;

// TODO check whether SEQUENCE OF SEQUENCE OF ... is allowed in ASN.1

Asn1String[noskipws]:
  (type_name='IA5String' | type_name='NumericString')
  ' (SIZE ('length=INT'))'
;
"""
