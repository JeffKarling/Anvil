#include <cstddef>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <item_store/item_store.hpp>
#include <perf_scope/perf_scope.hpp>
#include <system_error>
#include <vector>

int main() {
  namespace ps = anvil::perf_scope;

  std::vector<anvil::item_store::item_record> const records{
      {.id = "sensor_001", .name = "Temperature Probe", .value = 23.4},
      {.id = "sensor_002", .name = "Pressure Transducer", .value = 1013.25},
      {.id = "sensor_003", .name = "Humidity Gauge", .value = 45.8},
  };

  std::vector<std::byte> payload;
  (void)anvil::item_store::serialize_records(records, payload);

  auto const current_metrics = ps::measure_workload(1000U, [&payload, &records]() {
    std::vector<std::byte> temp;
    (void)anvil::item_store::serialize_records(records, temp);
    (void)anvil::item_store::deserialize_records(payload);
  });

  ps::score_baseline default_birth{};
  default_birth.component = "item_store";
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
