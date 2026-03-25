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

## Time management

**Getting Current Time**

```js
moment()                                // current date and time
moment().hour()                         // current hour (0-23)
moment().minute()                       // current minute
moment().second()                       // current second
moment().millisecond()                  // current millisecond
```

**Formatting Time**

```js
moment().format("HH:mm:ss")            // "14:30:00" (24hr)
moment().format("hh:mm:ss A")          // "02:30:00 PM" (12hr)
moment().format("hh:mm A")             // "02:30 PM"
moment().format("YYYY-MM-DD HH:mm:ss") // "2026-03-24 14:30:00"
```

**Setting Time**

```js
moment().startOf("day")                // 00:00:00
moment().endOf("day")                  // 23:59:59
moment().startOf("hour")               // current hour, 00:00
moment().set("hour", 14)               // set to 2pm
moment().set({ hour: 14, minute: 30 }) // set multiple
```

**Manipulating Time**

```js
moment().add(1, "hours")               // 1 hour from now
moment().add(30, "minutes")            // 30 mins from now
moment().subtract(2, "hours")          // 2 hours ago
moment().add(1, "days").startOf("day") // start of tomorrow
```

**Difference in Time**

```js
moment(b).diff(moment(a), "hours")     // difference in hours
moment(b).diff(moment(a), "minutes")   // difference in minutes
moment(b).diff(moment(a), "seconds")   // difference in seconds

// detailed duration
const duration = moment.duration(moment(b).diff(moment(a)));
duration.hours()                       // hours part
duration.minutes()                     // minutes part
duration.seconds()                     // seconds part
```

**Comparing Time**

```js
moment(a).isBefore(moment(b))          // strict time comparison
moment(a).isAfter(moment(b))           
moment(a).isSame(moment(b), "hour")    // same hour
moment(a).isBetween(start, end)        // between two times
```

**Timezone Handling**

```js
// plain moment (local timezone)
moment().format("HH:mm")               // local time

// UTC
moment.utc()                           // current time in UTC
moment.utc("2026-03-24 14:30")        // parse as UTC
moment().utc().format("HH:mm")        // convert to UTC

// with moment-timezone package
moment.tz("2026-03-24 14:30", "Asia/Kolkata")  // IST
moment().tz("America/New_York").format()        // convert to NY time
```

**Durations**

```js
moment.duration(2, "hours")            // create duration
moment.duration("02:30:00")            // parse duration
moment.duration(5000, "milliseconds")  // from ms

const d = moment.duration(90, "minutes");
d.hours()                              // 1
d.minutes()                            // 30
d.humanize()                           // "an hour"
```

**Key Gotchas**

- `moment()` uses **local timezone** by default — this caused the IST `+05:30` shift issue in your datepicker
- Always use `moment.utc()` when working with API dates to avoid timezone bugs
- `startOf("day")` and `endOf("day")` are useful for date range queries to include the full day
- `moment.duration` is better than manual math for displaying time differences like `"2 hours 30 minutes"`