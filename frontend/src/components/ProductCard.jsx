import { language, t } from '../localization';

function ProductCard({ product }) {
  return (
    <li className="product-card">
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
        <p className="no-allergens">{t.noAllergens}</p>
      )}
    </li>
  );
}

export default ProductCard;