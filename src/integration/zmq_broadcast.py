"""
ZMQ Pub-Sub Broadcasting - Backward Compatibility Wrapper

This module re-exports all ZMQ communication utilities from skynet-common
for backward compatibility with existing code.

New code should import directly from skynet_common.communication.
"""

# Re-export everything from skynet-common for backward compatibility
from skynet_common.communication.zmq_broadcast import (
    # Data structures
    FrameData,
    DetectionData,
    VehicleState,
    ParameterUpdate,
    # Publishers
    VehicleBroadcaster,
    ActionPublisher,
    ParameterPublisher,
    VehicleStatusPublisher,
    # Subscribers
    ViewerSubscriber,
    ActionSubscriber,
    ParameterSubscriber,
)

__all__ = [
    # Data structures
    "FrameData",
    "DetectionData",
    "VehicleState",
    "ParameterUpdate",
    # Publishers
    "VehicleBroadcaster",
    "ActionPublisher",
    "ParameterPublisher",
    "VehicleStatusPublisher",
    # Subscribers
    "ViewerSubscriber",
    "ActionSubscriber",
    "ParameterSubscriber",
]
