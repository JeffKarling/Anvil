#include <tbb_transform/tbb_transform.hpp>
#include <journal/journal.hpp>
#include <oneapi/tbb/parallel_for.h>

namespace anvil::tbb_transform {

auto parallel_double(std::span<int> numbers) noexcept -> bool {
  return parallel_scale(numbers, 2);
}

auto parallel_scale(std::span<int> numbers, int factor) noexcept -> bool {
  if (numbers.empty()) {
    return true;
  }

  namespace jrn = anvil::journal;
  try {
    oneapi::tbb::parallel_for(
        std::size_t{0}, numbers.size(), [numbers, factor](std::size_t i) noexcept {
          numbers[i] *= factor;
        });
    return true;
  } catch (...) {
    return jrn::catch_boundary_exception(k_catalog.k_boundary_fault);
  }
}

} // namespace anvil::tbb_transform
