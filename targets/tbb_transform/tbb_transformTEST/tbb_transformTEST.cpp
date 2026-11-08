#include <cstddef>
#include <gtest/gtest.h>
#include <numeric>
#include <tbb_transform/tbb_transform.hpp>
#include <vector>

namespace {

static_assert(anvil::journal::is_valid_catalog(anvil::tbb_transform::k_catalog));

TEST(TbbTransformTest, ParallelDoubleScalesArrayValues) {
  std::vector<int> numbers{1, 2, 3, 4, 5};
  EXPECT_TRUE(anvil::tbb_transform::parallel_double(numbers));

  std::vector<int> const expected{2, 4, 6, 8, 10};
  EXPECT_EQ(numbers, expected);
}

TEST(TbbTransformTest, ParallelDoubleHandlesEmptySpan) {
  std::vector<int> empty{};
  EXPECT_TRUE(anvil::tbb_transform::parallel_double(empty));
  EXPECT_TRUE(empty.empty());
}

TEST(TbbTransformTest, ParallelScaleHandlesLargeWorkload) {
  constexpr std::size_t k_size = 50'000U;
  std::vector<int> numbers(k_size);
  std::iota(numbers.begin(), numbers.end(), 0);

  EXPECT_TRUE(anvil::tbb_transform::parallel_scale(numbers, 3));

  for (std::size_t i = 0; i < k_size; ++i) {
    ASSERT_EQ(numbers[i], static_cast<int>(i) * 3);
  }
}

TEST(TbbTransformTest, ParallelScaleHandlesNegativeMultiplier) {
  std::vector<int> numbers{10, -20, 30};
  EXPECT_TRUE(anvil::tbb_transform::parallel_scale(numbers, -2));

  std::vector<int> const expected{-20, 40, -60};
  EXPECT_EQ(numbers, expected);
}

} // namespace
