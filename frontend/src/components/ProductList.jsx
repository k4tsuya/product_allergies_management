import { useEffect, useState } from 'react';
import ProductCard from './ProductCard';
import { t } from '../localization';

function ProductList() {
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

  if (isLoading) {
    return <p className="loading-message">{t.loading}</p>;
  }

  return (
    <ul className="product-list">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </ul>
  );
}

export default ProductList;