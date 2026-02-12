"""
ProjectSpark CLI Runner
========================
Entry point for running sensitivity sweeps from the command line.

Usage:
    python -m cli.runner --model meta-llama/Llama-3-8B --benchmark mmlu --mode demo --output results.json
"""

import argparse
import sys
import os

from .prompt_architectures import ALL_ARCHITECTURES, ARCHITECTURE_MAP
from .sweep_engine import SensitivitySweep
from .result_parser import results_summary_table


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project-spark",
        description="⚡ ProjectSpark — AI Eval Harness Benchmarker CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m cli.runner --model meta-llama/Llama-3-8B --mode demo
  python -m cli.runner --model meta-llama/Llama-3-8B --mode demo --output results.json
  python -m cli.runner --model gpt-4 --mode demo --format csv --output results.csv
  python -m cli.runner --model meta-llama/Llama-3-8B --mode live
        """,
    )

    parser.add_argument(
        "--model", "-m",
        type=str,
        default="meta-llama/Llama-3-8B",
        help="Model name/path (default: meta-llama/Llama-3-8B)",
    )
    parser.add_argument(
        "--benchmark", "-b",
        type=str,
        default="mmlu",
        choices=["mmlu"],
        help="Benchmark to evaluate (default: mmlu)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="demo",
        choices=["demo", "live"],
        help="Execution mode: 'demo' for simulated results, 'live' for real evaluation (default: demo)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output file path (default: print to stdout only)",
    )
    parser.add_argument(
        "--format", "-f",
        type=str,
        default="json",
        choices=["json", "csv"],
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--architectures", "-a",
        type=str,
        nargs="+",
        default=None,
        help=f"Architectures to test (default: all). Options: {list(ARCHITECTURE_MAP.keys())}",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress terminal output",
    )

    return parser


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)

    # Select architectures
    if args.architectures:
        archs = []
        for key in args.architectures:
            if key not in ARCHITECTURE_MAP:
                print(f"✗ Unknown architecture: {key}")
                print(f"  Available: {list(ARCHITECTURE_MAP.keys())}")
                sys.exit(1)
            archs.append(ARCHITECTURE_MAP[key])
    else:
        archs = ALL_ARCHITECTURES

    if not args.quiet:
        print()
        print("⚡ ProjectSpark — AI Eval Harness Benchmarker")
        print("=" * 50)
        print(f"  Model:       {args.model}")
        print(f"  Benchmark:   {args.benchmark}")
        print(f"  Mode:        {args.mode}")
        print(f"  Architectures: {len(archs)}")
        print("=" * 50)
        print()

    # Run sweep
    sweep = SensitivitySweep(
        model_name=args.model,
        architectures=archs,
        benchmark=args.benchmark,
        mode=args.mode,
    )

    if not args.quiet:
        print("Running sensitivity sweep...")
        for arch in archs:
            print(f"  ▸ {arch.name} ({arch.key})")

    results = sweep.run_sweep()

    # Display results
    if not args.quiet:
        print()
        print(results_summary_table(results.to_dict()))
        print()

    # Export
    if args.output:
        os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
        if args.format == "csv":
            sweep.export_csv(args.output)
        else:
            sweep.export_json(args.output)

    return results


if __name__ == "__main__":
    main()
