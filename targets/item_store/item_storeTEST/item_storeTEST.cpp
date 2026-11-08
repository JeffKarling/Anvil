#include <array>
#include <cstddef>
#include <gtest/gtest.h>
#include <item_store/item_store.hpp>
#include <vector>

namespace {

static_assert(anvil::journal::is_valid_catalog(anvil::item_store::k_catalog));

TEST(ItemStoreTest, RoundTripSerializationPreservesRecords) {
  std::vector<anvil::item_store::item_record> const original{
      {.id = "item_1", .name = "Alpha Sensor", .value = 42.5},
      {.id = "item_2", .name = "Beta Actuator", .value = -100.25},
  };

  std::vector<std::byte> payload;
  EXPECT_TRUE(anvil::item_store::serialize_records(original, payload));
  EXPECT_FALSE(payload.empty());

  auto const restored = anvil::item_store::deserialize_records(payload);
  ASSERT_TRUE(restored.has_value());
  EXPECT_EQ(restored.value(), original);
}

TEST(ItemStoreTest, HandlesEmptyRecordList) {
  std::vector<anvil::item_store::item_record> const empty{};
  std::vector<std::byte> payload;

  EXPECT_TRUE(anvil::item_store::serialize_records(empty, payload));

  auto const restored = anvil::item_store::deserialize_records(payload);
  ASSERT_TRUE(restored.has_value());
  EXPECT_TRUE(restored.value().empty());
}

TEST(ItemStoreTest, RejectsCorruptedPayloadGracefully) {
  std::array<std::byte, 16U> const garbage{
      std::byte{0xFF}, std::byte{0xFE}, std::byte{0xFD}, std::byte{0xFC},
  };

  auto const restored = anvil::item_store::deserialize_records(garbage);
  EXPECT_FALSE(restored.has_value());
}

} // namespace
