#include <item_store/item_store.hpp>
#include <item_proto/item_proto.pb.h>
#include <journal/journal.hpp>

namespace anvil::item_store {

auto serialize_records(
    std::span<const item_record> records,
    std::vector<std::byte>& out_payload) noexcept -> bool {
  namespace jrn = anvil::journal;
  try {
    anvil::item_proto::item_database proto_db;
    for (const auto& rec : records) {
      auto* item = proto_db.add_items();
      item->set_id(rec.id);
      item->set_name(rec.name);
      item->set_value(rec.value);
    }

    std::size_t const byte_size = proto_db.ByteSizeLong();
    out_payload.resize(byte_size);
    if (!proto_db.SerializeToArray(out_payload.data(), static_cast<int>(byte_size))) {
      return false;
    }
    return true;
  } catch (...) {
    return jrn::catch_boundary_exception(k_catalog.k_boundary_fault);
  }
}

auto deserialize_records(
    std::span<const std::byte> in_payload) noexcept -> std::optional<std::vector<item_record>> {
  namespace jrn = anvil::journal;
  try {
    anvil::item_proto::item_database proto_db;
    if (!proto_db.ParseFromArray(in_payload.data(), static_cast<int>(in_payload.size()))) {
      return std::nullopt;
    }

    std::vector<item_record> result;
    result.reserve(static_cast<std::size_t>(proto_db.items_size()));
    for (const auto& item : proto_db.items()) {
      result.push_back(item_record{
          .id = item.id(),
          .name = item.name(),
          .value = item.value(),
      });
    }
    return result;
  } catch (...) {
    (void)jrn::catch_boundary_exception(k_catalog.k_boundary_fault);
    return std::nullopt;
  }
}

} // namespace anvil::item_store
