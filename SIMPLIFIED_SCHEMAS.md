# Simplified Tool Input/Output Schemas

## ✅ Simplified Parameter Lists

### Tool 1: web_search

**Input Schema:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | ✅ Yes | Search query (minLength: 2) |
| `max_results` | integer | No | Maximum number of results (1-10, default: 10) |

**Output:** `string` - Markdown-formatted search results

---

### Tool 2: prior_art_search

**Input Schema:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | ✅ Yes | Search query describing the invention (minLength: 3, maxLength: 1000) |
| `context` | string or null | No | Additional context from document |

**Output:** `string` - Prior art analysis report

**Changes:**
- ❌ Removed: `max_results` (now hardcoded to 20)
- ❌ Removed: `conversation_history`

---

### Tool 3: claim_drafting

**Input Schema:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_query` | string | ✅ Yes | Description of the invention (minLength: 10) |
| `context` | string or null | No | Additional context from document |

**Output:** `string` - AI-generated patent claims

**Changes:**
- ❌ Removed: `conversation_history`

---

### Tool 4: claim_analysis

**Input Schema:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `claims` | array[Claim] | ✅ Yes | List of claims to analyze (minItems: 1) |
| `context` | string or null | No | Additional context for analysis |

**Output:** `string` - Comprehensive claim analysis report

**Claim Schema (nested):**
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `claim_text` | string | ✅ Yes | The text of the patent claim |

**Changes:**
- ❌ Removed: `analysis_type` (now hardcoded to "comprehensive")
- ❌ Removed: `focus_areas` (now hardcoded to [])
- ✅ Kept: `context` parameter for additional context

---

## Summary: Before vs After

| Tool | Before (Params) | After (Params) | Removed |
|------|-----------------|----------------|---------|
| **web_search** | 2 | 2 | None |
| **prior_art_search** | 4 | 2 | max_results, conversation_history |
| **claim_drafting** | 3 | 2 | conversation_history |
| **claim_analysis** | 4 | 2 | analysis_type, focus_areas |

## Benefits of Simplification

1. **Cleaner API**: Fewer parameters to configure
2. **Easier to use**: Only essential parameters remain
3. **Better defaults**: Hardcoded optimal values:
   - Prior art search: 20 results
   - Analysis type: "comprehensive"
   - Focus areas: [] (all areas)
4. **Consistency**: All tools use only `context` for optional information

## All Tools Now Follow This Pattern

| Tool | Required Params | Optional Params | Total |
|------|----------------|-----------------|-------|
| web_search | query | max_results | 2 |
| prior_art_search | query | context | 2 |
| claim_drafting | user_query | context | 2 |
| claim_analysis | claims (array) | context | 2 |

✅ **Much simpler and easier to use!**

