"""
Utility modules for simulation-specific features.

Note: LaneAnalyzer has been moved to decision.lane_analyzer to better reflect
its role as vehicle-agnostic decision logic. This module maintains backwards
compatibility by re-exporting it.

Note: LKASVisualizer and LaneDepartureStatus have been moved to skynet-common
package to enable platform-independent usage. This module re-exports them
for backwards compatibility.
"""

# Re-export from decision module for backwards compatibility
from lkas.decision.lane_analyzer import LaneAnalyzer

# Re-export from skynet-common for backwards compatibility
from skynet_common.types import LaneDepartureStatus
from skynet_common.visualization import LKASVisualizer

__all__ = ['LaneAnalyzer', 'LaneDepartureStatus', 'LKASVisualizer']
