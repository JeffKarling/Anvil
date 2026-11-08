#pragma once

#include <cstddef>
#include <journal/journal.hpp>
#include <optional>
#include <span>
#include <string>
#include <vector>

namespace anvil::item_store {

struct catalog {
  anvil::journal::catalog_entry k_boundary_fault{
      .message_id = "d4a1b938a84a4cf995125df45d003ae2",
      .component = "item_store",
      .summary = "Unhandled fault caught at item_store boundary firewall"};
};

inline constexpr catalog k_catalog{};

struct item_record {
  std::string id;
  std::string name;
  double value{0.0};

  auto operator==(const item_record&) const noexcept -> bool = default;
};

[[nodiscard]] auto serialize_records(
    std::span<const item_record> records,
    std::vector<std::byte>& out_payload) noexcept -> bool;

[[nodiscard]] auto deserialize_records(
    std::span<const std::byte> in_payload) noexcept -> std::optional<std::vector<item_record>>;

} // namespace anvil::item_store
