/* SPDX-License-Identifier: BSD-3-Clause
 * Copyright(c) 2021 Intel Corporation
 */

#pragma once

#include "kvdk/namespace.hpp"
#include "structures.hpp"

namespace KVDK_NAMESPACE {
// Free pmem blocks
struct SpaceEntry {
  uint64_t offset = 0;

  SpaceEntry() = default;
  explicit SpaceEntry(uint64_t bo) : offset(bo) {}
};

struct SizedSpaceEntry {
  SizedSpaceEntry() = default;
  SizedSpaceEntry(uint64_t offset, uint32_t size)
      : space_entry(offset), size(size) {}
  SpaceEntry space_entry;
  uint32_t size = 0;
};

class Allocator {
public:
  // TODO: do not use space entry
  virtual SizedSpaceEntry Allocate(uint64_t size) = 0;
  virtual void Free(const SizedSpaceEntry &entry) = 0;
};
} // namespace KVDK_NAMESPACE