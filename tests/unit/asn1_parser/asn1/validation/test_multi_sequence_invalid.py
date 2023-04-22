import pytest

from asn1_parser.asn1.asn1_bundle_builder import ASN1BundleBuilder


# pylint: disable=line-too-long
# line-too-long warning shows up for the asn modules only
# only other way to disable would be concatenating multiple strings
# to form the modules, but that degrades readability
from asn1_parser.asn1.validation.asn1_bundle_validator import (
    ASN1ConsistencyError,
)


def test_sequence_import_with_components_component_not_found():
    input_asn = [
        """
Module-sandbox-hk-pc DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  IMPORTS Ccsds-primary-header, Secondary-header FROM Module-tmtc-header;

  Uint64-t ::= INTEGER(0..18446744073709551615)

  Percent ::= REAL(0.00 .. 100.00)
  Load ::= REAL(0.00 .. 30.00)

  Sandbox-hk-pc-t ::= SEQUENCE {
    primary-header Ccsds-primary-header
      (WITH COMPONENTS {
        packet-version-number (0),
        packet-identification (WITH COMPONENTS {
          packet-type-is-cmd (FALSE),
          sec-hdr-flag-is-present (TRUE),
          application-process-identifier (153)
        })
      }),
    secondary-header Secondary-header,
    payload Payload-sandbox-hk-pc-t
  }

  Payload-sandbox-hk-pc-t ::= SEQUENCE {
    cpu Percent,
    load1 Load,
    load5 Load,
    load15 Load,
    total-ram Uint64-t,
    free-ram Uint64-t,
    free-swap Uint64-t
  }

END
""".lstrip(),
        """
Module-tmtc-header DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  Uint16-t ::= INTEGER(0..65535)
  Uint32-t ::= INTEGER(0..4294967295)

  Ccsds-primary-header ::= SEQUENCE {
    packet-identification Packet-identification,
    packet-sequence-control Packet-sequence-control,
    packet-data-length Uint16-t
  }

  Packet-identification ::= SEQUENCE {
    packet-type-is-cmd BOOLEAN,
    sec-hdr-flag-is-present BOOLEAN,
    application-process-identifier INTEGER(0..2047)
  }

  Packet-sequence-control ::= SEQUENCE {
    sequence-flags Sequence-flag,
    packet-sequence-count INTEGER(0..16383)
  }

  Sequence-flag ::= ENUMERATED {
    continuation-packet-in-sequence (0),
    first-packet-in-sequence (1),
    last-packet-in-sequence (2),
    complete-packet (3)
  }

  Secondary-header ::= SEQUENCE {
    seconds Uint32-t,
    subsecs Uint16-t
  }

END
""".lstrip(),  # noqa: E501
    ]

    with pytest.raises(ASN1ConsistencyError) as key_error:
        ASN1BundleBuilder.build_from_texts(input_asn)

    assert (
        key_error.value.args[0]
        == "'packet-version-number' in 'Sandbox-hk-pc-t' is not a valid key"
    )


def test_sequence_import_with_components_sub_component_not_found():
    input_asn = [
        """
Module-sandbox-hk-pc DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  IMPORTS Ccsds-primary-header, Secondary-header FROM Module-tmtc-header;

  Uint64-t ::= INTEGER(0..18446744073709551615)

  Percent ::= REAL(0.00 .. 100.00)
  Load ::= REAL(0.00 .. 30.00)

  Sandbox-hk-pc-t ::= SEQUENCE {
    primary-header Ccsds-primary-header
      (WITH COMPONENTS {
        packet-version-number (0),
        packet-identification (WITH COMPONENTS {
          packet-type-is-cmd (FALSE),
          sec-hdr-flag-is-present (TRUE),
          application-process-identifier (153)
        })
      }),
    secondary-header Secondary-header,
    payload Payload-sandbox-hk-pc-t
  }

  Payload-sandbox-hk-pc-t ::= SEQUENCE {
    cpu Percent,
    load1 Load,
    load5 Load,
    load15 Load,
    total-ram Uint64-t,
    free-ram Uint64-t,
    free-swap Uint64-t
  }

END
""".lstrip(),
        """
Module-tmtc-header DEFINITIONS AUTOMATIC TAGS ::= BEGIN

  Uint16-t ::= INTEGER(0..65535)
  Uint32-t ::= INTEGER(0..4294967295)

  Ccsds-primary-header ::= SEQUENCE {
    packet-version-number INTEGER(0..7),
    packet-identification Packet-identification,
    packet-sequence-control Packet-sequence-control,
    packet-data-length Uint16-t
  }

  Packet-identification ::= SEQUENCE {
    sec-hdr-flag-is-present BOOLEAN,
    application-process-identifier INTEGER(0..2047)
  }

  Packet-sequence-control ::= SEQUENCE {
    sequence-flags Sequence-flag,
    packet-sequence-count INTEGER(0..16383)
  }

  Sequence-flag ::= ENUMERATED {
    continuation-packet-in-sequence (0),
    first-packet-in-sequence (1),
    last-packet-in-sequence (2),
    complete-packet (3)
  }

  Secondary-header ::= SEQUENCE {
    seconds Uint32-t,
    subsecs Uint16-t
  }

END
""".lstrip(),  # noqa: E501
    ]

    with pytest.raises(ASN1ConsistencyError) as key_error:
        ASN1BundleBuilder.build_from_texts(input_asn)

    assert (
        key_error.value.args[0]
        == "'packet-type-is-cmd' in 'Sandbox-hk-pc-t' is not a valid key"
    )
