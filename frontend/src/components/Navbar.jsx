import { Link } from 'react-router-dom';
import { t } from '../localization';

function Navbar() {
  return (
    <nav className="navbar">
      <span className="navbar-brand">{t.brand}</span>
      <div className="navbar-links">
        <Link to="/" className="navbar-link">Allergens</Link>
        
        <a  href="http://localhost:8000/products/pdf"
          className="navbar-link"
        >
          Download PDF
        </a>
      </div>
    </nav>
  );
}

export default Navbar;