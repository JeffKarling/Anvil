#include <journal/journal.hpp>
#include <journal_signal_adapter/journal_signal_adapter.hpp>

int main() {
  namespace jrn = anvil::journal;
  namespace sig = anvil::journal_signal_adapter;

  auto adapter = sig::signal_adapter::create();
  if (!adapter) {
    jrn::log(jrn::severity::error, jrn::message{"Failed to start journal signal adapter"});
    return 1;
  }

  jrn::log(jrn::severity::info, jrn::message{"Anvil runtime initialized"});
  if (!jrn::flush()) {
    return 1;
  }
  return 0;
}
