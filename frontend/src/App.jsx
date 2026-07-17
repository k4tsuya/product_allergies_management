import { useEffect, useState } from 'react';
import './App.css';

const language = 'nl';

function App() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/products')
      .then(response => response.json())
      .then(data => {
        setProducts(data);
        setIsLoading(false);
      });
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>Product Allergies</h1>
      </header>

      {isLoading ? (
        <p className="loading-message">Loading products...</p>
      ) : (
        <ul className="product-list">
          {products.map((product) => (
            <li key={product.id} className="product-card">
              <span className="product-name">{product.name}</span>
              {product.allergens.length > 0 ? (
                <div className="allergen-tags">
                  {product.allergens.map((allergen) => (
                    <span key={allergen.id} className="allergen-tag">
                      <img
                        src={`http://localhost:8000/static/icons/${allergen.code}.png`}
                        alt={allergen.description_en}
                        className="allergen-icon"
                      />
                      {language === 'nl' ? allergen.description_nl : allergen.description_en}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="no-allergens">
                  {language === 'nl' ? 'Geen bekende allergenen' : 'No known allergens'}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;