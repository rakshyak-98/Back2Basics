The `Intl` module provides built-in internationalization support for formatting numbers, dates, times, strings, and lists based on locale.

### **1. Number Formatting
- Formats numbers, currency, percentages.
- **Example:**
```js
new Intl.NumberFormat('de-DE').format(1234567.89); // "1.234.567,89"
new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(1500); // "$1,500.00"
new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR" }); // ₹12,34,56,789.00

```
### **2. Date & Time Formatting

- Formats dates/times according to locale.
```js
new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long' }).format(new Date()); // "11 février 2025"
```
### **3. Relative Time

- Displays time differences in natural language.
- **Example:**
```js
new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(-1, 'day'); // "yesterday"
	```
### **4. String Sorting & Comparison (**``**)**
- Sorts strings based on locale.
- **Example:**
```js
['Zebra', 'apple', 'Banana'].sort(new Intl.Collator('en').compare); // ["apple", "Banana", "Zebra"]
    ```
### **5. Pluralization (**``**)**

- Determines plural forms in different languages.
- **Example:**

```js
new Intl.PluralRules('en-US').select(1); // "one"
new Intl.PluralRules('en-US').select(2); // "other"
```


### **6. List Formatting (**``**)**

- Formats lists naturally.
- **Example:**

```js
new Intl.ListFormat('en', { style: 'long', type: 'conjunction' }).format(["Apple", "Banana", "Cherry"]);
// "Apple, Banana, and Cherry"
```


### **7. Text Segmentation (**``**)**

- Splits text into words/sentences.
- **Example:**

```js
[...new Intl.Segmenter('en', { granularity: 'word' }).segment("Hello world!")].map(s => s.segment);
// ["Hello", " ", "world", "!"]
```


### **8. Localized Display Names (**``**)**

- Provides localized names for languages/regions.
- **Example:**

```js
new Intl.DisplayNames(['fr'], { type: 'language' }).of('en'); // "anglais"
```

---
### **Advanced Use Case: Multi-Language E-Commerce Formatting**

#### **1. Dynamic Currency Formatting**

```js
function formatPrice(amount, currency, locale) {
	return new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount);
}
```

Usage:

```js
formatPrice(1500, 'USD', 'en-US'); // "$1,500.00"
```

#### **2. Localized Date Formatting**

```js
function formatDate(date, locale) {
	return new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(date);
}
```

Usage:

```js
formatDate(new Date('2025-05-20'), 'fr-FR'); // "20 mai 2025"
```

#### **3. Stock Availability Pluralization**

```js
function formatStockMessage(quantity, locale) {
	const pluralRules = new Intl.PluralRules(locale);
	return quantity === 1 ? "Only 1 item left!" : `Only ${quantity} items left!`;
}
```

Usage:

```js
formatStockMessage(5, 'en-US'); // "Only 5 items left!"
```

#### **4. Relative Time for Delivery Estimation**

```js
function estimateDelivery(days, locale) {
	return new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(days, 'day');
}
```

Usage:

```js
estimateDelivery(3, 'fr-FR'); // "dans 3 jours"
```

#### **5. Sorting Products Alphabetically**

```js
function sortProducts(products, locale) {
	return products.sort(new Intl.Collator(locale).compare);
}
```

Usage:

```js
sortProducts(["Zebra", "Äpple", "Banana"], 'de-DE'); // ["Äpple", "Banana", "Zebra"]
```

#### **6. Displaying Categories in Local Language**

```js
const categoryNames = new Intl.DisplayNames(['fr'], { type: 'region' });
categoryNames.of('US'); // "États-Unis"
```

---
