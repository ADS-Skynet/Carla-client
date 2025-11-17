#!/usr/bin/env python3
"""
Distributed Lane Keeping System - CARLA Client

Features:
- Shared memory IPC with detection server (ultra-low latency)
- ZMQ broadcasting for remote viewers
- Clean architecture with dependency injection

Usage:
    simulation --broadcast

Note: This has been refactored to use SimulationOrchestrator for clean architecture.
"""

import argparse
import sys

from skynet_common.config import ConfigManager
from simulation.orchestrator import SimulationOrchestrator, SimulationConfig


def parse_arguments(config) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        config: System configuration for defaults

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Distributed Lane Keeping System - CARLA Client"
    )

    # System options
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file (default: <project-root>/config.yaml)",
    )
    parser.add_argument(
        "--host", type=str, default=None, help="CARLA server host (overrides config)"
    )
    parser.add_argument(
        "--port", type=int, default=None, help="CARLA server port (overrides config)"
    )
    parser.add_argument("--spawn-point", type=int, default=None)

    # Shared memory detection (default and only IPC method)
    parser.add_argument(
        "--image-shm-name",
        type=str,
        default=config.communication.image_shm_name,
        help=f"Shared memory name for camera images (default: {config.communication.image_shm_name})",
    )
    parser.add_argument(
        "--detection-shm-name",
        type=str,
        default=config.communication.detection_shm_name,
        help=f"Shared memory name for detection results (default: {config.communication.detection_shm_name})",
    )
    parser.add_argument(
        "--detector-timeout",
        type=int,
        default=1000,  # Module-specific: 1000ms
        help="Detection timeout in milliseconds (default: 1000)",
    )

    # Other options
    parser.add_argument("--autopilot", action="store_true")
    parser.add_argument(
        "--no-sync", action="store_true", help="Disable synchronous mode"
    )
    parser.add_argument(
        "--base-throttle",
        type=float,
        default=config.throttle_policy.base,
        help=f"Base throttle during initialization/failures (default: {config.throttle_policy.base})",
    )
    parser.add_argument(
        "--warmup-frames",
        type=int,
        default=50,  # Module-specific: 50 frames
        help="Frames to use base throttle before full control (default: 50)",
    )
    parser.add_argument(
        "--latency",
        action="store_true",
        help="Enable latency tracking and reporting (adds overhead)",
    )

    parser.add_argument(
        "--control-shm-name",
        type=str,
        default=config.communication.control_shm_name,
        help=f"Shared memory name for control commands (default: {config.communication.control_shm_name})",
    )

    # ZMQ Broadcasting options (legacy - always enabled now)
    parser.add_argument(
        "--broadcast",
        action="store_true",
        help="(Legacy flag - broadcasting is now always enabled for viewer support)",
    )
    parser.add_argument(
        "--broadcast-url",
        type=str,
        default=f"tcp://*:{config.communication.zmq_broadcast_port}",
        help=f"ZMQ URL for broadcasting vehicle data (default: tcp://*:{config.communication.zmq_broadcast_port})",
    )
    parser.add_argument(
        "--action-url",
        type=str,
        default=f"tcp://*:{config.communication.zmq_action_port}",
        help=f"ZMQ URL for receiving actions (default: tcp://*:{config.communication.zmq_action_port})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output (lane status, steering info)",
    )

    return parser.parse_args()


def print_banner(config: SimulationConfig, system_config: object):
    """
    Print startup banner with configuration.

    Args:
        config: Simulation configuration
        system_config: System-wide configuration
    """
    print("\n" + "=" * 60)
    print("DISTRIBUTED LANE KEEPING SYSTEM")
    print("=" * 60)
    print(f"CARLA Server: {config.carla_host}:{config.carla_port}")

    print(f"SHARED MEMORY TABLE")
    print(f"  Image: {config.image_shm_name}")
    print(f"  Detection: {config.detection_shm_name}")
    print(f"  Control: {config.control_shm_name}")
    print(f"  Timeout: {config.detector_timeout}ms")

    print(f"Camera: {system_config.camera.width}x{system_config.camera.height}")

    # ZMQ Broadcasting
    if config.enable_broadcast:
        print(f"ZMQ Broadcasting: ENABLED")
        print(f"  Broadcast URL: {config.broadcast_url}")
        print(f"  Action URL: {config.action_url}")
    else:
        print(f"ZMQ Broadcasting: DISABLED (use --broadcast to enable)")

    print("=" * 60)


def main():
    """Main entry point for distributed CARLA client with ZMQ broadcasting."""
    # Load configuration first (for defaults)
    print("\nLoading configuration...")
    # Check if --config is in sys.argv
    config_path = None
    for i, arg in enumerate(sys.argv):
        if arg == "--config" and i + 1 < len(sys.argv):
            config_path = sys.argv[i + 1]
            break
    system_config = ConfigManager.load(config_path)
    print(f"✓ Configuration loaded")

    # Parse arguments with config defaults
    args = parse_arguments(system_config)

    # Reload config if a different path was specified
    if args.config and args.config != config_path:
        system_config = ConfigManager.load(args.config)

    # Determine CARLA connection params
    carla_host = args.host if args.host else system_config.carla.host
    carla_port = args.port if args.port else system_config.carla.port

    # Create simulation configuration
    sim_config = SimulationConfig(
        carla_host=carla_host,
        carla_port=carla_port,
        spawn_point=args.spawn_point,
        image_shm_name=args.image_shm_name,
        detection_shm_name=args.detection_shm_name,
        detector_timeout=args.detector_timeout,
        enable_broadcast=args.broadcast,
        broadcast_url=args.broadcast_url,
        action_url=args.action_url,
        enable_autopilot=args.autopilot,
        enable_sync_mode=not args.no_sync,
        base_throttle=args.base_throttle,
        warmup_frames=args.warmup_frames,
        enable_latency_tracking=args.latency,
        control_shm_name=args.control_shm_name,
        verbose=args.verbose,
    )

    # Print banner
    print_banner(sim_config, system_config)

    # Create orchestrator
    orchestrator = SimulationOrchestrator(sim_config, system_config, verbose=args.verbose)

    # Setup all subsystems
    if not orchestrator.setup():
        print("\n✗ Setup failed")
        return 1

    # Run main loop
    orchestrator.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
