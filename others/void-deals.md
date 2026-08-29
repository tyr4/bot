# Void Deals API

Unauthenticated sandbox endpoint

```
POST https://jxjshswlabnmkxhyhbdx.supabase.co/functions/v1/sandbox
```

---

## `void-deals`

All 3 offer slots for one calendar date.

**Request**

```jsonc
{
  "domain": "void-deals",
  "options": { "voidDeals": { "date": "2026-08-29" } }
}
```

| Field | Type | |
|---|---|---|
| `options.voidDeals.date` | string, `YYYY-MM-DD` | required |

**Response**

```jsonc
{
  "domain": "void-deals",
  "result": {
    "date": "2026-08-29",
    "slots": [
      { "slot": 0, "index": 1, "className": "ticketShard",
        "amount": 5, "cost": 990, "costPerUnit": 199 },
      { "slot": 1, "index": 0, "className": "crate",
        "amount": 1, "cost": 180, "costPerUnit": 181 },
      { "slot": 2, "index": 3, "className": "ticketShard",
        "amount": 49, "cost": 7590, "costPerUnit": 155 }
    ]
  }
}
```

---

## `void-deals-next`

Scans forward from a date for the first slot of a class at or under a
per-unit cost. Whole scan runs server-side in one call.

**Request**

```jsonc
{
  "domain": "void-deals-next",
  "options": {
    "voidDealsNext": {
      "startDate": "2026-08-29",
      "className": "crate",
      "maxCostPerUnit": 160
    }
  }
}
```

| Field | Type | |
|---|---|---|
| `startDate` | string, `YYYY-MM-DD` | required |
| `className` | string — see [Deal classes](#deal-classes) | required |
| `maxCostPerUnit` | number | required |
| `maxDaysScan` | number | optional, default `365` |
| `amountBand` | `"low" \| "high" \| "both"` | optional, default `"both"` |

**Response**

```jsonc
{
  "domain": "void-deals-next",
  "result": {
    "input": { "startDate": "2026-08-29", "className": "crate", "maxCostPerUnit": 160 },
    "deal": {
      "slot": 0, "index": 0, "className": "crate",
      "amount": 1, "cost": 150, "costPerUnit": 157, "date": "2026-09-02"
    }
  }
}
```

`deal` is `null` if nothing matches within `maxDaysScan` days.

---

## `void-deals-projection`

Sums every slot of one class over an N-day window. No budget cap — assumes
every offer is bought.

**Request**

```jsonc
{
  "domain": "void-deals-projection",
  "options": {
    "voidDealsProjection": { "startDate": "2026-08-29", "days": 7 }
  }
}
```

| Field | Type | |
|---|---|---|
| `startDate` | string, `YYYY-MM-DD` | required |
| `days` | number | required |
| `className` | string | optional, default `"ticket"` |

**Response**

```jsonc
{
  "domain": "void-deals-projection",
  "result": {
    "startDate": "2026-08-29", "days": 7, "className": "ticket",
    "totalAmount": 30, "totalCost": 7260,
    "deals": [
      { "slot": 0, "index": 2, "className": "ticket",
        "amount": 3, "cost": 710, "costPerUnit": 238, "date": "2026-08-30" }
      // ...one entry per matching slot in the window
    ]
  }
}
```

---

## Deal classes

| `className` | Reward | Cost / unit | Amount |
|---|---|---|---|
| `crate` | Weapon Crate | 150 – 200 | 1 |
| `ticketShard` | Shard | 150 – 200 | 1–9 or 20–49 |
| `ticket` | Hero Ticket | 200 – 300 | 1 – 9 |

---

## Errors

```jsonc
{ "error": "void-deals requires options.voidDeals.date" }
```

HTTP 400. Same shape for any missing/malformed field.

---

## Try it

**bash / curl**

```bash
curl -s -X POST "https://jxjshswlabnmkxhyhbdx.supabase.co/functions/v1/sandbox" \
  -H "Content-Type: application/json" \
  -d '{"domain":"void-deals","options":{"voidDeals":{"date":"2026-08-29"}}}'
```

**PowerShell**

```powershell
Invoke-RestMethod -Uri "https://jxjshswlabnmkxhyhbdx.supabase.co/functions/v1/sandbox" `
  -Method Post -ContentType "application/json" `
  -Body '{"domain":"void-deals","options":{"voidDeals":{"date":"2026-08-29"}}}'
```

