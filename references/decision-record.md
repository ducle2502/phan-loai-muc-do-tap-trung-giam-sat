# Decision record

```json
{
  "id": "[ID]",
  "minimum_facts_sufficient": true,
  "evidenced_serious_consequence": false,
  "mandatory_condition_failed": false,
  "immediate_authority_intervention_required": false,
  "significant_deviation_or_delay_risk": false,
  "verification_gap_only": false,
  "positive_green_evidence": false,
  "pic_control_issue": "[none or concise control issue]",
  "selected_level": "[ĐỎ|CAM|VÀNG|XANH|XÁM]",
  "boundary_considered": "[adjacent boundary]",
  "decisive_evidence": ["[source-bound fact]"],
  "human_review_required": false
}
```

Consistency: `ĐỎ` requires severity/mandatory failure plus authority intervention. `CAM` requires significant deviation/risk. `VÀNG` requires an assessable verification gap. `XANH` requires positive evidence. `XÁM` requires inability to assess. Review is mandatory for `ĐỎ`, proposed `XANH` closure, and unresolved boundaries.
