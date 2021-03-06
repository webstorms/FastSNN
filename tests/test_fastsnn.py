import torch
import torch.nn as nn

from fastsnn.models import LinearModel
from fastsnn.layers import LinearLIFNeurons, LinearFastLIFNeurons


def test_linear_layers():
    t_len = 500
    n_in = 100
    n_out = 100

    van_snn = LinearLIFNeurons(n_in, n_out, deactivate_reset=True, single_spike=True)
    fast_snn = LinearFastLIFNeurons(t_len, n_in, n_out)
    fast_snn.pre_spikes_to_current.weight = van_snn.pre_spikes_to_current.weight
    fast_snn.pre_spikes_to_current.bias = van_snn.pre_spikes_to_current.bias

    pre_spikes = torch.ones(20, n_in, t_len)
    van_spikes, van_mem = van_snn(pre_spikes)
    fast_spikes, fast_mem = fast_snn(pre_spikes)
    assert (van_spikes.long() ^ fast_spikes.long()).sum() == 0


def test_models():
    t_len = 10

    van_model = LinearModel(t_len=t_len, n_in=40, n_out=10, n_hidden=100, n_layers=2, fast_layer=False, skip_connections=True, bias=0.0, hidden_beta=0.9, readout_beta=0.9, single_spike=True)
    fast_model = LinearModel(t_len=t_len, n_in=40, n_out=10, n_hidden=100, n_layers=2, fast_layer=True, skip_connections=True, bias=0.0, hidden_beta=0.9, readout_beta=0.9)

    for van_layer, fast_layer in zip(van_model._layers, fast_model._layers):
        fast_layer.pre_spikes_to_current.weight = nn.Parameter(van_layer.pre_spikes_to_current.weight)
    fast_layer.pre_spikes_to_current.bias = van_layer.pre_spikes_to_current.bias

    fast_model._readout_layer.pre_spikes_to_current.weight = nn.Parameter(van_model._readout_layer.pre_spikes_to_current.weight)
    fast_model._readout_layer.pre_spikes_to_current.bias = van_model._readout_layer.pre_spikes_to_current.bias

    foo_input = torch.rand(1, 40, t_len)

    van_out, van_spike_history, van_mem_history = van_model(foo_input)
    fast_out, fast_spike_history, fast_mem_history = fast_model(foo_input)

    assert ((van_out - fast_out).abs() < 1e7).all().item()
