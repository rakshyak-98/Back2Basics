**Parsing**

```js
moment("2026-03-24")                    // parse from string
moment(new Date())                      // parse from JS Date
moment("2026-03-24", "YYYY-MM-DD")      // parse with explicit format (safer)
```

**Formatting**

```js
moment().format("YYYY-MM-DD")           // "2026-03-24"
moment().format("MMMM DD")             // "March 24"
```

**Manipulation**

```js
moment().add(1, "days")                 // tomorrow
moment().subtract(1, "days")           // yesterday
moment().add(1, "months")              // next month
```

**Comparison**

```js
moment(a).isSame(moment(b), "day")      // same day check
moment(a).isBefore(moment(b), "day")    // before check
moment(a).isAfter(moment(b), "day")     // after check
moment(a).isSameOrBefore(b, "day")      // same or before
diff(b, "days")                         // difference in days
```

**Converting back to JS Date**

```js
moment().toDate()                       // convert back to native Date
```

**Key gotchas learned from this codebase**
- Always use `DateObject.format("YYYY-MM-DD")` instead of `toDate()` when working with `react-multi-date-picker` to avoid **IST timezone offset issues**
- Wrapping an already formatted string in `new Date()` causes **double conversion bugs**
- Prefer `moment(date, "YYYY-MM-DD")` over `moment(new Date(date))` to avoid timezone shifts