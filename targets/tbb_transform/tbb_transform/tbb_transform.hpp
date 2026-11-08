#pragma once

#include <cstddef>
#include <journal/journal.hpp>
#include <span>

namespace anvil::tbb_transform {

struct catalog {
  anvil::journal::catalog_entry k_boundary_fault{
      .message_id = "30499866b3914a1c98baac6171bd36bc",
      .component = "tbb_transform",
      .summary = "Unhandled fault caught at tbb_transform boundary firewall"};
};

inline constexpr catalog k_catalog{};

[[nodiscard]] auto parallel_double(std::span<int> numbers) noexcept -> bool;

[[nodiscard]] auto parallel_scale(std::span<int> numbers, int factor) noexcept -> bool;

} // namespace anvil::tbb_transform
