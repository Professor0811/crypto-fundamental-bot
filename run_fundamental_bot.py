# ==============================================================================
# RUN FUNDAMENTAL BOT: Main Asynchronous Orchestrator Loop
# ==============================================================================

import time
import sys
import config_fundamental as cfg
import research_brain as brain

def main_loop():
    print("==================================================")
    print(" 🧠 FUNDAMENTAL RESEARCH & MACRO BIAS BOT ONLINE 🧠 ")
    print("==================================================")
    print(f"Polling intervals:")
    print(f" • Sentiment Check     : every {cfg.SENTIMENT_POLL_INTERVAL}s")
    print(f" • Macro Calendar Scan : every {cfg.MACRO_CALENDAR_POLL_INTERVAL}s")
    print(f" • Derivatives Check   : every {cfg.FUNDING_RATE_POLL_INTERVAL}s")
    print(f" • Synthesis Loop      : every {cfg.SYNTHESIS_INTERVAL}s")
    print("--------------------------------------------------\n")

    try:
        while True:
            start_time = time.time()
            
            # Run Research Brain synthesis & update IPC bridge JSON
            res = brain.calculate_composite_bias()
            
            timestamp_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(res['timestamp']))
            print(f"[{timestamp_str}] Synthesized Composite Score: {res['composite_score']:+.1f} | Bias: {res['bias_label']} | Freeze: {res['is_news_freeze']}")

            # Sleep until next synthesis interval
            elapsed = time.time() - start_time
            sleep_time = max(5.0, cfg.SYNTHESIS_INTERVAL - elapsed)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[Fundamental Bot] Stopped manually by user. Stay safe out there!")
        sys.exit(0)

if __name__ == "__main__":
    main_loop()