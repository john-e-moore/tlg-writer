Phase 0 placeholder system prompt for topic_selection.

On-disk structured output should validate as `topic_selection_result` (`schemas/json/topic_selection_result.schema.json`):

- **assigned** runs: v1 **skipped** branch (`skip_reason: assigned_topic`, `carried_topic_label`).
- **auto** Phase 0 stub runs: v1 **completed** branch with a deterministic `selected_topic_label` and empty `candidates_considered` (no live search yet).
