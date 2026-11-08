#include <gtest/gtest.h>
#include <item_proto/item_proto.pb.h>

namespace {

TEST(ItemProtoTest, InstantiatesGeneratedSchemaMessages) {
  anvil::item_proto::item_record record;
  record.set_id("item_101");
  record.set_name("Telemetry Node");
  record.set_value(99.5);

  EXPECT_EQ(record.id(), "item_101");
  EXPECT_EQ(record.name(), "Telemetry Node");
  EXPECT_DOUBLE_EQ(record.value(), 99.5);

  anvil::item_proto::item_database db;
  auto* item = db.add_items();
  *item = record;

  EXPECT_EQ(db.items_size(), 1);
  EXPECT_EQ(db.items(0).id(), "item_101");
}

} // namespace
