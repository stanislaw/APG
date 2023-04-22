#ifndef ASN1_PARSER_TEST_MODULE_MSG_H_INCLUDED
#define ASN1_PARSER_TEST_MODULE_MSG_H_INCLUDED

/*
This file was autogenerated from ASN.1 model.

Module test-module comment
*/

#include <stdint.h>
// Import comment used.
#include "test_simple_types1_msg.h"
#include "test_simple_types2_msg.h"

/* Type-seq-1 comment */
typedef struct
{
  // ts1 field1 comment
  uint8_t test_module_type_seq_1_field_1 : 4;
  // ts1 field2 comment
  uint8_t test_module_type_seq_1_field_2 : 4;
} __attribute__((packed)) Test_module_type_seq_1;

/* Type-seq-2 comment */
typedef struct
{
  // ts2 field1 comment
  uint8_t test_module_type_seq_2_field_1 : 4;
  // ts2 field2 comment
  uint8_t test_module_type_seq_2_field_2 : 4;
} __attribute__((packed)) Test_module_type_seq_2;

/* Test-seq comment */
typedef struct
{
  // testseq1 field1 comment
  Test_module_type_seq_1 test_module_test_seq_1_field_1;
  // testseq1 field2 comment
  Test_module_type_seq_2 test_module_test_seq_1_field_2;
} __attribute__((packed)) Test_module_test_seq;

#endif // ASN1_PARSER_TEST_MODULE_MSG_H_INCLUDED
