import { useEffect, useState } from 'react';
import { language, t } from '../localization';

function AllergensPage() {
  const [allergens, setAllergens] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('http://localhost:8000/allergens').then(res => res.json()),
      fetch('http://localhost:8000/products').then(res => res.json()),
    ]).then(([allergensData, productsData]) => {
      setAllergens(allergensData);
      setProducts(productsData);
      setIsLoading(false);
    });
  }, []);

  if (isLoading) {
    return <p className="loading-message">{t.loading}</p>;
  }

  return (
    <div className="app">
      <div className="matrix-wrapper">
        <table className="allergen-matrix">
          <thead>
            <tr>
              <th className="matrix-corner">Product</th>
                {allergens.map((allergen) => (
                <th key={allergen.id} className="matrix-allergen-header">
                    <img
                    src={`http://localhost:8000/static/icons/${allergen.code}.png`}
                    alt={language === 'nl' ? allergen.description_nl : allergen.description_en}
                    title={language === 'nl' ? allergen.description_nl : allergen.description_en}
                    className="matrix-icon"
                    />
                </th>
                ))}
            </tr>
          </thead>
          <tbody>
            {products.map((product) => {
              const productAllergenIds = product.allergens.map((a) => a.id);

              return (
                <tr key={product.id}>
                  <td className="matrix-product-name">{product.name}</td>
                  {allergens.map((allergen) => (
                    <td key={allergen.id} className="matrix-cell">
                      {productAllergenIds.includes(allergen.id) ? '●' : ''}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="legend-section">
        <div className="legend">
          <span className="legend-item">
            <span className="legend-dot">●</span>
            {language === 'nl' ? ' Bevat dit allergeen' : ' Contains this allergen'}
          </span>
        </div>

        <h2 className="allergen-key-title">
          {language === 'nl' ? 'Allergenen' : 'Allergens'}
        </h2>
        <div className="allergen-key">
          {allergens.map((allergen) => (
            <span key={allergen.id} className="allergen-key-item">
              <img
                src={`http://localhost:8000/static/icons/${allergen.code}.png`}
                alt={language === 'nl' ? allergen.description_nl : allergen.description_en}
                className="allergen-key-icon"
              />
              {language === 'nl' ? allergen.description_nl : allergen.description_en}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export default AllergensPage;