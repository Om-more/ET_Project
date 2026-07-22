from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mapao.src.episode_builder.builder import build_episode_summary, group_events_into_episodes
from mapao.src.normalization.parser import load_json_events
from mapao.src.ttp_mapper.mapper import select_best_ttp
from mapao.src.predictor.risk import build_risk_verdict
from mapao.src.orchestrator.engine import enact_risk_verdict


def load_audit_log() -> list[dict[str, str]]:
    path = Path(__file__).resolve().parents[2] / "data" / "processed" / "audit_trail.json"
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    st.set_page_config(page_title="MAPAO Dashboard", layout="wide")
    st.title("MAPAO Cyber Attack Episode Dashboard")

    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        st.header("Event Feed")
        sample_file = st.text_input("Path to raw JSON events", "data/raw/sample_events.json")
        if st.button("Load Events"):
            try:
                events = load_json_events(Path(sample_file))
                episodes = group_events_into_episodes(events)
                st.success(f"Loaded {len(events)} events and built {len(episodes)} episodes")
                selected = st.selectbox("Select Attack Episode", episodes, format_func=lambda e: f"{e.episode_id}: {e.entity_key} ({e.event_count})")
                st.write(selected)

                if selected:
                    st.subheader("Episode Events")
                    for event in selected.events:
                        st.json(event.dict())

                    summary = build_episode_summary(selected)
                    ttp_match = select_best_ttp(summary)
                    verdict = build_risk_verdict(
                        episode_id=selected.episode_id,
                        ttp_match=ttp_match,
                        predicted_next_step="Credential Dumping via Mimikatz",
                        asset_criticality=5.0,
                        blast_radius=3.5,
                        recommended_action="isolate_host",
                    )

                    with col2:
                        st.header("AI Reasoning")
                        st.metric("Matched TTP", f"{ttp_match.matched_ttp_id} - {ttp_match.matched_ttp_name}")
                        st.metric("Confidence", f"{ttp_match.ttp_confidence:.2f}")
                        st.markdown("**Episode Summary**")
                        st.code(summary)
                        st.markdown("**TTP Description**")
                        st.write(ttp_match.description)
                        st.markdown("**Risk Verdict**")
                        st.json(verdict.dict())

                    with col3:
                        st.header("SOAR Control")
                        st.markdown(f"**Gate Decision:** {verdict.gate_decision}")
                        if verdict.gate_decision == "HUMAN_APPROVAL":
                            if st.button("Approve Action"):
                                st.write(enact_risk_verdict(verdict, entity_identifier=selected.entity_key.split(":", 1)[-1]))
                            if st.button("Reject Action"):
                                st.warning("Action rejected by analyst")
                        else:
                            st.write(enact_risk_verdict(verdict, entity_identifier=selected.entity_key.split(":", 1)[-1]))

            except Exception as exc:
                st.error(str(exc))

    with col3:
        st.header("Audit Trail")
        audit_rows = load_audit_log()
        st.write(audit_rows)


if __name__ == "__main__":
    main()
