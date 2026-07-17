import { useEffect, useState } from 'react';
import './App.css';

const language = 'nl';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/products')
      .then(response => response.json())
      .then(data => setProducts(data));
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>Product Allergies</h1>
      </header>

      <ul className="product-list">
        {products.map((product) => (
          <li key={product.id} className="product-card">
            <span className="product-name">{product.name}</span>
            {product.allergens.length > 0 && (
              <div className="allergen-tags">
                {product.allergens.map((allergen) => (
                  <span key={allergen.id} className="allergen-tag">
                    {language === 'nl' ? allergen.description_nl : allergen.description_en}
                  </span>
                ))}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;