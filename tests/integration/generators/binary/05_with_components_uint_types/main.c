#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef __APPLE__
#include <libkern/OSByteOrder.h>

#define htobe16(x) OSSwapHostToBigInt16(x)
#define htole16(x) OSSwapHostToLittleInt16(x)
#define be16toh(x) OSSwapBigToHostInt16(x)
#define le16toh(x) OSSwapLittleToHostInt16(x)

#define htobe32(x) OSSwapHostToBigInt32(x)
#define htole32(x) OSSwapHostToLittleInt32(x)
#define be32toh(x) OSSwapBigToHostInt32(x)
#define le32toh(x) OSSwapLittleToHostInt32(x)

#define htobe64(x) OSSwapHostToBigInt64(x)
#define htole64(x) OSSwapHostToLittleInt64(x)
#define be64toh(x) OSSwapBigToHostInt64(x)
#define le64toh(x) OSSwapLittleToHostInt64(x)
#endif

#include "sample_module.h"

const char *path = "output/binary/sample_packet.bin";

int main() {
  uint32_t size_sample_packet = sizeof(Sample_packet);
  Sample_packet *sample_packet = malloc(size_sample_packet);
  FILE * readfile = fopen(path, "rb");
  if (readfile != NULL) {
    fread(sample_packet, size_sample_packet, 1, readfile);
    fclose(readfile);
  }

  With_component_packet sample_packet_with_component = sample_packet->sample_packet_with_component;

  sample_packet_with_component.with_component_packet_number_2
    = le16toh(sample_packet_with_component.with_component_packet_number_2);
  sample_packet_with_component.with_component_packet_number_3
    = le32toh(sample_packet_with_component.with_component_packet_number_3);
  sample_packet_with_component.with_component_packet_number_4
    = le64toh(sample_packet_with_component.with_component_packet_number_4);

  assert(
    sample_packet->sample_packet_with_component.with_component_packet_number_1 == 23
  );

  assert(
    sample_packet->sample_packet_with_component.with_component_packet_number_2 == 300
  );

  assert(
    sample_packet->sample_packet_with_component.with_component_packet_number_3 == 66000
  );

  assert(
    sample_packet->sample_packet_with_component.with_component_packet_number_4 == 4300000000
  );

  free(sample_packet);

  return 0;
}