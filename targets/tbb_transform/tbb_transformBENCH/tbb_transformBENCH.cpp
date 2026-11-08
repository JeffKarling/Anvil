#include <cstddef>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <numeric>
#include <perf_scope/perf_scope.hpp>
#include <system_error>
#include <tbb_transform/tbb_transform.hpp>
#include <vector>

int main() {
  namespace ps = anvil::perf_scope;

  constexpr std::size_t k_workload_size = 5'000U;
  std::vector<int> workload(k_workload_size);
  std::iota(workload.begin(), workload.end(), 1);

  auto const current_metrics = ps::measure_workload(100U, [&workload]() {
    (void)anvil::tbb_transform::parallel_scale(workload, 2);
  });

  ps::score_baseline default_birth{};
  default_birth.component = "tbb_transform";
  default_birth.birth_metrics = current_metrics;

  std::filesystem::path const baseline_path = COMPONENT_BASELINE_PATH;
  auto const baseline = ps::load_or_create_baseline(baseline_path, default_birth);
  auto const evaluation = ps::evaluate_performance(baseline, current_metrics);
  auto const report = ps::format_performance_report(baseline, evaluation);

  std::cout << report;

  std::filesystem::path const report_path = COMPONENT_REPORT_PATH;
  if (report_path.has_parent_path()) {
    std::error_code ec;
    std::filesystem::create_directories(report_path.parent_path(), ec);
  }
  std::ofstream out(report_path, std::ios::out | std::ios::trunc);
  if (out.is_open()) {
    out << report;
  }
  return 0;
}
