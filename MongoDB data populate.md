## Populating faker data using `faker-js`

```ts
import mongoose from "mongoose";
import { faker } from "@faker-js/faker";

// MongoDB connection
mongoose.connect("mongodb://127.0.0.1:27017/your_db_name", {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Define Product Schema
const productSchema = new mongoose.Schema({
  id: { type: String, required: true },
  productId: { type: String, default: null },
  image: { type: String, required: true },
  title: { type: String, required: true },
  price: { type: Number, required: true },
  originalPrice: { type: Number, required: true },
  rating: { type: Number, required: true },
  category: { type: String, default: null },
  productType: { type: String, enum: ["class", "product"], default: "product" },
});

const Product = mongoose.model("Product", productSchema);

// Generate Fake Products
const generateFakeProducts = (count = 10) => {
  return Array.from({ length: count }, () => ({
    id: faker.string.uuid(),
    productId: faker.string.uuid(),
    image: faker.image.url(),
    title: faker.commerce.productName(),
    price: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
    originalPrice: parseFloat(faker.commerce.price({ min: 500, max: 1000 })),
    rating: faker.number.float({ min: 1, max: 5, precision: 0.1 }),
    category: faker.commerce.department(),
    productType: faker.helpers.arrayElement(["class", "product"]),
  }));
};

// Insert Fake Data
const seedDatabase = async () => {
  try {
    const fakeProducts = generateFakeProducts(20); // Generate 20 fake products
    await Product.insertMany(fakeProducts);
    console.log("Fake products inserted successfully!");
  } catch (error) {
    console.error("Error inserting fake products:", error);
  } finally {
    mongoose.connection.close(); // Close connection
  }
};

seedDatabase();

```