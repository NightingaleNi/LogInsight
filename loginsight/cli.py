import argparse
import sys
from .core import scan_logs, summarize_buckets
from .anomaly import detect_spikes


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="loginsight", description="Quick insights from log files")
    sub = p.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Scan logs for pattern counts")
    scan.add_argument("path", help="Path to log file")
    scan.add_argument("--pattern", default=None, help="Substring to match (case sensitive)")
    scan.add_argument("--limit", type=int, default=0, help="Max lines to process (0=all)")
    scan.add_argument("--json", action="store_true", help="Output JSON")
    scan.add_argument("--top", type=int, default=10, help="Number of top messages to show")

    summ = sub.add_parser("summary", help="Summarize counts by time bucket")
    summ.add_argument("path", help="Path to log file")
    summ.add_argument("--bucket", choices=["minute", "hour", "day"], default="hour")
    summ.add_argument("--limit", type=int, default=0)
    summ.add_argument("--json", action="store_true")
    summ.add_argument("--spikes", action="store_true", help="Highlight spikes via simple z-score")

    return p


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    args = _build_parser().parse_args(argv)

    if args.cmd == "scan":
        res = scan_logs(args.path, pattern=args.pattern, limit=args.limit)
        if "top_messages" in res and args.top:
            res["top_messages"] = dict(list(res["top_messages"].items())[: args.top])
    elif args.cmd == "summary":
        res = summarize_buckets(args.path, bucket=args.bucket, limit=args.limit)
        if args.spikes:
            res["spikes"] = detect_spikes(res.get("counts", {}))
    else:
        raise SystemExit(2)

    if getattr(args, "json", False):
        import json

        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        for k, v in res.items():
            print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
