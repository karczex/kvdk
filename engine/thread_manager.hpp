/* SPDX-License-Identifier: BSD-3-Clause
 * Copyright(c) 2021 Intel Corporation
 */

#pragma once

#include <atomic>
#include <unordered_set>

#include "kvdk/engine.hpp"
#include "utils.hpp"

namespace KVDK_NAMESPACE {

class ThreadManager;

struct Thread {
public:
  Thread() : id(-1), thread_manager(nullptr) {}
  ~Thread();
  int id;
  std::shared_ptr<ThreadManager> thread_manager;
};

class ThreadManager : public std::enable_shared_from_this<ThreadManager> {
public:
  ThreadManager(uint32_t max_threads) : max_threads_(max_threads), ids_(0) {}
  Status MaybeInitThread(Thread &t);

  void Release(const Thread &t);

private:
  std::atomic<uint32_t> ids_;
  std::unordered_set<uint32_t> usable_id_;
  uint32_t max_threads_;
  SpinMutex spin_;
};

extern thread_local Thread write_thread;

} // namespace KVDK_NAMESPACE